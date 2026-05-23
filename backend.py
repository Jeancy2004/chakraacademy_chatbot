from flask import Flask, render_template, request, jsonify
import mysql.connector
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "myverifytoken"

ACCESS_TOKEN = "EAAXybnFtTwUBRnojM9ZCNBAgRtLueOn7eZAJarjbEXMweKZB5akZA5RPFmAGsKvPh4XirMs8rPCC2qLps9m9mSIkVaA5kAVLUmafQHLYHD5KXmu4y8BMH6hbqY8LiQ5GfU41mkwHxKpRZCNN6sZBh1KmzBcqDYwh2mfv1KLywMxBvmZAbZC1cag4TVsBpY29JDwlbETfZBSsXUiZCv65bk1qcJHykciPGre2ty7AH2W8OLPTFxhPrFqt7pPdVUaxTPU4OuyOdZBNOZBn8C0wfgSXIihNRK3kbjPncq4Qzt8G"

PHONE_NUMBER_ID = "1159050887288007"


def get_db():
    return mysql.connector.connect(
        host="kodama.proxy.rlwy.net",
        user="root",
        password="slAVRpPALeXBSWyfxAzakwaOEJmTpfjV",
        database="railway",
        port=12638
    )


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/webhook', methods=['GET'])
def verify():

    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token:

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200

        else:
            return "Verification token mismatch", 403

    return "Webhook verified"

@app.route('/webhook', methods=['POST'])
def webhook():

    data = request.get_json()

    print(data)

    try:

        entry = data['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']

        if 'messages' in value:

            message = value['messages'][0]

            phone_number = message['from']
            msg = message['text']['body'].lower()

            print("MESSAGE RECEIVED:", msg)

            # CHATBOT REPLIES
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

            # SAVE CHAT TO DATABASE
            db = get_db()
            cursor = db.cursor()

            sql = "INSERT INTO chats(user_message, bot_reply) VALUES(%s, %s)"
            val = (msg, reply)

            cursor.execute(sql, val)
            db.commit()

            cursor.close()
            db.close()

            send_whatsapp_message(phone_number, reply)

    except Exception as e:
        print("ERROR:", e)

    return "ok", 200

def send_whatsapp_message(to, message):

    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": message
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    print(response.text)

@app.route('/chat', methods=['POST'])
def chat():

    try:

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

        sql = "INSERT INTO chats(user_message, bot_reply) VALUES(%s, %s)"
        val = (msg, reply)

        cursor.execute(sql, val)
        db.commit()

        cursor.close()
        db.close()

        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"reply": str(e)})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)