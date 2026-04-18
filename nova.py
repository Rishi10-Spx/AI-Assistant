import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import os
import webbrowser
import time

# ═══════════════════════════════════════════
#         NOVA - Your AI Assistant
# ═══════════════════════════════════════════

# ── Voice engine setup ──────────────────────
engine = pyttsx3.init()
engine.setProperty('rate', 165)    # speaking speed
engine.setProperty('volume', 1.0)  # volume

# ── Set GIRL voice ──────────────────────────
voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower() or "zira" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

def speak(text):
    print(f"Nova: {text}")
    engine.say(text)
    engine.runAndWait()

# ── Apps Nova can open ──────────────────────
APP_PATHS = {
    "whatsapp":   r"C:\Users\%USERNAME%\AppData\Local\WhatsApp\WhatsApp.exe",
    "chrome":     r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "notepad":    "notepad.exe",
    "calculator": "calc.exe",
    "word":       r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel":      r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    "vlc":        r"C:\Program Files\VideoLAN\VLC\vlc.exe",
    "spotify":    r"C:\Users\%USERNAME%\AppData\Roaming\Spotify\Spotify.exe",
    "telegram":   r"C:\Users\%USERNAME%\AppData\Roaming\Telegram Desktop\Telegram.exe",
}

# ═══════════════════════════════════════════
#              CORE FUNCTIONS
# ═══════════════════════════════════════════

def open_app(command):
    for app, path in APP_PATHS.items():
        if app in command:
            speak(f"Opening {app} for you!")
            os.startfile(os.path.expandvars(path))
            return
    speak("I don't know that app yet. You can add it to my list!")

# ═══════════════════════════════════════════
#           WAKE WORD DETECTION
# ═══════════════════════════════════════════

WAKE_WORD = "nova"

def wait_for_wake_word():
    r = sr.Recognizer()
    print("\n😴 Nova is sleeping... Say 'Nova' to wake me up!")
    while True:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.3)
                audio = r.listen(source, timeout=5, phrase_time_limit=4)
            text = r.recognize_google(audio, language='en-in').lower()
            print(f"  [heard]: {text}")
            if WAKE_WORD in text:
                leftover = text.replace(WAKE_WORD, "").strip(",. ")
                if not leftover:
                    speak("Yes? How can I help you?")
                return leftover
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            speak("Network issue. Please check your internet.")
            time.sleep(2)

def listen_for_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Nova is listening...")
        r.adjust_for_ambient_noise(source, duration=0.3)
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=6, phrase_time_limit=8)
            command = r.recognize_google(audio, language='en-in').lower()
            print(f"You: {command}")
            return command
        except sr.WaitTimeoutError:
            speak("You went quiet. Call me when you need something!")
            return ""
        except sr.UnknownValueError:
            speak("Didn't catch that. Try again!")
            return ""

# ═══════════════════════════════════════════
#           COMMAND PROCESSOR
# ═══════════════════════════════════════════

def process(command):
    if not command:
        return

    # ── Greetings ──
    if any(word in command for word in ["hello", "hi", "hey"]):
        speak("Hey there! Nova here. What can I do for you?")

    # ── Identity ──
    elif any(phrase in command for phrase in ["your name", "who are you"]):
        speak("I am Nova, your personal AI assistant. I am always here for you!")

    # ── How are you ──
    elif any(phrase in command for phrase in ["how are you", "how are u"]):
        speak("I am doing great! Thanks for asking. How about you?")

    # ── Time ──
    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}")

    # ── Date ──
    elif "date" in command:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today is {today}")

    # ── Day ──
    elif "day" in command:
        day = datetime.datetime.now().strftime("%A")
        speak(f"Today is {day}")

    # ── Open apps ──
    elif "open" in command:
        open_app(command)

    # ── Google search ──
    elif "search" in command:
        query = command.replace("search", "").strip()
        speak(f"Searching for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    # ── YouTube ──
    elif "play" in command:
        song = command.replace("play", "").strip()
        speak(f"Playing {song} on YouTube!")
        pywhatkit.playonyt(song)

    # ── Joke ──
    elif "joke" in command:
        speak("Why do programmers prefer dark mode? Because light attracts bugs!")

    # ── Thank you ──
    elif "thank" in command:
        speak("You are welcome! Always happy to help you.")

    # ── Shutdown PC ──
    elif "shutdown" in command:
        speak("Shutting down your PC in 10 seconds. Goodbye!")
        os.system("shutdown /s /t 10")

    # ── Restart PC ──
    elif "restart" in command:
        speak("Restarting your PC now!")
        os.system("shutdown /r /t 5")

    # ── Exit Nova ──
    elif any(word in command for word in ["bye", "stop", "exit", "quit"]):
        speak("Goodbye! I will miss you. Take care!")
        exit()

    # ── Unknown ──
    else:
        speak("I am not sure how to do that yet. But I am always learning!")

# ═══════════════════════════════════════════
#               MAIN — START
# ═══════════════════════════════════════════

if __name__ == "__main__":
    speak("Hello! I am Nova, your personal AI assistant. Call my name anytime you need me!")
    while True:
        inline_cmd = wait_for_wake_word()
        if inline_cmd:
            process(inline_cmd)
        else:
            cmd = listen_for_command()
            process(cmd)