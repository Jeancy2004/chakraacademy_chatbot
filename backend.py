from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/chat', methods=['POST'])
def chat():

    data = request.get_json()

    msg = data.get('message', '').lower()

    print("MESSAGE RECEIVED:", msg)

    if "course" in msg:
        reply = "We offer NEET coaching courses."

    elif "fee" in msg:
        reply = "Fees start from ₹10,000."

    elif "timing" in msg:
        reply = "Morning & Evening batches available."

    elif "placement" in msg:
        reply = "Yes, placement support available."

    elif "contact" in msg:
        reply = "You can contact us at https://chakraacademy.in/"

    elif "hello" in msg or "hi" in msg:
        reply = "Hello! How can I assist you today?"

    elif "வகுப்பு" in msg:
        reply = "நாங்கள் NEET பயிற்சி வகுப்புகளை வழங்குகிறோம்."

    elif "கட்டணம்" in msg or "kattanam" in msg:
        reply = "கட்டணங்கள் ₹10,000 முதல் தொடங்குகிறது."

    elif "நேரம்" in msg:
        reply = "காலை மற்றும் மாலை வகுப்புகள் கிடைக்கின்றன."

    elif "தொடர்பு" in msg:
        reply = "நீங்கள் எங்களை https://chakraacademy.in/ இல் தொடர்பு கொள்ளலாம்."

    else:
        reply = "Ask about courses, fees, timings, contact."

    return jsonify({"reply": reply})


if __name__ == '__main__':
    app.run(debug=True)