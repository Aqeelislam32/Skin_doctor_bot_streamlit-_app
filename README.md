# AI Skin Assistant (Portfolio Demo)

Free-tier stack: **Groq Whisper** (speech-to-text) + **Gemini 2.5 Flash** (image + text
analysis) + **gTTS** (text-to-speech) + **Gradio** (UI).

⚠️ Ye sirf ek portfolio/demo project hai, real medical use ke liye nahi.

## Setup

```bash
cd doctor_bot
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env
```

`.env` file open karke apni free API keys daal dein:

- `GROQ_API_KEY` → https://console.groq.com (free)
- `GEMINI_API_KEY` → https://aistudio.google.com/apikey (free)

## Run

```bash
python app.py
```

Browser mein `http://127.0.0.1:7860` open hoga.

## Folder Structure

```
doctor_bot/
├── app.py          # Gradio UI + main workflow
├── speech.py        # Groq Whisper (voice → text)
├── vision.py         # Gemini 2.5 Flash (image + text → response)
├── llm.py            # optional: text-only follow-up questions
├── tts.py            # gTTS (text → speech)
├── utils.py          # small helpers
├── requirements.txt
├── .env.example
└── uploads/          # generated audio responses land here
```

## Workflow

1. User skin image upload karta hai.
2. User voice record karta hai (ya text type karta hai) apni problem describe karne ke liye.
3. Groq Whisper voice ko text mein convert karta hai.
4. Image + patient text Gemini 2.5 Flash ko jaate hain.
5. Gemini cautious, non-diagnostic response deta hai.
6. gTTS response ko audio mein convert karta hai.
7. User ko text + audio dono milta hai.

## Notes / Next Steps

- Is demo mein AI kabhi bhi definitive diagnosis nahi deta — hamesha "consult a doctor"
  wala disclaimer attach hota hai. Ye production-safety ke liye zaroori hai.
- Agar aap ise real users ke liye deploy karte hain, to legal/medical disclaimer aur
  data-privacy (image storage, consent) par extra dhyan dein.
- `llm.py` optional follow-up chat ke liye hai — agar chahein to app.py mein ek chat box
  add karke isko wire kar sakte hain.
