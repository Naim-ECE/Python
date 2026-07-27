import pyttsx3
import os
engine = pyttsx3.init()
engine.say("Hello, I am your voice assistant.")
engine.runAndWait()

directory_path = "/Front and Back/Git/PYTHON/2-Basic_Twist"
contents = os.listdir(directory_path)

voices = engine.getProperty('voices')

# Set voice to female (index 1 usually represents female)
engine.setProperty('voice', voices[1].id)

# Text to be spoken
engine.say("Hello, this is a female voice.")

# Process and play the speech
engine.runAndWait()


for item in contents:
    print(item)
