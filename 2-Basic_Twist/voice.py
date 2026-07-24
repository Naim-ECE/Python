import pyttsx3
import os
engine = pyttsx3.init()
engine.say("Hello, I am your voice assistant.")
engine.runAndWait()

directory_path = "/Front and Back"
contents = os.listdir(directory_path)

for item in contents:
    print(item)
