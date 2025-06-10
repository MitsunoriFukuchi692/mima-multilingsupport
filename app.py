from flask import Flask, render_template, request, jsonify, send_file
from openai import OpenAI
import os
from dotenv import load_dotenv
from google.cloud import texttospeech
from io import BytesIO

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    selected_lang = request.json.get("lang", "ja")

    system_prompts = {
        "ja": "あなたは高齢者と外国人介護士を支援する親切な会話ボットです。",
        "en": "You are a friendly support chatbot assisting elderly people and foreign caregivers.",
        "tl": "Ikaw ay isang magiliw na chatbot na tumutulong sa matatanda at mga banyagang tagapag-alaga.",
        "id": "Anda adalah chatbot ramah yang membantu lansia dan perawat asing.",
        "ms": "Anda ialah chatbot mesra yang membantu warga emas dan penjaga asing."
    }

    prompt = system_prompts.get(selected_lang, system_prompts["ja"])

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"エラーが発生しました: {e}"}), 500

@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text", "")
    lang = data.get("lang", "ja")

    lang_map = {
        "ja": "ja-JP",
        "en": "en-US",
        "tl": "fil-PH",
        "id": "id-ID",
        "ms": "ms-MY"
    }

    voice_lang = lang_map.get(lang, "ja-JP")

    tts_client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=voice_lang,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = tts_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    audio_data = BytesIO(response.audio_content)
    return send_file(audio_data, mimetype="audio/mp3")

if __name__ == '__main__':
    app.run(debug=True)
