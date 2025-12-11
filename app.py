from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)

# Load small LLM model (DistilGPT-2 - 82M parameters)
# No API key needed - runs locally
print("Loading model...")
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
print("Model loaded successfully!")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/api/data')
def api_data():
    return {
        'message': 'Hello from Flask API!',
        'status': 'success'
    }

@app.route('/api/chat', methods=['POST'])
def chat_api():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Generate response using the model
        inputs = tokenizer.encode(user_message, return_tensors='pt', max_length=100, truncation=True)
        
        # Generate text
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_length=150,
                num_return_sequences=1,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Decode the response
        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Remove the input prompt from response
        if response_text.startswith(user_message):
            response_text = response_text[len(user_message):].strip()
        
        return jsonify({
            'response': response_text if response_text else "I generated a response!",
            'model': model_name
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
