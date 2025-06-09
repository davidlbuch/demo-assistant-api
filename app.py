import os
from flask import Flask, request, jsonify
from openai import OpenAI
from supabase import create_client, Client
import traceback

# === CONFIG ===
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)

# === ROUTE: RECOMMEND VIDEOS ===
@app.route("/demo-assistant", methods=["POST"])
def demo_assistant():
    try:
        data = request.json
        user_message = data.get("user_message", "")

        if not user_message:
            return jsonify({"error": "user_message is required"}), 400

        supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)
        rows = supabase.table("demo_videos").select("title, description, transcript").execute().data

        # Build assistant prompt
        prompt = (
            "You are a helpful LMS demo assistant. The user will describe their training needs, "
            "and you will recommend the most relevant videos. You must only recommend videos "
            "whose titles exactly match one of the following:\n\n"
        )
        for row in rows:
            prompt += f"- {row['title']}: {row['description']}\n"

        prompt += "\nBe concise and conversational. Recommend only the most relevant titles (1–3 max). "
        prompt += "Respond with JSON like this: {\"recommended_videos\": [...], \"response\": \"...\"}.\n"
        prompt += f"\nUser: {user_message}"

        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )

        reply = completion.choices[0].message.content

        return jsonify(eval(reply))  # You may sanitize this if needed

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# === ROUTE: FETCH ALL VIDEOS ===
@app.route("/all-videos", methods=["GET"])
def all_videos():
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)
        response = supabase.table("demo_videos").select("*").execute()
        data = response.data

        videos = [
            {
                "title": item["title"],
                "description": item["description"],
                "url": item["thumbnail_url"],
                "vimeo": item["vimeo_url"]
            }
            for item in data
        ]

        return jsonify({"all_videos": videos})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# === START LOCAL TESTING ===
if __name__ == "__main__":
    app.run(debug=True)
