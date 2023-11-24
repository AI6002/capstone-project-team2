import os
import base64
import requests

# Function to read API key
def get_openai_api_key():
    print("get_openai_api_key")
    key_file_path = os.environ.get('OPENAI_KEY_PATH', 'openai_key.txt')
    try:
        with open(key_file_path, 'r') as file:
            print("get_openai_api_key: file opened")
            return file.read().strip()
    except FileNotFoundError:
        return False

# Function to encode the image
def encode_image(image_path):
    print("encode_image:", image_path)
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            return encoded_image
    except FileNotFoundError:
        print(f"File not found: {image_path}")
        return None
    except IOError as e:
        print(f"IO error occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during image encoding: {e}")
        return None
    
def process_gtp4(img_path, question):
    print("process_gtp4:", img_path, question)
    
    api_key = get_openai_api_key()
    
    if api_key:
        print("API key loaded.")
    else:
        return "Error loading GPT-4 API key."

    base64_image = encode_image(img_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",  # Make sure this is the correct model endpoint
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": question
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    try:
        response =requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        print(f"Response status code: {response.status_code}")

        if response.status_code == 200:
            api_response = response.json()
            message_content = api_response['choices'][0]['message']['content']
            return message_content
        else:
            print(f"Error in API response: {response.text}")
            return f"Error: {response.text}"
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return f"Request failed: {e}"
