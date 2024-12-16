from flask import Flask, request, jsonify
from flask_cors import CORS  # Для разрешения запросов от других источников
import openai  # Для взаимодействия с OpenAI API
from dotenv import load_dotenv  # Для работы с переменными окружения
import os
from PyPDF2 import PdfReader  # Для обработки PDF
from PIL import Image  # Для обработки изображений
import io

# Загружаем переменные окружения из файла .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # Убедитесь, что .env файл содержит ключ OPENAI_API_KEY

# Инициализация Flask приложения
app = Flask(__name__)
CORS(app)  # Разрешаем CORS для всех маршрутов

@app.route('/')
def home():
    """Корневой маршрут для проверки работоспособности"""
    return "Welcome to GPT-powered server! 🚀", 200

@app.route('/api/chat', methods=['POST'])
def chat():
    """Обработка чата с GPT"""
    try:
        # Получаем данные из запроса
        data = request.json
        print("Received data:", data)  # Лог входящих данных для отладки

        # Проверяем, что данные корректны
        if not data or 'messages' not in data:
            return jsonify({"error": "Invalid request format. 'messages' is required."}), 400

        # Отправляем запрос в OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Используем модель GPT-4
            messages=data['messages']
        )
        print("Response from OpenAI:", response)  # Лог ответа OpenAI для отладки

        # Возвращаем ответ клиенту
        return jsonify(response)
    except Exception as e:
        print("Error:", str(e))  # Лог ошибки
        return jsonify({"error": str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload():
    """Обработка загрузки файлов (PDF и изображений)"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']

        # Если загружается PDF
        if file.filename.endswith('.pdf'):
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return jsonify({"text": text})

        # Если загружается изображение
        elif file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image = Image.open(io.BytesIO(file.read()))
            return jsonify({"info": f"Image size: {image.size}"})

        # Если формат файла не поддерживается
        else:
            return jsonify({"error": "Unsupported file format"}), 400
    except Exception as e:
        print("Error:", str(e))  # Лог ошибки
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Запуск сервера в режиме отладки
    app.run(debug=True)
