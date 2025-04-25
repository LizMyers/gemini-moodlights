# Gemini Moodlights

This project allows you to control Cheerlights with Gemini and your voice. Edit the script to enter your own name, prefeered language and run it. Gemini asks how you're doing and interprets your answer as a color. Then the new color is posted to Mastodon where the Cheerlights bot picks it up and changes the color. To learn more about Cheerlights, see this link: https://www.cheerlights.com/learn.

To see the cheerlight color change IRL:
1. Visit this cheerlights project within Liz's portfolio: https://lizmyers.sanddollarapps.com
2. Install the Chrome Extension for Cheerlights: https://chromewebstore.google.com/detail/cheerlights/hpphbpobchhjfiknafjcpopiipahokpd
3. Make an IoT device with a NeoPixel Ring, Matrix, LED Strips
4. Fallback --> open terminal and see which color Gemini chose

---

## ✨ Features

- Voice recording via your computer mic
- Whisper transcription
- Gemini prompt-to-color mapping
- Multi-lingual and high quality voices from GCP
- Mastodon post
- Ambiant lighting and Cheerlights Voice UI

---

## 🚀 Setup Instructions

### 1. Clone the Project

```bash
git clone https://github.com/LizMyers/gemini_cheerlights.git
cd gemini_cheerlights
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

Make sure the following packages are installed:

- `openai-whisper`
- `sounddevice`
- `scipy`
- `python-dotenv`
- `requests`
- `google-cloud-texttospeech`

You can install manually if needed:

```bash
pip install openai-whisper sounddevice scipy python-dotenv requests google-cloud-texttospeech
```

### 4. Setup `.env` File

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
GCP_TTS_KEY_PATH=path_to_your_service_key.JSON (at root of your project)
MASTODON_TOKEN=your_mastodon_token
MASTODON_API_URL=https://mastodon.social/api/v1/statuses
```

### 5. Gemini API Key

- Go to Gemini AI Studio (https://aistudio.google.com/prompts/new_chat)
- Click the Get API Key Button
- Select Gemini 2.0 Flash - it's FREE

### 6. Google Cloud Service Account Key (for Text-to-Speech)

- Go to the [Google Cloud Console](https://console.cloud.google.com/)
- Create a **new project** (or select an existing one)
- In the left sidebar, go to **APIs & Services > Library**
- Search for **Text-to-Speech API**
- **Enable** the Text-to-Speech API
- In the sidebar, go to **APIs & Services > Credentials**
- Click **Create Credentials > Service Account**
- Give your Service Account a name (example: `gemini-tts`)
- Click **Create and Continue** (default roles are fine for this project)
- After the Service Account is created, find it in the list and **click it**
- Under the **Keys** tab, click **Add Key > Create New Key**
- Choose **JSON** format and **Download** the key
- Save this `.json` file in the root project directory
- In your `.env` file, set the path to this JSON key as `GCP_TTS_KEY_PATH`

> **Note:** This Service Account key is needed so your project can synthesize voice messages with Google Cloud Text-to-Speech.

> **Tip:** Google Cloud may ask you to set up a billing account when enabling the Text-to-Speech API, even if you stay within the free tier. Don't worry — for light personal use like this project, you won't be charged.

### 7. Mastodon Token

- Get your Mastodon Account (https://mastodon.social)
- Preference > Development > New Application
- Name it something like VoiceToMastodon
- **IMPORTANT** check write:statuses

### 8. Git Ignore Sensitive Files

Be sure your `.gitignore` includes:

```
.env
```

### 9. Run the App

```bash
source venv/bin/activate
python3 gemini_cheer_tts_final.py
```

---

## 🔊 Add Your Name and Choose Your Voice

Open `gemini_cheer_tts_final.py` and set:

```python
USER_NAME="[YOU FIRST NAME GOES HERE]"
COMPUTER_LANGUAGE = "en-US"  # or "en-GB, es-ES, fr-FR", "de-DE", etc
```

Each language maps to a GCP Neural Voice:

```python
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
```

---

## 🌊 What Happens:

1. Script starts, greets you aloud
2. Listens to 3-second audio via laptop mic
3. Transcribes speech to text with Whisper
4. Gemini matches the mood to a color
5. Whisper transcribes text to speech (TTS)
6. Gemini speaks a response message and...
7. Posts the new color to Mastodon 
8. Cheerlights following the Thingspeak channel 1417 pick up the color

To learn more about how Cheerlights work, see: http://cheerlights.io/learn

---

## 🔧 Additional Tips

- Use `afplay output.wav` to test audio locally
- To debug TTS or Gemini output, watch the terminal logs
- On Mac, use Automator to launch from a desktop app

---
## Project tutorial:
https://www.hackster.io/elizmyers/gemini-moodlights-2e8fe4

## 😊 Thanks for trying it out!


