from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

# Load environment variables from .env file
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

# User agent for HTTP requests
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

# Default chatbot system message
SystemChatBot = [
    {"role": "system", "content": f"Hello, I am {os.environ.get('Username')}. You are a content writer tasked with creating various types of content like letters, codes, applications, essays, songs, and poems."}
]

# Predefined professional responses
professional_responses = [
    "Thank you for reaching out. How can I assist you today?",
    "I understand your concern. Let me look into it and provide a solution.",
    "Your feedback is valuable to us. We’ll use it to improve our services.",
    "I appreciate your patience while I address your request.",
    "I’ve noted your requirements and will get back to you with the next steps shortly.",
    "If you have any additional questions, please don’t hesitate to ask.",
    "Could you please provide more details to help me better understand your needs?",
    "Thank you for bringing this to our attention. We’re working to resolve it promptly.",
    "I will ensure this is escalated to the appropriate team for a quick resolution.",
    "It was a pleasure assisting you. Let me know if you need further help."
]

# Function to perform a Google search
def GoogleSearch(topic):
    search(topic)
    return True

# Function to generate content and save it to a text file
def Content(topic):
    def OpenNotepad(file):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, file])

    def ContentWriteAI(prompt):
        messages = [{"role": "user", "content": f"{prompt}"}]
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True
        )
        answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content

        answer = answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": answer})
        return answer

    topic = topic.replace("Content ", "")
    content_by_ai = ContentWriteAI(topic)

    file_path = rf"Data\{topic.lower().replace(' ', '')}.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content_by_ai)
    OpenNotepad(file_path)
    return True

# Function to search YouTube
def YouTubeSearch(topic):
    url = f"https://www.youtube.com/results?search_query={topic}"
    webbrowser.open(url)
    return True

# Function to play a YouTube video
def PlayYouTube(query):
    playonyt(query)
    return True

# Function to open an application
def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except Exception:
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {'jsname': 'UWckNb'})
            return [link.get('href') for link in links]

        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": user_agent}
            response = sess.get(url, headers=headers)
            return response.text if response.status_code == 200 else None

        html = search_google(app)
        if html:
            links = extract_links(html)
            if links:
                webopen(links[0])
        return True

# Function to close an application
def CloseApp(app):
    if "chrome" in app:
        return False
    try:
        close(app, match_closest=True, output=True, throw_error=True)
        return True
    except Exception:
        return False

# Function to handle system commands
def System(command):
    actions = {
        "mute": lambda: keyboard.press_and_release("volume mute"),
        "unmute": lambda: keyboard.press_and_release("volume mute"),
        "volume up": lambda: keyboard.press_and_release("volume up"),
        "volume down": lambda: keyboard.press_and_release("volume down")
    }
    action = actions.get(command)
    if action:
        action()
    return True

# Main function for executing commands
async def TranslateAndExecute(commands):
    funcs = []
    for command in commands:
        if command.startswith("open "):
            funcs.append(asyncio.to_thread(OpenApp, command.removeprefix("open ")))
        elif command.startswith("close "):
            funcs.append(asyncio.to_thread(CloseApp, command.removeprefix("close ")))
        elif command.startswith("play "):
            funcs.append(asyncio.to_thread(PlayYouTube, command.removeprefix("play ")))
        elif command.startswith("content "):
            funcs.append(asyncio.to_thread(Content, command.removeprefix("content ")))
        elif command.startswith("google search "):
            funcs.append(asyncio.to_thread(GoogleSearch, command.removeprefix("google search ")))
        elif command.startswith("youtube search "):
            funcs.append(asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search ")))

    results = await asyncio.gather(*funcs)
    for result in results:
        yield result

# Main function for automation
async def Automation(commands):
    async for result in TranslateAndExecute(commands):
        pass
    return True

if __name__ == "__main__":
    pass
