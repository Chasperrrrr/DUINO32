from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

# Initialize Groq client
client = Groq(api_key="YOUR_API_KEY")


def generate_code(command):

    prompt = f"""
You are an expert embedded systems engineer.

Convert the following user instruction into working ESP32 or Arduino firmware.

Rules:
- Use Arduino C++ syntax
- Include setup() and loop()
- Use reasonable GPIO pins
- Add comments explaining the logic
- Use Serial.begin(115200) if serial output is needed
- Return ONLY the code

Instruction:
{command}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


@app.route("/generate", methods=["POST"])
def generate():

    data = request.json
    command = data.get("command", "")

    if command == "":
        return jsonify({"code": "No command provided"}), 400

    try:
        code = generate_code(command)
        return jsonify({"code": code})
    except Exception as e:
        return jsonify({"code": f"Error generating code: {str(e)}"}), 500


@app.route("/")
def home():
    return "Natural Language to Embedded Code API with Groq is running."


if __name__ == "__main__":
    app.run(debug=True)