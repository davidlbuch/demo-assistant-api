from flask import Flask, request, jsonify
from openai import OpenAI
from supabase import create_client, Client
import os

app = Flask(__name__)

# 🔧 Load environment variables (adjust these for your project)
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

supabase: Client = create_client(supabase_url, supabase_key)
openai = OpenAI(api_key=openai_api_key)

@app.route("/demo-assistant", methods=["POST"])
def demo_assistant():
    data = request.json
    user_message = data.get("user_message")

    if not user_message:
        return jsonify({"error": "user_message is required"}), 400

    # Step 1: Pull all demo videos
    response = supabase.table("demo_videos").select("*").execute()
    all_videos = response.data

    # Step 2: Create a reference string for the assistant
    reference_text = ""
    for video in all_videos:
        reference_text += (
            f"Title: {video['title']}\n"
            f"Description: {video['description']}\n"
            f"Tags: {', '.join(video['tags']) if video['tags'] else ''}\n"
            f"Transcript: {video['transcript']}\n\n"
        )

    # Step 3: Ask GPT which titles match
    prompt = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant recommending LMS demo videos. "
                "The user will describe their learning needs. Choose the most relevant video titles "
                "based ONLY on the list of demos provided below. "
                "Respond with a JSON object with 2 keys: "
                "`recommended_videos` (a list of matching titles ONLY) and "
                "`response` (a friendly sentence explaining why you chose them).\n\n"
                f"Here is the list of available videos:\n\n{reference_text}"
            )
        },
        {
            "role": "user",
            "content": f"My training need is: {user_message}"
        }
    ]

    try:
        chat_response = openai.chat.completions.create(
            model="gpt-4",
            messages=prompt,
            temperature=0.3
        )
        content = chat_response.choices[0].message.content

        # Parse the result as JSON
        import json
        result = json.loads(content)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
