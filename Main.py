# Importing necessary modules and functions
from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetMicrophoneStatus,
    GetAssistantStatus,
)
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "Assistant")

# Default initial chat message
DefaultMessage = f'''{Username}: Hello {Assistantname}, How are you?
{Assistantname}: Welcome {Username}, I am doing well. How may I help you?'''

# Functions supported by the assistant
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

# Handle initial chat log setup
def ShowDefaultChatIfNoChats():
    try:
        with open(r'Data\ChatLog.json', "r", encoding='utf-8') as file:
            if len(file.read()) < 5:  # If the chat log is empty
                with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as db_file:
                    db_file.write("")
                with open(TempDirectoryPath('Response.data'), 'w', encoding='utf-8') as resp_file:
                    resp_file.write(DefaultMessage)
    except FileNotFoundError:
        print("Chat log file not found. Initializing default chat.")

# Read chat log from JSON
def ReadChatLogJson():
    try:
        with open(r'Data\ChatLog.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Error decoding chat log JSON.")
        return []

# Integrate chat log into the temporary database
def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"User: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"Assistant: {entry['content']}\n"
    formatted_chatlog = formatted_chatlog.replace("User", f"{Username}").replace("Assistant", f"{Assistantname}")
    with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

# Display chats on the GUI
def ShowChatsOnGUI():
    try:
        with open(TempDirectoryPath('Database.data'), 'r', encoding='utf-8') as file:
            data = file.read()
        if data.strip():
            with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
                file.write('\n'.join(data.splitlines()))
    except FileNotFoundError:
        print("Database file not found for GUI display.")

# Initial setup execution
def InitialExecution():
    SetMicrophoneStatus("True")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()

# Main execution logic
def MainExecution():
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""

    SetAssistantStatus("Listening ... ")
    Query = SpeechRecognition()
    ShowTextToScreen(f"{Username}: {Query}")
    SetAssistantStatus("Thinking ...")
    Decision = FirstLayerDMM(Query)

    print(f"\nDecision: {Decision}\n")

    GeneralQuery = any(d.startswith("general") for d in Decision)
    RealtimeQuery = any(d.startswith("realtime") for d in Decision)
    MergedQuery = " and ".join(" ".join(d.split()[1:]) for d in Decision if d.startswith("general") or d.startswith("realtime"))

    for queries in Decision:
        if "generate" in queries:
            ImageGenerationQuery = queries
            ImageExecution = True

        if not TaskExecution and any(queries.startswith(func) for func in Functions):
            run(Automation(list(Decision)))
            TaskExecution = True

    if ImageExecution:
        try:
            with open(r"Frontend\Files\ImageGeneration.data", "w") as file:
                file.write(f"{ImageGenerationQuery},True")
            subprocess.Popen(['python', r'Backend\ImageGeneration.py'], shell=False)
        except Exception as e:
            print(f"Error starting ImageGeneration.py: {e}")

    if GeneralQuery or RealtimeQuery:
        SetAssistantStatus("Searching ...")
        Answer = RealtimeSearchEngine(QueryModifier(MergedQuery))
        ShowTextToScreen(f"{Assistantname}: {Answer}")
        SetAssistantStatus("Answering ... ")
        TextToSpeech(Answer)
        return

    for query in Decision:
        if "general" in query:
            SetAssistantStatus("Thinking ...")
            Answer = ChatBot(QueryModifier(query.replace("general", "")))
            ShowTextToScreen(f"{Assistantname}: {Answer}")
            SetAssistantStatus("Answering ... ")
            TextToSpeech(Answer)
        elif "realtime" in query:
            SetAssistantStatus("Searching ...")
            Answer = RealtimeSearchEngine(QueryModifier(query.replace("realtime", "")))
            ShowTextToScreen(f"{Assistantname}: {Answer}")
            SetAssistantStatus("Answering ... ")
            TextToSpeech(Answer)
        elif "exit" in query:
            SetAssistantStatus("Exiting ...")
            os._exit(0)

# Thread for continuous task monitoring
def FirstThread():
    while True:
        if GetMicrophoneStatus() == "True":
            MainExecution()
        else:
            if "Available ..." not in GetAssistantStatus():
                SetAssistantStatus("Available ...")

# Thread for GUI operation
def SecondThread():
    GraphicalUserInterface()

# Main entry point
if __name__ == "__main__":
    thread2 = threading.Thread(target=FirstThread, daemon=True)
    thread2.start()
    SecondThread()
