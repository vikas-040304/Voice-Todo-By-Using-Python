import speech_recognition as sr # type: ignore
import pyttsx3 # type: ignore
import sqlite3

# Initialize recognizer and voice engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Speak function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Listen function
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        return command.lower()
    except:
        speak("Sorry, I didn't catch that.")
        return ""

# Set up database
conn = sqlite3.connect("todo.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)''')
conn.commit()

# Add task
def add_task(task):
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    speak(f"Task '{task}' added.")

# List tasks
def list_tasks():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    if tasks:
        speak("Here are your tasks:")
        for i, (id, task) in enumerate(tasks):
            speak(f"{i+1}. {task}")
    else:
        speak("Your to-do list is empty.")

# Delete task
def delete_task(task_name):
    cursor.execute("DELETE FROM tasks WHERE task LIKE ?", ('%' + task_name + '%',))
    conn.commit()
    speak(f"Task '{task_name}' deleted.")

# Main loop
def main():
    speak("Welcome to your voice-controlled to-do list.")
    while True:
        speak("What do you want to do? Say add, list, delete or quit.")
        command = listen()
        if "add" in command:
            speak("What task do you want to add?")
            task = listen()
            if task:
                add_task(task)
        elif "list" in command:
            list_tasks()
        elif "delete" in command:
            speak("Which task should I delete?")
            task_name = listen()
            if task_name:
                delete_task(task_name)
        elif "quit" in command or "exit" in command:
            speak("Goodbye!")
            break
        else:
            speak("Please say add, list, delete or quit.")

# Run the app
if __name__ == "__main__":
    main()
