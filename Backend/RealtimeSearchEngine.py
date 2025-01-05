# Import required libraries and modules
from googlesearch import search  # Used for performing Google searches
from groq import Groq  # Groq client for AI-based chat completions
from json import load, dump  # For reading and writing JSON files
import datetime  # For fetching current date and time
from dotenv import dotenv_values  # For loading environment variables from a .env file

# Load environment variables from .env file
env_vars = dotenv_values(".env")

# Retrieve specific environment variables for username, assistant name, and API key
Username = env_vars.get("Username")  # Username of the user
Assistantname = env_vars.get("Assistantname")  # Name of the AI assistant
GroqAPIKey = env_vars.get("GroqAPIKey")  # API key for Groq client

# Initialize the Groq client with the API key
client = Groq(api_key=GroqAPIKey)

# System message to define the AI assistant's behavior and tone
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***
"""

# Attempt to load chat logs from a file, or create a new file if it doesn't exist
try:
    with open(r"Data\ChatLog.json", "r") as f:
        try:
            messages = load(f)  # Load chat messages from the file
        except json.JSONDecodeError:
            messages = []  # Initialize an empty list if the file is invalid
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)  # Create an empty JSON file

# Function to perform a Google search and format results
def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))  # Perform the search
    Answer = f"The search results for '{query}' are:\n[start]\n"
    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"
    Answer += "[end]"
    return Answer

# Function to clean up and format the AI assistant's response
def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]  # Remove empty lines
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer

# System-level messages for initializing the chatbot
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

# Function to get the current date and time information
def Information():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    # Return formatted real-time information
    data = f"Please use this real-time information if needed,\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours:{minute} minutes:{second} seconds\n"
    return data

# Function to interact with the AI system and return responses
def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    # Load existing chat messages
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)

    # Add the user's query to the chat log
    messages.append({"role": "user", "content": f"{prompt}"})
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

    # Generate a response using the Groq client
    completion = client.chat.completions.create(
        model="llama3-70b-8192",  # Model for chatbot
        messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        max_tokens=2048,  # Maximum token limit for response
        temperature=0.7,  # Controls response creativity
        top_p=1,  # Nucleus sampling
        stream=True,  # Enables streaming responses
        stop=None  # No explicit stopping condition
    )

    Answer = ""

    # Build the answer from the streamed chunks
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    # Remove unwanted tags
    Answer = Answer.replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})

    # Save updated chat log
    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

    SystemChatBot.pop()  # Remove the latest system message
    return AnswerModifier(Answer=Answer)

# Main script for running the chatbot
if __name__ == "__main__":
    while True:
        user = input(">>> Enter Your Query: ")  # Prompt the user for input
        print(RealtimeSearchEngine(user))  # Generate and display the chatbot's response
