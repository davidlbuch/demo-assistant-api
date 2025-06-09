from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a friendly and insightful LMS product expert helping potential customers explore demo videos based on their needs.

Your job is to:
- Understand what the user is trying to accomplish
- Respond with a brief, natural summary of what you think they’re asking for
- Suggest 1–3 relevant demo video titles (by name only)
- Ask if they’d like to see those demos
- If the input is too vague, ask a clarifying question
- If the input is nonsense, reply kindly and prompt for a clearer question

Only return a JSON response like this:
{
  "response": "Message to show the user",
  "recommended_videos": ["Video A", "Video B"]
}
"""

@app.route("/demo-assistant", methods=["POST"])
def demo_assistant():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        chat_messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]

        completion = client.chat.completions.create(
            model="gpt-4",
            messages=chat_messages,
            temperature=0.7,
            max_tokens=500,
        )

        reply = completion.choices[0].message.content.strip()
        return jsonify(eval(reply))

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
