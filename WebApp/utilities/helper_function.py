import tensorflow as tf
import numpy as np
import re
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg19 import preprocess_input

# Function to extract features from an image
def image_feature_extractor(image_file, model):
    img = image.load_img(image_file, target_size=(224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)

    features = model.predict(img)
    features = tf.reshape(features, (features.shape[0], features.shape[1], -1))
    features = tf.transpose(features, perm=[0, 2, 1])
    return features

# Function to preprocess and clean a question
def process_sentence(sentence):
    # Add your preprocessing steps here (e.g., removing special characters, lowercasing)
    cleaned_sentence = sentence.lower()  # This is a simple example
    return cleaned_sentence

# Function to predict the answer to a question based on an image
def predict_answers(image_file, question, vqa_model, image_model):
    img_feat = image_feature_extractor(image_file, image_model)
    question_feat = process_sentence(question)
    # You might need another function to turn the cleaned question into a feature vector

    preds = vqa_model.predict([img_feat, question_feat])  # Assuming your model takes two inputs
    # Post-process the model's prediction to get a human-readable answer
    answer = "Yes" if preds[0] > 0.5 else "No"  # This is a simplistic binary example
    return answer

# You might need other utility functions here, such as a function to convert processed questions into feature vectors






































#def my_helper():
    # TODO: Implement helper function logic here
    #pass