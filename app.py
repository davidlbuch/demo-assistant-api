from flask import Flask, request, jsonify
import os
import openai

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/recommendations", methods=["POST"])
def recommend_videos():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        prompt = f"You are an LMS demo assistant. Based on this user message: '{user_message}', return a list of 2-4 LMS features that best match their needs. Return the feature names exactly as they appear in the video titles."

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You recommend LMS feature demo videos based on user needs. Only use available titles."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        reply = response["choices"][0]["message"]["content"]
        # Expecting a simple list format
        video_titles = [line.strip("- ").strip() for line in reply.split("\n") if line.strip()]

        return jsonify({"recommended_videos": video_titles})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
