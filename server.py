from flask import Flask, request, jsonify
import openai
from PyPDF2 import PdfReader
from PIL import Image
import io

app = Flask(__name__)

openai.api_key = "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"  # Замените на свой ключ OpenAI

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=data['messages']
    )
    return jsonify(response)

@app.route('/api/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
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

if __name__ == '__main__':
    app.run(debug=True)


