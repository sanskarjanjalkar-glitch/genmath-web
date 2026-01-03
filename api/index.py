from flask import Flask, request, jsonify
from google import genai
from PIL import Image
import io

app = Flask(__name__)

# --- CONFIGURATION ---
GEMINI_API_KEY = "AIzaSyBK45Qqo88fydpa-wX0dYX9U6nQ4usGRzM"  # hardcoded as requested

# Create Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

@app.route('/api/solve', methods=['POST'])
def solve():
    try:
        # 1. AUTH CHECK
        auth_header = request.headers.get('Authorization')
        if auth_header != "Bearer admin-token-123":
            return jsonify({"error": "Unauthorized. Please login."}), 401

        # 2. GET DATA
        query = request.form.get('query', '')
        image_file = request.files.get('image')

        prompt = """
You are a Math Professor.

1. Identify the math problem.
2. Provide a rigorous STEP-BY-STEP derivation using LaTeX.
3. Explain the concept clearly.
4. State the Final Answer.
"""

        # 3. GEMINI CALL
        if image_file:
            image_bytes = image_file.read()
            image = Image.open(io.BytesIO(image_bytes))

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    prompt,
                    image
                ]
            )
        else:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"{prompt}\nProblem: {query}"
            )

        return jsonify({"solution": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Local run
if __name__ == '__main__':
    app.run(debug=True)







