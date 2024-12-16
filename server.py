from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
from PIL import Image
import io

# Загрузка переменных окружения
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Новый маршрут для корневого URL
@app.route('/')
def home():
    return "Welcome to your GPT-powered server! 🚀", 200

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=data['messages']
        )
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    try:
        if file.filename.endswith('.pdf'):
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return jsonify({"text": text})
        elif file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image = Image.open(io.BytesIO(file.read()))
            return jsonify({"info": f"Image size: {image.size}"})
        else:
            return jsonify({"error": "Unsupported file format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
