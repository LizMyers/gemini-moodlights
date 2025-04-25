# gemini_cheer_tts_final.py
# Author: Liz Myers 
# Description: This script control the current cheerlights color with your voice
# You can customize the array of languages, record time, and UI

# To see the current cheerlights color - install this extension for Chrome: 
# https://chromewebstore.google.com/detail/cheerlights/hpphbpobchhjfiknafjcpopiipahokpd?pli=1
# Or visit the cheerlights project in here https://lizmyers.sanddollarapps.com
# To learn more about the cheerlights project:  https://cheerlights.com/learn/

# RUN THIS FIRST TIME IN NEW TERMINAL source venv/bin/activate
# THEN python gemini_cheer_tts_final.py

import os
os.environ["PATH"] += os.pathsep + "/opt/homebrew/bin"
import time
import random
import requests
import whisper
import sounddevice as sd
from scipy.io.wavfile import write
from dotenv import load_dotenv
from google.cloud import texttospeech

# --- Load environment variables ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MASTODON_TOKEN = os.getenv("MASTODON_TOKEN")
MASTODON_API_URL = os.getenv("MASTODON_API_URL")

# --- Constants ---
VALID_COLORS = [
    "red", "green", "blue", "cyan", "white", "warmwhite", "oldlace",
    "purple", "magenta", "yellow", "orange", "pink"
]

# --- Personalization ---
USER_NAME = "Lizzie"
COMPUTER_LANGUAGE = "de-DE" 

VOICE_MODELS = {
    "en-US": "en-US-Standard-C", # female - US Englih
    "en-GB": "en-GB-Standard-N", # female - UK English
    "es-ES": "es-ES-Standard-A", # female - Spanish of Spain
    "fr-FR": "fr-FR-Standard-B", # male - French of France
    "de-DE": "de-DE-Standard-B", # male - German
    "it-IT": "it-IT-Standard-A", # female - Italian
    "pt-PT": "pt-PT-Standard-A", # female - Portuguese of Portugal
    "uk-UA": "uk-UA-Standard-A"  # female - Ukrainian
}
# Choose the ones you like from here:
# https://cloud.google.com/text-to-speech/docs/list-voices-and-types

GOOGLE_TTS_LANGUAGE = COMPUTER_LANGUAGE
GOOGLE_TTS_MODEL = VOICE_MODELS.get(COMPUTER_LANGUAGE, "en-US-Standard-C")  # fallback just in case

# --- Greeting Variations by Voice Model (not language code) ---
GREETINGS_MAP = {
    "en-US": [
        f"Hiya {USER_NAME}, how’s it going?",
        f"Good to see you, {USER_NAME}. What’s the vibe now?",
        f"Hey {USER_NAME}, what color are you feeling?",
        f"Welcome back {USER_NAME}! Let's set the mood.",
        f"Alright {USER_NAME}, let’s light the place!",
        f"Hi there. What color would you like?"
    ],
    "es-ES": [
        f"¡Hola {USER_NAME}! ¿Cómo estás?",
        f"¿Qué color te inspira hoy, {USER_NAME}?",
        f"¡Bienvenido, {USER_NAME}! Vamos a ponerle color al día.",
        f"Dime {USER_NAME}, ¿cómo te sientes hoy?",
        f"Hola, {USER_NAME}. ¿Qué ánimo tienes hoy?"
    ],
    "fr-FR": [
        f"Salut {USER_NAME}, comment ça va?",
        f"Quelle couleur reflète ton humeur aujourd'hui, {USER_NAME}?",
        f"Bonjour {USER_NAME}, quel est ton état d'esprit?",
        f"Hey {USER_NAME}, tu veux changer les lumières?",
        f"Bienvenue {USER_NAME}, choisis une couleur."
    ],
    "de-DE": [
        f"Hallo {USER_NAME}! Wie geht’s dir heute?",
        f"Welche Farbe passt zu deiner Stimmung, {USER_NAME}?",
        f"Guten Tag {USER_NAME}, wie fühlst du dich?",
        f"Hey {USER_NAME}, lass uns deine Stimmung zeigen.",
        f"Willkommen zurück {USER_NAME}, Zeit für Farben!"
    ],
    "it-IT": [
        f"Ciao {USER_NAME}, come va?",
        f"Che colore senti oggi, {USER_NAME}?",
        f"Bentornata {USER_NAME}, scegli un colore.",
        f"Ehi {USER_NAME}, come ti senti oggi?",
        f"Facciamo brillare le luci, {USER_NAME}."
    ],
    "pt-PT": [
        f"Olá {USER_NAME}, como estás?",
        f"Qual cor combina com o teu humor, {USER_NAME}?",
        f"Bem-vinda {USER_NAME}, vamos mudar as luzes!",
        f"Oi {USER_NAME}, que tal mudar as cores?",
        f"{USER_NAME}, como te sentes hoje?"
    ],
    "uk-UA": [
        f"Привіт {USER_NAME}, як справи?",
        f"Який настрій сьогодні, {USER_NAME}?",
        f"{USER_NAME}, обери колір для освітлення.",
        f"Вітаю {USER_NAME}, який колір тобі підходить?",
        f"Готові змінити світло, {USER_NAME}?"
    ]
}

# --- Helpers ---
# --- DURATION - change this to allow you to say more or less - keep < 5 sec for smaller files
def record_mac_mic(duration=3, filename="mic_input.wav", sample_rate=44100):
    print("\U0001F399️ Listening...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    write(filename, sample_rate, recording)
    return filename

def speak(message, language_code=None, gender=texttospeech.SsmlVoiceGender.NEUTRAL):
    language_code = language_code or COMPUTER_LANGUAGE
    model_name = VOICE_MODELS.get(language_code)

    if not model_name:
        print(f"❌ Unknown voice model for language code: {language_code}")
        return

    client = texttospeech.TextToSpeechClient.from_service_account_file(GCP_TTS_KEY_PATH)
    synthesis_input = texttospeech.SynthesisInput(text=message)
    voice = texttospeech.VoiceSelectionParams(
        name=model_name,
        language_code=language_code,
        ssml_gender=gender
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    temp_wav = "output.wav"
    with open(temp_wav, "wb") as out:
        out.write(response.audio_content)
    os.system(f"afplay {temp_wav}")

def ask_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print("❌ Gemini Error:", response.text)
        return "", ""
    text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    return parse_gemini_response(text)

def parse_gemini_response(text):
    color, message = "", ""
    for line in text.splitlines():
        if line.lower().startswith("color:"):
            color = line.split(":", 1)[1].strip().lower()
        elif line.lower().startswith("message:"):
            message = line.split(":", 1)[1].strip()
    return color, message

def post_to_mastodon(color):
    headers = {"Authorization": f"Bearer {MASTODON_TOKEN}", "Content-Type": "application/json"}
    data = {"status": f"#cheerlights {color}"}
    response = requests.post(MASTODON_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        print("✅ Posted to Mastodon!")
    else:
        print("❌ Mastodon error:", response.text)


# --- Start Conversation ---
# --- Begin main flow ---
greeting_template = random.choice(GREETINGS_MAP[COMPUTER_LANGUAGE])
speak(greeting_template.format(user=USER_NAME), COMPUTER_LANGUAGE)

filename = record_mac_mic()
model = whisper.load_model("base")
result = model.transcribe(filename)
user_input = result["text"].strip()

print(f"📝 Whisper Transcript: {user_input}")

# LANGUAGE_HINTS maps full GCP voice language codes to prompt instructions
LANGUAGE_HINTS = {
    "en-US": "Respond in English.",
    "en-GB": "Respond in English.",
    "es-ES": "Responde en español.",
    "fr-FR": "Réponds en français.",
    "de-DE": "Antworten Sie auf Deutsch.",
    "it-IT": "Rispondi in italiano.",
    "pt-PT": "Responda em português.",
    "uk-UA": "Відповідай українською."
}

# --- Language instruction for Gemini ---
if COMPUTER_LANGUAGE not in LANGUAGE_HINTS:
    print(f"⚠️ Warning: No language hint for {COMPUTER_LANGUAGE}, defaulting to English.")
    language_hint = "Respond in English."
else:
    language_hint = LANGUAGE_HINTS[COMPUTER_LANGUAGE]

# Use .get to safely fallback to English if the key is missing or malformed
language_hint = LANGUAGE_HINTS.get(COMPUTER_LANGUAGE, "Respond in English.")

extraction_prompt = (
    f"{language_hint}\n"
    f"The user said: \"{user_input}\"\n"
    f"Suggest a Cheerlights color that matches this mood.\n"
    f"Valid colors are: {', '.join(VALID_COLORS)}.\n"
    f"If you can’t match a color, pick a random one.\n"
    f"Important: Do not use emojis or special symbols. Keep the language friendly but natural.\n"
    f"Keep punctuation simple (periods, commas, exclamation marks are fine).\n"
    f"Return your answer like this:\n"
    f"Color: <color>\n"
    f"Message: <friendly message>"
)

color, message = ask_gemini(extraction_prompt)

print(f"🧠 Gemini Raw Response:\nColor: {color}\nMessage: {message}")

if not color or color not in VALID_COLORS:
    color = random.choice(VALID_COLORS)
    message = f"Feeling playful? Let's go with {color}."

print(f"🎨 Final Color: {color}")
print(f"💬 Message to speak: {message}")
print(f"🚀 Posting to Mastodon...")

speak(message, COMPUTER_LANGUAGE)
post_to_mastodon(color)