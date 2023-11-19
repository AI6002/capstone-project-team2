from transformers import ViltProcessor, ViltForQuestionAnswering
from PIL import Image
import requests

# Initialize processor and model into global vars
processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
    
def process_vqa(img_path, question):
    # Convert image for processing
    image = Image.open(img_path)
    
    # Prepare inputs
    encoding = processor(image, question, return_tensors="pt")

    # Forward pass
    outputs = model(**encoding)
    logits = outputs.logits
    idx = logits.argmax(-1).item()

    # Get the predicted answer
    return model.config.id2label[idx]

def test_vqa():
    img_path = "../session/user-1/test_img1.jpg"
    question = "what is the color of thing child holding in hand?"
    
    answer = process_vqa(img_path, question)
    print("Answer:", answer)