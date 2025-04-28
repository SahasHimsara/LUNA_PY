import sqlite3

# Create a connection to SQLite database (this will create the database file if it doesn't exist)
conn = sqlite3.connect('chat_data.db')  # This will create the file in your working directory
cursor = conn.cursor()

# Create chat_data table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS chat_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT NOT NULL,         
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

''')


# Insert some sample chat data
sample_data = [

     ("Good morning", " Good morning "),
    ("Hi", "Hiiiiiiiii"),
    ("How are you?", "I’m doing great, thanks for asking!"),
    ("Hello!", "Hey there!"),
    ("What’s up?", "Not much, how about you?"),
    ("Good afternoon", "Hope your day’s going well!"),
    ("Morning!", "Rise and shine!"),
    ("How’s it going?", "All good, how about you?"),
    ("Hey!", "Yo!"),
    ("Hi there", "Hello, how’s your day?"),
    ("What’s happening?", "Just chilling, how about you?"),
    ("Good night", "Sweet dreams!"),
    ("Good evening", "Good to see you!"),
    ("What’s new?", "Not much, just relaxing!"),
    ("Howdy!", "Hey, how’s everything?"),
    ("How’s your day?", "Pretty good, thanks for asking!"),
    ("Yo!", "What’s up, my friend?"),
    ("Hiya!", "Hello there!"),
    ("Greetings!", "Salutations!"),
    ("Long time no see!", "I know, it’s been a while!"),
    ("What’s going on?", "Not much, just enjoying the day!"),
    ("Morning sunshine!", "Good morning, starshine!"),
    ("I'm feeling really down today.", "I'm sorry to hear that. Want to talk about it?"),
    ("I just got some good news!", "That's amazing! What's the good news?"),
    ("I'm feeling really anxious.", "It’s okay to feel that way. Would you like some tips on how to relax?"),
    ("I’m excited about this weekend!", "That sounds fun! What’s planned for the weekend?"),
    ("I'm so stressed out with work.", "I totally understand. Maybe we could talk through it and find a way to manage?"),
    ("I’m having a great day!", "That's awesome! What made your day so great?"),
    ("I'm feeling lonely lately.", "I’m really sorry you're feeling that way. I’m here to talk if you want."),
    ("I can’t stop thinking about the past.", "It’s tough when that happens. Have you tried focusing on the present moment?"),
    ("I’m overwhelmed with everything.", "Take it one step at a time. You don’t have to do it all at once."),
    ("I’m in a really good mood today!", "That’s fantastic! What’s making you feel so positive?"),
    ("I feel so tired today.", "Maybe you need some rest. Take care of yourself!"),
    ("I’m really proud of what I accomplished today.", "That’s awesome! Celebrate your success!"),
    ("I’m feeling a bit lost.", "It’s okay to feel that way sometimes. Do you want to talk it through?"),
    ("I’m really excited for the holidays.", "That sounds wonderful! Do you have anything special planned?"),
    ("I feel like everything is going wrong.", "I’m so sorry you're going through that. Is there something I can do to help?"),
    ("I just need some time to myself.", "That’s completely understandable. Take the time you need."),
    ("I’m really grateful for today.", "That’s great to hear! What are you grateful for?"),
    ("I’m nervous about the future.", "It’s normal to feel that way. Have you thought about how you can plan for it?"),
    ("I’m feeling so overwhelmed by everything.", "One step at a time, you’ve got this. Want to talk about what’s on your mind?"),
    ("I’m feeling great today!", "That’s awesome! What’s making your day so good?"),
    ("I’ve been feeling really disconnected lately.", "That can be tough. Have you considered reaching out to someone you trust?"),
    ("I’m worried about tomorrow.", "It’s okay to be concerned. Maybe preparing for it will ease your mind."),
    ("I’m feeling really motivated right now!", "That’s amazing! What’s driving your motivation today?"),
    ("I’ve been so busy lately.", "It sounds like you’ve got a lot going on. How are you managing all of it?"),
    ("I feel like everything is in chaos.", "Take a deep breath, you can handle this. What’s the first step you can take?"),
    ("I’m feeling a little discouraged.", "I’m sorry to hear that. Do you want to share what’s on your mind?"),
    ("I’m feeling hopeful about the future.", "That’s wonderful! What’s making you feel so hopeful?"),
    ("I’m feeling really happy today!", "That’s fantastic! What’s making you feel so happy?"),
    ("I feel like I’m stuck in a rut.", "It happens to the best of us. Maybe a change of routine could help?"),
    ("I’m feeling so grateful today.", "That’s a beautiful feeling. What are you grateful for?"),
    ("I’m really proud of myself for making progress.", "That’s awesome! Every step forward counts."),
    ("I’m really nervous about this presentation.", "It’s normal to feel nervous. You’ve got this, just take a deep breath!"),
    ("I’m feeling very positive about everything.", "That’s great to hear! What’s making you feel so positive?"),
    ("I’m feeling a bit confused.", "That’s okay. Sometimes talking it through can help. What’s confusing you?"),
    ("I’m feeling like I need a break.", "It’s important to take breaks. Go ahead and recharge."),
    ("I’m really upset about what happened.", "I’m sorry that you’re upset. Want to talk about it?"),
    ("I’m feeling so much better today.", "That’s great! What made today better?"),
    ("I’m feeling a little anxious about the future.", "That’s completely normal. Do you want to talk about your worries?"),
    ("I’m feeling so motivated to work out.", "That’s fantastic! What kind of exercise are you thinking of doing?"),
    ("I’m feeling a bit overwhelmed by everything.", "That’s understandable. Is there something specific you’re worried about?"),
    ("I’m really proud of what I’ve achieved so far.", "That’s awesome! Celebrate your progress, no matter how small."),
    ("I feel really calm today.", "That’s wonderful! What do you think helped you feel so calm?"),
    ("I’m feeling really down about this situation.", "I’m so sorry you're feeling that way. Want to talk about it?"),
    ("I feel like things are finally turning around.", "That’s great to hear! What’s changed for the better?"),
    ("I’m feeling overwhelmed with work.", "Take a deep breath. What part of your work is overwhelming?"),
    ("I’m feeling pretty excited right now.", "That’s great! What’s got you feeling so excited?"),
    ("I’m feeling really tired.", "Maybe you should get some rest. You deserve it!"),
    ("I feel like I’m in a slump.", "That can happen. What’s been on your mind lately?"),
    ("I’m feeling so much anxiety right now.", "I’m sorry to hear that. Have you tried any relaxation techniques?"),
    ("I’m feeling a bit better today.", "That’s good to hear! What helped you feel better?"),
    ("I’m feeling really proud of myself today.", "That’s awesome! What did you accomplish?"),
    ("I’m feeling a little lonely.", "I’m really sorry to hear that. I’m here to talk if you need me."),
    ("I’m so excited about this opportunity.", "That’s fantastic! What’s the opportunity?"),
    ("I’m feeling like I can conquer anything right now.", "That’s amazing! Keep that positive energy going."),
    ("I’m feeling really nervous about the exam.", "It’s normal to feel nervous. Do you have a study plan in place?"),
    ("I’m feeling really grateful today.", "That’s great! What are you feeling grateful for?"),
    ("I’m feeling like I’ve made some progress.", "That’s wonderful! Celebrate your progress, no matter how small."),
    ("I feel really connected to myself today.", "That’s beautiful! What made you feel that way?"),
    ("I’m feeling really sad right now.", "I’m so sorry to hear that. Do you want to talk about it?"),
    ("I’m feeling so stressed out.", "I’m here if you want to talk. Stress can be tough to manage."),
    ("I’m feeling like I’m getting stronger.", "That’s fantastic! Keep building on that strength."),
    ("I’m feeling a little bit unsure about things.", "It’s okay to feel uncertain. Would you like to talk it through?"),
    ("I’m feeling really happy today.", "That’s awesome! What’s making you feel so happy?"),
    ("I’m feeling a bit stuck in life.", "I’m sorry you're feeling that way. Maybe we can brainstorm some ideas."),
    ("I’m feeling like I need a change.", "It’s okay to want change. What kind of change are you thinking about?"),
    ("I’m feeling really good today.", "That’s great to hear! What’s making your day so good?"),
    ("I’m feeling a little overwhelmed.", "I understand. Is there anything in particular that’s overwhelming you?"),
    ("I’m feeling pretty motivated.", "That’s awesome! What’s motivating you today?"),
    ("I’m feeling really anxious about everything.", "It’s okay to feel that way. Maybe we can figure out how to manage the anxiety."),
    ("I’m feeling really relaxed.", "That’s wonderful! What helped you relax today?"),
    ("I’m feeling a little sad today.", "I’m really sorry you’re feeling that way. Want to talk about it?"),
    ("I’m feeling really excited for the future.", "That’s amazing! What’s making you excited?"),
    ("I’m feeling so thankful for today.", "That’s great! What are you thankful for?"),
    ("I’m feeling pretty good today.", "That’s awesome! Anything in particular that’s making you feel good?"),
    ("I’m feeling really calm today.", "That’s great! What do you think contributed to that calm feeling?"),
    ("I’m feeling so much more confident.", "That’s wonderful! Confidence can really make a difference."),
    ("I’m feeling really stressed about work.", "I understand. Want to share what’s stressing you out?"),
    ("I’m feeling like I need a break.", "Take a breather. Rest is important."),
    ("I’m feeling a little uneasy.", "I’m sorry to hear that. Want to talk about what’s making you uneasy?"),
    ("I’m feeling pretty good today.", "That’s great! What’s making your day so good?"),
    ("I’m feeling really optimistic.", "That’s fantastic! What’s giving you that optimism?"),
    ("I’m feeling a bit tired.", "Maybe a quick nap would help! Take care of yourself."),
    ("I’m feeling really energized!", "That’s awesome! What’s got you feeling so energized?"),
    ("my cat is sick","I'm sorry to hear that. How old is your cat?"),
    ("she is five","Five years is still young! Hope she feels better soon."),
    ("she is not eating","Maybe you should see a vet if she continues not eating."),
    ("I’m feeling really proud of what I’ve done today.", "That’s amazing! Every accomplishment counts."),
    ("I’m feeling so happy today!", "That’s fantastic! What’s making you feel so happy?")
                

]

cursor.executemany('''
INSERT INTO chat_data (user_message, bot_response)
VALUES (?, ?)
''', sample_data)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database created and sample data inserted successfully.")


def fetch_all_data():
    conn = sqlite3.connect('chat_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM chat_data')
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()

# Example usage
fetch_all_data()