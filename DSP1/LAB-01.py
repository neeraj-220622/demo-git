import random
import datetime
import string

# ---------------- MEMORY ----------------
user_name = None
STOP_WORDS = {"is", "the", "a", "an", "of", "to", "in", "on", "for", "what", "who"}

def load_memory():
    memory = []
    try:
        with open("chatbot_memory.txt", "r", encoding="utf-8") as file:
            for line in file:
                if "|" in line:
                    question, answer = line.strip().split("|", 1)
                    key_set = set(question.split())
                    memory.append((key_set, answer))
    except FileNotFoundError:
        pass
    return memory


def save_memory(question, answer):
    with open("chatbot_memory.txt", "a", encoding="utf-8") as file:
        file.write(f"{question}|{answer}\n")


learned_responses = load_memory()

# ---------------- BASIC FUNCTIONS ----------------
def greet():
    hour = datetime.datetime.now().hour
    if hour < 12:
        msg = "Good morning"
    elif hour < 17:
        msg = "Good afternoon"
    else:
        msg = "Good evening"

    print(f"Chatbot: {msg}! 👋")
    print("Chatbot: Talk to me freely. Type 'bye' to exit.\n")


def clean_text(text):
    text = text.lower()
    for ch in string.punctuation:
        text = text.replace(ch, "")
    return text


def tell_joke():
    jokes = [
        "Why do programmers hate nature? Too many bugs 🐞",
        "Why did Python go to school? To improve its classes 😄",
        "Why was the computer cold? It forgot to close its Windows ❄️",
        "Why do Java developers wear glasses? Because they don't C# 😆"
    ]
    return random.choice(jokes)


def simple_calculator(text):
    try:
        expression = text.replace("calculate", "")
        result = eval(expression)
        return f"The result is {result}"
    except:
        return "I couldn't calculate that. Try again."

# ---------------- LEARNED MEMORY MATCHING ----------------
def match_learned(words):
    best_score = 0
    best_answer = None

    for key_set, answer in learned_responses:
        score = len(words & key_set)
        if score > best_score:
            best_score = score
            best_answer = answer

    return best_answer if best_score >= 1 else None


# ---------------- MAIN RESPONSE ENGINE ----------------
def get_response(user_input):
    global user_name

    user_input = clean_text(user_input)
    words = set(user_input.split()) - STOP_WORDS

    # 🔹 Check learned memory (keyword-based)
    learned_match = match_learned(words)
    if learned_match:
        return learned_match

    # 🔹 Predefined intents
    intents = {
        "greeting": {
            "keywords": {"hello", "hi", "hey", "hola"},
            "responses": ["Hello 😊", "Hi there 👋", "Hey! How can I help?"]
        },
        "how_are_you": {
            "keywords": {"how", "you"},
            "responses": ["I'm fine!", "Doing great 😄", "All good!"]
        },
        "name": {
            "keywords": {"your", "name"},
            "responses": ["I'm a Python chatbot 🤖"]
        },
        "help": {
            "keywords": {"help", "assist", "support"},
            "responses": ["You can chat, joke, calculate, or teach me new replies."]
        },
        "thanks": {
            "keywords": {"thanks", "thank"},
            "responses": ["You're welcome 😊", "No problem!", "Anytime!"]
        },
        "time": {
            "keywords": {"time"},
            "responses": [f"The time is {datetime.datetime.now().strftime('%H:%M:%S')}"]
        },
        "date": {
            "keywords": {"date", "day"},
            "responses": [f"Today's date is {datetime.datetime.now().strftime('%d-%m-%Y')}"]
        },
        "joke": {
            "keywords": {"joke", "funny", "laugh"},
            "responses": [tell_joke()]
        },
        "bye": {
            "keywords": {"bye", "exit", "quit"},
            "responses": ["Goodbye 👋", "See you soon!", "Bye! 😊"]
        }
    }

    # 🔹 Name memory
    if "my name is" in user_input:
        user_name = user_input.replace("my name is", "").title()
        return f"Nice to meet you, {user_name}! 😊"

    if "what is my name" in user_input:
        return f"Your name is {user_name}" if user_name else "I don't know your name yet."

    # 🔹 Calculator
    if "calculate" in user_input:
        return simple_calculator(user_input)

    # 🔹 Intent scoring
    best_score = 0
    best_response = None

    for intent in intents.values():
        score = len(words & intent["keywords"])
        if score > best_score:
            best_score = score
            best_response = random.choice(intent["responses"])

    if best_score > 0:
        return best_response

    # 🔹 Learning fallback (keyword-based)
    reply = input("Chatbot: I don't know that. Teach me a reply 👉 ")
    key_set = words

    learned_responses.append((key_set, reply))
    save_memory(" ".join(key_set), reply)

    return "Thanks! I learned it and saved it permanently 👍"


# ---------------- CHAT LOOP ----------------
def chatbot():
    greet()
    while True:
        user_input = input("You: ")
        response = get_response(user_input)
        print("Chatbot:", response)

        if "bye" in user_input.lower():
            break


# ---------------- START ----------------
chatbot()
