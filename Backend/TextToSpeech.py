import pygame  # For playing audio
import random  # For random selection of responses
import asyncio  # For asynchronous functions
import edge_tts  # For text-to-speech (TTS)
import os  # For file operations
from dotenv import dotenv_values  # For loading environment variables from .env file

# Load environment variables from .env file
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice")  # Get the voice setting from the .env file

# Function to generate an audio file from the provided text
async def TextToAudioFile(text) -> None:
    file_path = r"Data\speech.mp3"  # Path for the generated speech file

    # Remove the existing file to ensure no conflicts
    if os.path.exists(file_path):
        os.remove(file_path)

    # Correctly instantiate the Communicate class
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')
    await communicate.save(file_path)

# Function to play the text-to-speech audio
def TTS(Text, func=lambda r=None: True):
    try:
        # Convert text to audio file
        asyncio.run(TextToAudioFile(Text))

        # Initialize the Pygame mixer for playing the audio
        pygame.mixer.init()
        pygame.mixer.music.load(r"Data\speech.mp3")
        pygame.mixer.music.play()

        # Wait while the audio is playing
        while pygame.mixer.music.get_busy():
            if not func():  # Call the provided callback function
                break
            pygame.time.Clock().tick(10)  # Wait 10ms before checking again

    except Exception as e:
        print(f"Error in TTS: {e}")
    finally:
        try:
            # Safely stop and quit the mixer
            func(False)
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
                pygame.mixer.quit()
        except Exception as e:
            print(f"Error in finally block: {e}")

# Function to process text and play it as speech
def TextToSpeech(Text, func=lambda r=None: True):
    # Split the input text into sentences
    Data = str(Text).split(".")

    # Predefined responses for large text
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]
    # If the text is too long, truncate and add a response
    if len(Data) > 4 and len(Text) >= 250:
        TTS(" ".join(Text.split(".")[0:2]) + ". " + random.choice(responses), func)
    else:
        TTS(Text, func)

# Main execution loop
if __name__ == "__main__":
    try:
        while True:
            # Take user input and convert it to speech
            TextToSpeech(input(">>> Enter the text: "))
    except KeyboardInterrupt:
        print("\nExiting program.")
