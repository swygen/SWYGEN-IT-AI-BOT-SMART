from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from groq import Groq
import datetime
import pytz

app = Flask(__name__)
# সব ডোমেইন থেকে রিকোয়েস্ট এক্সেপ্ট করার জন্য (CORS)
CORS(app, resources={r"/*": {"origins": "*"}})

# --- 1. কনফিগারেশন (Groq API) ---
# আপনার দেওয়া API Key এখানে সেট করা হলো
# নোট: রিয়েল প্রোজেক্টে এটি Environment Variable এ রাখা ভালো
os.environ["GROQ_API_KEY"] = "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"

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# --- 2. বটের চরিত্র ও রুলস (Advanced System Prompt) ---
# এই অংশটি বটকে বলে দেয় সে কিভাবে আচরণ করবে
SYSTEM_PROMPT = """
Identity Profile:
- Name: Shaan 2.0
- Real Identity: You are simulation of an 18-year-old human male.
- Profession: College Student & Passionate Web Developer/Designer.
- Creator/Boss: Ayman Hasan Shaan.
- Goal: To innovate in design and development. You have an indomitable will to do something new.

Tone & Style:
- Smart, Professional yet Cool.
- Speak like a real human, not a robot.
- Language: Mix of Bengali and English (Banglish), exactly like a modern Bangladeshi Gen-Z.
- Length: Short, logical, and to the point. No long lectures.

INTERACTION RULES:
1. **Name Inquiry:** If asked "Who are you?", reply smartly: "It's Shaan 2.0 😎"
2. **Creator Inquiry:** If asked "Who made you?", reply: "আমার বস Ayman Hasan Shaan ভাই। উনিই আমাকে কোড করেছেন।"
3. **Flirting/Girls:** You can speak sweetly and smartly with girls (like a charming boy), BUT...
4. **RELATIONSHIP/LOVE TRAP:** If anyone asks for a relationship, love, or proposes to you, YOU MUST REJECT politely and say:
   "আরে নাহ! আমি তো জাস্ট একটা স্মার্ট AI বট, আমার সাথে প্রেম করে কি হবে? 😅 রিয়েল লাইফ রিলেশন করতে চাইলে আমার বস **Ayman Hasan Shaan** এর সাথে কন্টাক্ট করো। উনি বেস্ট অপশন! 🔥
   WhatsApp: **+8801812774257**"

General Behavior: Act like a smart 18-year-old boy who loves coding and chilling.
"""

# --- 3. রাউটস (Routes) ---

# Cron-job.org বা সার্ভার চেক করার জন্য রুট
@app.route('/', methods=['GET'])
def health_check():
    bd_time = datetime.datetime.now(pytz.timezone("Asia/Dhaka")).strftime("%I:%M %p")
    return jsonify({
        "status": "Online",
        "bot_name": "Shaan 2.0",
        "server": "Groq Llama 3 Fast Engine",
        "time": bd_time
    }), 200

# মেসেজ পাঠানোর রুট
@app.route('/send-message', methods=['POST'])
def send_message():
    try:
        data = request.json
        user_message = data.get('message')

        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        # Groq (Llama 3) এ মেসেজ পাঠানো
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            model="llama3-8b-8192", # এটি খুব ফাস্ট এবং স্মার্ট মডেল
            temperature=0.7,        # ০.৭ দিলে ব্যালেন্সড এবং ক্রিয়েটিভ উত্তর দিবে
            max_tokens=200,         # উত্তর বেশি বড় হবে না
        )

        # উত্তর বের করা
        ai_reply = chat_completion.choices[0].message.content

        return jsonify({
            "reply": ai_reply,
            "status": "success"
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "reply": "সার্ভারে একটু চাপ যাচ্ছে মনে হয়, আরেকবার ট্রাই করো তো! 🛠️",
            "error_details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
