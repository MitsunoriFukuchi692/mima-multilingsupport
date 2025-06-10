from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

print("API KEY from env:", os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    selected_lang = request.json.get("lang", "ja")  # 追加：言語コードを取得

    # 言語別プロンプト（日本語, 英語, タガログ語, インドネシア語, マレー語）
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

if __name__ == '__main__':
    app.run(debug=True)
