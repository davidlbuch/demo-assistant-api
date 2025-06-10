from flask import Flask, request, jsonify
from openai import OpenAI
import os
import json

app = Flask(__name__)

# 🔧 Load environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
openai = OpenAI(api_key=openai_api_key)

@app.route("/demo-assistant", methods=["POST"])
def demo_assistant():
    data = request.json
    user_message = data.get("user_message")
    array_raw = data.get("array")

    if not user_message:
        return jsonify({"error": "user_message is required"}), 400
    if not array_raw:
        return jsonify({"error": "array is required"}), 400

    # Step 1: Try to parse the stringified JSON array
    try:
        all_videos = json.loads(array_raw)
    except Exception as e:
        return jsonify({"error": "Invalid JSON in array", "details": str(e)}), 400

    # Step 2: Build reference text for GPT
    reference_text = ""
    for video in all_videos:
        reference_text += (
            f"Title: {video.get('title', '')}\n"
            f"Description: {video.get('description', '')}\n\n"
        )

    # Step 3: GPT Prompt
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
        result = json.loads(content)

        # Match titles to full objects
        recommended_titles = result.get("recommended_videos", [])
        explanation = result.get("response", "")

        matched_videos = [
            video for video in all_videos
            if video.get("title", "").strip().lower() in [t.strip().lower() for t in recommended_titles]
        ]

        return jsonify({
            "recommended_videos": matched_videos,
            "demo_assistant_response": explanation
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
