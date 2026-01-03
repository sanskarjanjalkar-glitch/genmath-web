from flask import Flask, request, jsonify
import google.generativeai as genai
from PIL import Image
import io
import os

app = Flask(__name__)

# --- CONFIGURATION ---
# We will set this in Vercel Settings later
GEMINI_API_KEY = "AIzaSyBK45Qqo88fydpa-wX0dYX9U6nQ4usGRzM" 

def configure_gemini():
    if not GEMINI_API_KEY:
        raise ValueError("API Key not found")
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel('gemini-1.5-flash')

@app.route('/api/solve', methods=['POST'])
def solve():
    try:
        # 1. AUTHENTICATION CHECK (Basic Login System)
        auth_header = request.headers.get('Authorization')
        if auth_header != "Bearer admin-token-123": # Simple hardcoded token for demo
            return jsonify({"error": "Unauthorized. Please login."}), 401

        # 2. GET DATA
        data = request.form.get('query', '')
        image_file = request.files.get('image')

        # 3. GEMINI VISION & SOLVING
        model = configure_gemini()
        
        prompt = """
        You are a Math Professor. 
        1. Identify the math problem.
        2. Provide a rigorous, STEP-BY-STEP derivation using LaTeX for math.
        3. Explain the concept clearly.
        4. State the Final Answer.
        """

        response = None
        if image_file:
            # Load image for Gemini Vision (Replaces Tesseract)
            img_bytes = image_file.read()
            image = Image.open(io.BytesIO(img_bytes))
            response = model.generate_content([prompt, image])
        else:
            response = model.generate_content(f"{prompt}\nProblem: {data}")

        return jsonify({"solution": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vercel requires this for serverless execution
if __name__ == '__main__':
    app.run()
us this o
from google import genai

# The client gets the API key from the environment variable GEMINI_API_KEY.
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text)
Error: 404 models/gemini-1.5-flash is not found for API version v1beta, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.
fix this an use key hardcode don't get from env fix this
 



ChatGPT can make mistakes. Check important info. See Cookie Preferences.
We use cookies
