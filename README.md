# Jarvis AI - Intelligent Assistant

Jarvis AI is an advanced real-time AI assistant that can handle complex queries, speak responses, generate images, and perform automation tasks. Designed with cutting-edge AI capabilities, it leverages APIs to provide powerful features and seamless interaction.

## Features
- **Real-Time Query Handling**: Answers questions and provides solutions instantly.
- **Voice Interaction**: Speaks responses for a natural conversational experience.
- **Image Generation**: Creates images based on user descriptions.
- **Automation**: Executes automated tasks and workflows based on user commands.

## Prerequisites
Ensure you have the following API keys:

- [Cohere](https://cohere.com/): For language processing and advanced AI capabilities.
- [GroqCloud](https://console.groq.com/keys): For optimizing computations and AI performance.
- [HuggingFace](https://huggingface.co/): For NLP and image generation models.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/jarvis-ai.git
   cd jarvis-ai
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r .\Requirements.txt
   ```

## Setup
1. Create a `.env` file in the project root and add your API keys (replace placeholders with your actual keys):
   ```env
   CohereAPIKey = <your_cohere_api_key>
   Username = <your_username>
   Assistantname = <assistant_name>
   GroqAPIKey = <your_groq_api_key>
   InputLanguage = en 
   # hi = hindi ,en = english
   AssistantVoice = en-CA-LiamNeural
   HuggingFaceAPIKey = <your_huggingface_api_key>
   ```
2. Configure additional settings in the `config.py` file if needed.

## Usage
Run the AI assistant with the following command:
```bash
python main.py
```

### Capabilities
1. **Query Handling**:
   - Ask any question, and Jarvis will provide accurate answers.
   - Example:
     ```
     User: What is the capital of France?
     Jarvis: The capital of France is Paris.
     ```

2. **Voice Interaction**:
   - Enable the speaking mode to hear responses.
   - Example:
     ```
     User: Tell me a joke.
     Jarvis: Why don’t scientists trust atoms? Because they make up everything! (spoken response)
     ```

3. **Image Generation**:
   - Generate custom images by describing them.
   - Example:
     ```
     User: Create an image of a futuristic city at sunset.
     ```

4. **Automation**:
   - Perform tasks like setting reminders, sending emails, or controlling IoT devices.



## Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments
- [Cohere](https://cohere.com/) for language AI.
- [GroqCloud](https://console.groq.com/) for computation optimization.
- [HuggingFace](https://huggingface.co/) for NLP and image generation models.
