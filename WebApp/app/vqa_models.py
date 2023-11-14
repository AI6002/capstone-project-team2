from transformers import ViltProcessor, ViltForQuestionAnswering
from PIL import Image
import requests

def process_vqa(image, question):
    # Convert image for processing
    image = Image.open(image.stream)

    # Initialize processor and model

    processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
    model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
    
    # Prepare inputs
    encoding = processor(image, question, return_tensors="pt")

    # Forward pass
    outputs = model(**encoding)
    logits = outputs.logits
    idx = logits.argmax(-1).item()

    # Get the predicted answer
    return model.config.id2label[idx]