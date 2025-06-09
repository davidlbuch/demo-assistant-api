from flask import Flask, request, jsonify
import os
import openai

app = Flask(__name__)

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/recommendations", methods=["POST"])
def recommend_videos():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        prompt = f"You are an LMS demo assistant. Based on this user message: '{user_message}', return a list of 2-4 LMS features that best match their needs. Respond ONLY with a plain JSON array like: [\"Ease of use\", \"Reporting\"]"

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You recommend LMS feature demo videos based on user needs. Only use available titles."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        reply = response.choices[0].message.content.strip()

        return jsonify({"recommended_videos": eval(reply)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
