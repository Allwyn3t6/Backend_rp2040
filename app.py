from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# Set your OpenAI API Key from environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "sk-xxxx"))

# Load your RP2040 knowledge base
with open("data/rp2040_docs.txt", "r", encoding="utf-8") as f:
    rp2040_knowledge = f.read()

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json["question"]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert assistant that only answers questions about the RP2040 microcontroller. "
                    "Use the following knowledge base as context:\n" + rp2040_knowledge
                )
            },
            {
                "role": "user",
                "content": user_question
            }
        ]
    )

    answer = completion.choices[0].message.content
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
