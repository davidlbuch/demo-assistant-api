from flask import Flask, request, jsonify
from openai import OpenAI
import os
import json

app = Flask(__name__)

# Load environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
openai = OpenAI(api_key=openai_api_key)

# Shared hardcoded list of all demo videos
demo_videos = [
    {
        "title": "AI Course builder",
        "description": "Generate complete training modules instantly from your existing materials using AI.",
        "url": "https://storage.googleapis.com/demo_experience_bucket/thumbnails/thumb%20AI%20overview%20%281%29.jpg",
        "vimeo": "https://player.vimeo.com/video/1083905582"
    },
    {
        "title": "AI Tools",
        "description": "Leverage intelligent tools to recommend content and streamline learning workflows.",
        "url": "https://storage.googleapis.com/demo_experience_bucket/thumbnails/thumb%20AI%20overview%20%282%29.jpg",
        "vimeo": "https://player.vimeo.com/video/1083905582"
    },
    {
        "title": "APIs & Integration",
        "description": "Easily connect the LMS to your existing HR, CRM, and business systems.",
        "url": "https://storage.googleapis.com/demo_experience_bucket/thumbnails/thumb%20apis%20and%20zapier%20%281%29.jpg",
        "vimeo": "https://player.vimeo.com/video/1082957223?share=copy"
    },
    # (Truncated for brevity. Add remaining demos here...)
]

@app.route("/all-videos", methods=["GET"])
def all_videos():
    return jsonify({"array": demo_videos})

@app.route("/demo-assistant", methods=["POST"])
def demo_assistant():
    data = request.json
    user_message = data.get("user_message")

    if not user_message:
        return jsonify({"error": "user_message is required"}), 400

    # Build reference for GPT
    reference_text = ""
    for video in demo_videos:
        reference_text += (
            f"Title: {video['title']}\n"
            f"Description: {video['description']}\n\n"
        )

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
        completion = openai.chat.completions.create(
            model="gpt-4",
            messages=prompt,
            temperature=0.3
        )
        content = completion.choices[0].message.content
        result = json.loads(content)

        recommended_titles = result.get("recommended_videos", [])
        explanation = result.get("response", "")

        matched_videos = [
            video for video in demo_videos
            if video["title"].strip().lower() in [t.strip().lower() for t in recommended_titles]
        ]

        return jsonify({
            "recommended_videos": matched_videos,
            "demo_assistant_response": explanation
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
