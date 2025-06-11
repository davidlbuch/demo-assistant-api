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
    {
        "title": "Certificates and Badges",
        "description": "Reward and track learner achievements with automatically issued credentials.",
        "url": "https://storage.googleapis.com/demo_experience_bucket/thumbnails/thumb%20certificates%20and%20badges.jpg",
        "vimeo": "https://player.vimeo.com/video/1084056633?share=copy"
    },
    {
        "title": "Conference Format",
        "description": "Run large-scale live training events with multiple sessions and registration options.",
        "url": "https://storage.googleapis.com/demo_experience_bucket/thumbnails/thumb%20conferences%20%281%29.jpg",
        "vimeo": "https://player.vimeo.com/video/1084056596?share=copy"
    },
    {
        "title": "Content Types",
        "description": "Support a wide range of training content including videos, documents, and quizzes.",
        "url": "https://storage.googleapis.com/demo_experience_bucket/thumbnails/thumb%20content%20types%20%281%29.jpg",
        "vimeo": "https://player.vimeo.com/video/1082957273?share=copy"
    },
    {
        "title": "Credit Management",
        "description": "Track and manage continuing education credits and learning hour requirements.",
        "url": "https://storage.googleapis.com/demo_experience_bucket/thumbnails/thumb%20credit%20%281%29.jpg",
        "vimeo": "https://player.vimeo.com/video/1084063604?share=copy"
    },
    {
        "title": "Discussions",
        "description": "Enable course-based dialogue with threaded discussions to drive engagement.",
        "url": "https://storage.googleapis.com/demo_experience_bucket/thumbnails/thumb%20discussions.jpg",
        "vimeo": "https://player.vimeo.com/video/1082960861?share=copy"
    },
    {
        "title": "Ease of use",
        "description": "Designed for intuitive navigation by both learners and administrators.",
        "url": "https://storage.googleapis.com/demo_experience_bucket/thumbnails/thumb%20ease%20of%20use.jpg",
        "vimeo": "https://player.vimeo.com/video/1082957258?share=copy"
    },
    {
        "title": "Finding and Completing a Course",
        "description": "Help users quickly locate and complete their assigned or recommended courses.",
        "url": "https://storage.googleapis.com/demo_experience_bucket/thumbnails/thumb%20Finding%20and%20completing.jpg",
        "vimeo": "https://player.vimeo.com/video/1082567534?share=copy#t=0"
    },
    {
        "title": "Interface and Groups",
        "description": "Assign access, views, and permissions based on user roles and group memberships.",
        "url": "https://storage.googleapis.com/demo_experience_bucket/thumbnails/thumb%20groups%20%281%29.jpg",
        "vimeo": "https://player.vimeo.com/video/1082564274?share=copy#t=0"
    },
    {
        "title": "My Learning",
        "description": "Give learners a personalized list of all assigned, in-progress, and completed training.",
        "url": "https://storage.googleapis.com/demo_experience_bucket/thumbnails/thumb%20manda%20tory%20training.jpg",
        "vimeo": "https://player.vimeo.com/video/1082568518?share=copy#t=0"
    },
    {
        "title": "Rapid Content with Drive and 365",
        "description": "Quickly build training from your existing content in Google Drive or Microsoft 365.",
        "url": "https://storage.googleapis.com/demo_experience_bucket/thumbnails/thumb%20drive%20intgration%20%281%29.jpg",
        "vimeo": "https://player.vimeo.com/video/1082563462?share=copy#t=0"
    },
    {
        "title": "Registration Expiration",
        "description": "Limit course access windows with configurable registration expiration settings.",
        "url": "https://storage.googleapis.com/demo_experience_bucket/thumbnails/thumb%20reg%20expiration%20%281%29.jpg",
        "vimeo": "https://player.vimeo.com/video/1084062580?share=copy"
    },
    {
        "title": "Reporting",
        "description": "Track learner progress, completions, and compliance through robust reporting tools.",
        "url": "https://storage.googleapis.com/demo_experience_bucket/thumbnails/thumb%20reporting.jpg",
        "vimeo": "https://player.vimeo.com/video/1082565301?share=copy#t=0"
    },
    {
        "title": "Roster Management",
        "description": "Organize and manage learner lists by department, team, or custom groups.",
        "url": "https://storage.googleapis.com/demo_experience_bucket/thumbnails/thumb%20roster%20%281%29.jpg",
        "vimeo": "https://player.vimeo.com/video/1082957320?share=copy"
    },
    {
        "title": "Uploading a SCORM course",
        "description": "Easily upload SCORM-compliant training content into the platform.",
        "url": "https://storage.googleapis.com/demo_experience_bucket/thumbnails/thumb%20uploading%20scorm%20%281%29.jpg",
        "vimeo": "https://player.vimeo.com/video/1084059425?share=copy"
    },
    {
        "title": "User Onboarding",
        "description": "Automate new user setup with guided onboarding and first-course assignment.",
        "url": "https://storage.googleapis.com/demo_experience_bucket/thumbnails/thumb%20onboarding.jpg",
        "vimeo": "https://player.vimeo.com/video/1084056655?share=copy"
    },
    {
        "title": "Video Format",
        "description": "Deliver crisp, responsive video learning experiences on all devices.",
        "url": "https://storage.googleapis.com/demo_experience_bucket/thumbnails/thumb%20video%20format%20%281%29.jpg",
        "vimeo": "https://player.vimeo.com/video/1084059527?share=copy"
    },
    {
        "title": "White Label",
        "description": "Customize the look and feel of the LMS to reflect your brand identity.",
        "url": "https://storage.googleapis.com/demo_experience_bucket/thumbnails/thumb%20discussions.jpg",
        "vimeo": "https://player.vimeo.com/video/1082957515?share=copy"
    },
    {
        "title": "Zoom and Google Meets",
        "description": "Connect live training through integrated Zoom or Google Meet sessions.",
        "url": "https://storage.googleapis.com/demo_experience_bucket/thumbnails/thumb%20zoom%20%281%29.jpg",
        "vimeo": "https://player.vimeo.com/video/1082566757?share=copy"
    }
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
        print("GPT raw output:", content)  # log GPT output

        result = json.loads(content)
        print("Parsed result:", result)

        recommended_titles = result.get("recommended_videos", [])
        explanation = result.get("response", "")

        print("GPT recommended titles:", recommended_titles)

        matched_videos = [
            video for video in demo_videos
            if video["title"].strip().lower() in [t.strip().lower() for t in recommended_titles]
        ]

        print("Matched videos:", matched_videos)

        return jsonify({
            "recommended_videos": matched_videos,
            "demo_assistant_response": explanation
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/expand-array", methods=["POST"])
def expand_array():
    data = request.json
    raw = data.get("selected_titles")
    try:
        selected_titles = json.loads(raw)
    except Exception:
        return jsonify({"error": "Failed to parse selected_titles"}), 400

    matched_videos = [
        video for video in demo_videos
        if video["title"].strip().lower() in [t.strip().lower() for t in selected_titles]
    ]

    return jsonify({"carousel_cards": matched_videos})
