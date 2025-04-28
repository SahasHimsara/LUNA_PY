from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import sqlite3
import re

app = Flask(__name__)
CORS(app)

# Preprocess the text (lowercase, remove punctuation)
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

# Get the last n user messages
def get_last_user_messages(n=3):
    conn = sqlite3.connect('chat_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT message FROM chat_history
        WHERE sender = 'user'
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (n,))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows[::-1]]  # Reverse to keep oldest to newest

# Generate AI Response
from sentence_transformers import SentenceTransformer, util

# Load the model once at the top (Global)
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_ai_response(user_input):
    conn = sqlite3.connect('chat_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT user_message, bot_response FROM chat_data')
    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return random.choice([
            "I'm not sure how to respond to that. Can you ask something else?",
            "Hmm, I didn’t quite get that. Want to try rephrasing?",
            "Interesting… but I’m not sure how to reply just yet!"
        ])

    # Prepare corpus (all previous user_messages)
    corpus_messages = [row[0] for row in rows]
    corpus_embeddings = model.encode(corpus_messages, convert_to_tensor=True)

    # Embed the new user input
    user_embedding = model.encode(user_input, convert_to_tensor=True)

    # Compute cosine similarity
    scores = util.cos_sim(user_embedding, corpus_embeddings)[0]

    # Get the best match
    best_score_idx = scores.argmax().item()
    best_score = scores[best_score_idx]

    if best_score > 0.5:  # threshold (0.5 = 50%)
        return rows[best_score_idx][1]  # return corresponding bot_response
    else:
        return random.choice([
            "I'm not sure how to respond to that. Can you ask something else?",
            "Hmm, I didn’t quite get that. Want to try rephrasing?",
            "Interesting… but I’m not sure how to reply just yet!"
        ])

# Route for chatting
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')

    if user_message:
        conn = sqlite3.connect('chat_data.db')
        cursor = conn.cursor()

        # Save user message
        cursor.execute('''
            INSERT INTO chat_history (sender, message)
            VALUES (?, ?)
        ''', ('user', user_message))
        conn.commit()

        # Generate bot response
        ai_response = generate_ai_response(user_message)

        # Save bot response
        cursor.execute('''
            INSERT INTO chat_history (sender, message)
            VALUES (?, ?)
        ''', ('bot', ai_response))
        conn.commit()

        conn.close()

        return jsonify({"response": ai_response}), 200
    else:
        return jsonify({"error": "Message is empty!"}), 400

# Route to get chat history
@app.route('/history', methods=['GET'])
def get_history():
    conn = sqlite3.connect('chat_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT sender, message, timestamp
        FROM chat_history
        ORDER BY timestamp ASC
    ''')
    rows = cursor.fetchall()

    history = [{"sender": row[0], "message": row[1], "timestamp": row[2]} for row in rows]

    conn.close()

    return jsonify(history), 200

# Main entry point
if __name__ == '__main__':
    app.run(debug=True)
