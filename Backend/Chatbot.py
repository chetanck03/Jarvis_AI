# Import necessary libraries
from groq import Groq  # Import Groq for AI chatbot interaction
from json import load, dump  # For working with JSON files (loading and saving chat logs)
import datetime  # For working with dates and times
from dotenv import dotenv_values  # To load environment variables from a .env file
import json  # For handling JSON operations

# Load environment variables from .env file
env_vars = dotenv_values(".env")

# Retrieve specific environment variables for username, assistant name, and API key
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Groq client with the API key
client = Groq(api_key=GroqAPIKey)

# Initialize an empty list to store chat messages
messages = []

# Define the system message that will set the chatbot's behavior and constraints
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

# Define system-level chat message
SystemChatBot = [
    {"role": "system", "content": System}
]

# Try to load chat log from a file, if it doesn't exist, create an empty log
try:
    with open(r"Data\ChatLog.json", "r") as f:
        # Attempt to load messages from the file
        try:
            messages = load(f)
        except json.JSONDecodeError:
            messages = []  # Initialize an empty list if JSON is invalid
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)  # Create a new empty file if it doesn't exist

# Function to fetch real-time information like date and time
def RealTimeInformation():
    # Get the current date and time
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    # Format the real-time information for the output
    data = f"Please use this real time information if needed,\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours:{minute} minutes:{second} seconds\n"
    return data

# Function to clean and modify the chatbot's answer by removing empty lines
def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer

# Main function to interact with the chatbot and process user queries
def ChatBot(Query):
    try:
        # Load the chat log from the file
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)  # Load existing chat messages

        # Add user's query to the chat log
        messages.append({"role": "user", "content": f"{Query}"})

        # Send the query to Groq's chat API
        completion = client.chat.completions.create(
            model="llama-3.3-70b-specdec",  # Model to be used by the chatbot
            messages = SystemChatBot + [{"role": "system", "content": RealTimeInformation()}] + messages,  # Include system and chat history
            max_tokens=1204,  # Limit the length of the response
            temperature=0.7,  # Control the randomness of the response
            top_p=1,  # Nucleus sampling, a form of randomness control
            stream=True,  # Enable streaming for real-time responses
            stop=None  # No explicit stopping condition
        )

        Answer = ""  # Initialize the answer as an empty string

        # Collect the response from the API stream in chunks
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        # Clean up the response by removing unnecessary tags
        Answer = Answer.replace("</s>", "")

        # Add assistant's response to the chat log
        messages.append({"role": "assistant", "content": f"{Answer}"})

        # Save the updated chat log to the file
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)  # Write the chat log with proper formatting

        # Return the cleaned answer
        return AnswerModifier(Answer=Answer)

    except Exception as e:
        # In case of an error, reset the chat log and retry the query
        with open(r"Data\ChatLog.json", "w") as f:
            dump([], f, indent=4)  # Reset the chat log
        return ChatBot(Query)  # Retry the query

# Main entry point for the program
if __name__ == "__main__":
    while True:
        # Continuously prompt the user for input
        user = input(">>> Enter Your Question :  ")
        print(ChatBot(user))  # Print the response from the chatbot
