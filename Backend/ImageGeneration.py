import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep

# Function to open and display generated images
def open_images(prompt):
    """
    Opens images from the 'Data' folder based on the provided prompt.
    The prompt determines the file name format.
    """
    folder_path = "Data"
    prompt = prompt.replace(" ", "_")
    files = [f"{prompt}{i}.jpg" for i in range(1, 5)]
    
    for jpg_file in files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)  # Pause to ensure images have time to display
        except IOError:
            print(f"Unable to open {image_path}. Check if the file exists.")

# HuggingFace API endpoint and authorization setup
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

# Asynchronous function to query the HuggingFace API
async def query(payload):
    """
    Sends a POST request to the API with the given payload.
    Returns the response content (image bytes).
    """
    try:
        response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for HTTP issues
        return response.content
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return None

# Asynchronous function to generate images based on the prompt
async def generate_images(prompt: str):
    """
    Generates images using the HuggingFace API for the given prompt.
    Saves the generated images in the 'Data' folder.
    """
    tasks = []
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality-4K, sharpness-maximum, Ultra High details, high resolution"
        }
        tasks.append(asyncio.create_task(query(payload)))
    
    image_bytes_list = await asyncio.gather(*tasks)
    
    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes:  # Ensure image_bytes is valid
            file_path = os.path.join("Data", f"{prompt.replace(' ', '_')}{i + 1}.jpg")
            with open(file_path, "wb") as f:
                f.write(image_bytes)
            print(f"Image saved: {file_path}")
        else:
            print(f"Failed to generate image {i + 1}.")

# Wrapper function to generate and open images
def GenerateImages(prompt: str):
    """
    Generates images using the API and then displays them.
    """
    asyncio.run(generate_images(prompt))
    open_images(prompt)

# Main loop to monitor the file for new image generation tasks
while True:
    try:
        # Read the data file for the prompt and generation status
        with open(r"Frontend\Files\ImageGeneration.data") as f:
            data = f.read().strip()
        prompt, status = data.split(",")
        
        if status == "True":
            print("Generating Images...")
            GenerateImages(prompt)
            # Update the file to indicate task completion
            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False, False")
            break
        else:
            sleep(1)  # Wait before checking again
    except FileNotFoundError:
        print("Data file not found. Ensure the file path is correct.")
        sleep(1)
    except:
       pass
   