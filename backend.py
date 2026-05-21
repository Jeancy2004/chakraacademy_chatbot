from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="mysql.railway.internal",
        user="root",
        password="slAVRpPALeXBSWyfxAzakwaOEJmTpfjV",
        database="railway",
        port=3306
    )

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/chat', methods=['POST'])
def chat():

    db = get_db()
    cursor = db.cursor()

    msg = request.json.get('message', '').lower()

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
    else:
        reply = "Ask about courses, fees, timings, contact."
    if "hello" in msg or "hi" in msg:
        reply = "Hello! How can I assist you today?"
    if "வகுப்பு" in msg :
        reply = "நாங்கள் NEET பயிற்சி வகுப்புகளை வழங்குகிறோம்."
    if "கட்டணம்" in msg or "kattanam" in msg:
        reply = "கட்டணங்கள் ₹10,000 முதல் தொடங்குகிறது."
    if "நேரம்" in msg:
        reply = "காலை மற்றும் மாலை வகுப்புகள் கிடைக்கின்றன."
    if "தொடர்பு" in msg:
        reply = "நீங்கள் எங்களை https://chakraacademy.in/ இல் தொடர்பு கொள்ளலாம்."

    sql = "INSERT INTO chats(user_message, bot_reply) VALUES(%s, %s)"
    val = (msg, reply)

    cursor.execute(sql, val)
    db.commit()

    cursor.close()
    db.close()

    return jsonify({"reply": reply})


if __name__ == '__main__':
    app.run(debug=True)