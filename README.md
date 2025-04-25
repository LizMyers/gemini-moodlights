# Gemini Moodlights TTS

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
- Multilingual text-to-speech via **Google Cloud TTS**
- Mastodon post
- Ambient + multilingual support

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
GCP_TTS_KEY_PATH=/full/path/to/your/gcp_service_account.json
MASTODON_TOKEN=your_mastodon_token
MASTODON_API_URL=https://mastodon.social/api/v1/statuses
```

### 5. Service Account Key

- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a **service account key** (JSON format) with **Text-to-Speech API** enabled
- Save it as `gcp_tts_key.json`
- Add its full path in `.env` as shown above

### 6. Git Ignore Sensitive Files

Be sure your `.gitignore` includes:

```
.env
gcp_tts_key.json
```

### 7. Run the App

```bash
source venv/bin/activate
python3 gemini_cheer_tts_final.py
```

---

## 🔊 Choose Your Voice

Open `gemini_cheer_tts_final.py` and set:

```python
COMPUTER_LANGUAGE = "fr-FR"  # or "es-ES", "de-DE", etc
```

Each language maps to a GCP Neural Voice:

```python
VOICE_MODELS = {
  "en-US": "en-US-Standard-C",
  "fr-FR": "fr-FR-Standard-B",
  ...
}
```

---

## 🌊 What Happens:

1. Script starts, greets you aloud
2. Listens to 2-second audio via Mac mic
3. Transcribes with Whisper
4. Gemini matches the mood to a color
5. Speaks the response aloud via GCP TTS
6. Posts color to Mastodon

---

## 🔧 Additional Tips

- Use `afplay output.wav` to test audio locally
- To debug TTS or Gemini output, watch the terminal logs
- Add support for other boards (ESP32, Pi Zero) by serial connection or webhooks

---
## Project tutorial:
https://www.hackster.io/elizmyers/gemini-moodlights-2e8fe4

## 😊 Thanks for trying it out!


