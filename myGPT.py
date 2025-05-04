from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

with open("GPT_key.txt", 'r') as f:
    OPENAI_API_KEY = f.read().strip()
    
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

@app.route('/')

def index():
    return render_template('index.html')

@app.route('/chat', methods=["POST"])

def chat_with_gpt():
    try:
        user_message = request.json.get("message")
        
        response = requests.post(
            OPENAI_API_URL,
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": user_message}
                ]
            }
        )
        print('response:', response.json())


        data = response.json()

        if "choices" in data:
            
            reply = data["choices"][0]["message"]["content"]
            return jsonify({"status": "success", "reply": reply})
        
        else:
            
            error_code = data.get("error", {}).get("code", "")
            
            if error_code == "insufficient_quota":
                
                return jsonify({"status": "success", "reply": "Your quota has been exceeded. Please check your OpenAI account."})
            
            return jsonify({
                
                "status": "error",
                "message": data.get("error", {}).get("message", "OpenAI API returned an error")
                
            })


    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
