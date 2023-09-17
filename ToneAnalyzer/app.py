from flask_cors import CORS
from langdetect import detect
from flask import Flask, request, jsonify

import requests

app = Flask(__name__, static_folder='static')

# Replace YOUR_API_KEY with your actual OpenAI API key
GPT_API_KEY = "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"

CORS(app)

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/analyze_tone', methods=['POST'])
def analyze_tone():
    text = request.json.get('text', '')
    
    # Detect language
    try:
        lang = detect(text)
    except:
        lang = 'en'  # Default to English if detection fails
    

    headers = {
        'Authorization': f'Bearer {GPT_API_KEY}',
        'Content-Type': 'application/json'
    }
     # Modify the prompt based on the detected language
    if lang == 'en':
        prompt = f"What is the tone of the following text: '{text}'?"
    elif lang == 'es':
        prompt = f"¿Cuál es el tono del siguiente texto: '{text}'?"
    # Add more languages here
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that can analyze the tone of text."},
            {"role": "user", "content": f"What is the tone of the following text: '{text}'?"}
        ]
    }
    
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    
    if response.status_code == 200:
        gpt_response = response.json()
        tone = gpt_response['choices'][0]['message']['content'].strip()
        return jsonify({"tone": tone,"lang": lang})
    else:
        print("Error:", response.status_code, response.json())
        return jsonify({"error": "Failed to analyze tone"}), 400

if __name__ == '__main__':
    app.run(debug=True)
