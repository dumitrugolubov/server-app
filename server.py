from flask import Flask, request, jsonify
from flask_cors import CORS  # Для разрешения CORS (запросы с других доменов)
import openai  # Для взаимодействия с OpenAI API
from dotenv import load_dotenv  # Для загрузки переменных окружения
import os
from PyPDF2 import PdfReader  # Для чтения PDF-файлов
from PIL import Image  # Для обработки изображений
import io

# Загрузка переменных окружения из файла .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # Убедитесь, что ваш ключ указан в .env

# Инициализация Flask приложения
app = Flask(__name__)
CORS(app)  # Включаем CORS для всех маршрутов

@app.route('/')
def home():
    """Маршрут для проверки работоспособности сервера"""
    return "Welcome to GPT-powered server! 🚀", 200

@app.route('/api/chat', methods=['POST'])
def chat():
    """Обработка чата с GPT"""
    try:
        # Получаем данные из запроса
        data = request.json
        print("Received data:", data)  # Логируем входящие данные

        # Проверяем, что данные содержат ключ 'messages'
        if not data or 'messages' not in data:
            return jsonify({"error": "Invalid request format. 'messages' is required."}), 400

        # Отправляем запрос в OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Используем модель GPT-4
            messages=data['messages']
        )

        # Логируем полный ответ от OpenAI API
        print("Raw OpenAI response:", response)

        # Извлекаем содержимое ответа
        if 'choices' in response and len(response['choices']) > 0:
            message = response['choices'][0]['message']['content']
            return jsonify({"message": message})
        else:
            return jsonify({"error": "Invalid OpenAI response format."}), 500
    except Exception as e:
        print("Error:", str(e))  # Логируем ошибку
        return jsonify({"error": str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload():
    """Обработка загрузки файлов (PDF и изображений)"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']

        # Обработка PDF
        if file.filename.endswith('.pdf'):
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return jsonify({"text": text})

        # Обработка изображений
        elif file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image = Image.open(io.BytesIO(file.read()))
            return jsonify({"info": f"Image size: {image.size}"})

        # Если формат файла не поддерживается
        else:
            return jsonify({"error": "Unsupported file format"}), 400
    except Exception as e:
        print("Error:", str(e))  # Логируем ошибку
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Запуск сервера
    app.run(debug=True)
