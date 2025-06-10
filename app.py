from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# テスト確認用　250608
print("API KEY from env:", os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')  # ←ここを修正

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは高齢者と外国人介護士を支援する親切な会話ボットです。"},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response["choices"][0]["message"]["content"].strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"エラーが発生しました: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
