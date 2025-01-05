# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt

# Load environment variables from .env file
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage")  # Get the input language from the .env file

# HTML code for speech recognition
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';  // Placeholder for language, to be updated dynamically
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;  // Append recognized text
            };

            recognition.onend = function() {
                recognition.start();  // Automatically restart recognition
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();  // Stop recognition
            output.innerHTML = "";  // Clear the output
        }
    </script>
</body>
</html>'''

# Replace the language placeholder with the actual input language from the environment variable
HtmlCode = HtmlCode.replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# Write the modified HTML code to a file
with open(r"Data\Voice.html", "w") as f:
    f.write(HtmlCode)

# Construct the file path for the HTML file
current_dir = os.getcwd()
Link = f"{current_dir}/Data/Voice.html"

# Configure Chrome WebDriver options
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Use fake UI for media permissions
chrome_options.add_argument("--use-fake-device-for-media-stream")  # Use fake media device
chrome_options.add_argument("--headless=new")  # Enable headless mode for browser automation

# Set up the WebDriver service
service = Service(ChromeDriverManager().install())

# Initialize the WebDriver with the configured options
driver = webdriver.Chrome(
    service=service,
    options=chrome_options
)

# Path to store temporary status data
TempDirPath = rf"{current_dir}/Frontend/Files"

# Function to set assistant status in a file
def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}/Status.data', "w", encoding='utf-8') as file:
        file.write(Status)

# Function to modify a query for better formatting
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's", "can you"]
    
    # Add appropriate punctuation based on query type
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"   
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."                     
    
    return new_query.capitalize()

# Function to translate text to English
def UniversalTranslator(Text):    
    english_translation = mt.translate(Text, "en", "auto")  # Auto-detect source language
    return english_translation.capitalize()

# Function to perform speech recognition
def SpeechRecognition():
    driver.get("file:///" + Link)  # Open the HTML file in the browser
    driver.find_element(by=By.ID, value="start").click()  # Click the "Start Recognition" button
    
    while True:
        try:
            # Fetch the recognized text
            Text = driver.find_element(by=By.ID, value="output").text
            
            if Text:
                driver.find_element(by=By.ID, value="end").click()  # Stop recognition
                if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                    return QueryModifier(Text)  # Return the modified query
                else:
                    SetAssistantStatus("Translating ...")
                    return QueryModifier(UniversalTranslator(Text))  # Translate and modify query
        except Exception as e:
            pass  # Ignore exceptions during recognition

# Main script execution
if __name__ == "__main__":
    while True:
        Text = SpeechRecognition()  # Perform speech recognition
        print(Text)  # Print the recognized or translated text
