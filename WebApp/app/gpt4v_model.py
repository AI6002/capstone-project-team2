import os
import base64
import requests

# Function to read API key
def get_openai_api_key():
    key_file_path = os.environ.get('OPENAI_KEY_PATH', 'openai_key.txt')
    print("key path:", key_file_path)
    with open(key_file_path, 'r') as file:
        return file.read().strip()

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
        
# Example route using the API key
def process_gtp4(img_path, question):
    api_key = get_openai_api_key()
    
    # Getting the base64 string
    base64_image = encode_image(img_path)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
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
    
    
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    api_response = response.json()
    # print(api_response)

    # Extracting the message content
    message_content = api_response['choices'][0]['message']['content']
    return message_content
