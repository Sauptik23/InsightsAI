from flask import Flask, render_template, request, send_file,jsonify
import PyPDF2
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from helper_functions import calculate_results,plot_loss_curves
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
import matplotlib.pyplot as plt
from tensorflow.keras.layers import TextVectorization
import os
import pickle

app = Flask(__name__)
def model(): 
    model1 = pickle.load(open('model_5.pkl', 'rb')) # Load your trained ML model
    print("Done")
    return 1

@app.route("/")
def home():    
    l1=model()
    print(l1)
    return render_template("index.html")  # Render home page

# def preprocess():



@app.route("/predict", methods=["POST"])
def predict():
    # Get data from POST request
    data = request.get_json(force=True)

    # Make prediction using model loaded from disk as per the data
    prediction = model.predict([np.array(data["feature"])])

    # Take the first value of prediction
    # output = prediction[0]

    # return str(output)


def convert_file_to_txt(file_path):
    # Get the file extension
    _, file_extension = os.path.splitext(file_path)

    if file_extension == '.pdf':
        # If the file is a PDF, convert it to text
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            text = ''
            for page_num in range(pdf_reader.numPages):
                text += pdf_reader.getPage(page_num).extractText()
        return text

    elif file_extension == '.txt':
        # If the file is already a text file, just read it
        with open(file_path, 'r') as txt_file:
            return txt_file.read()

    else:
        # If the file is neither a PDF nor a text file, raise an error
        raise ValueError('The file must be a .pdf or .txt file')

def read_file_to_sentences(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
            # Splitting text into sentences based on common punctuation marks.
            sentences = text.split('. ')  # Splitting by period and space (assuming sentences end with ". ")
            # If the split didn't properly capture the last sentence (without ". "), add it separately.
            if text[-1] != '.' and sentences[-1] != text:
                sentences.append(text.rsplit('. ', 1)[-1])
            return sentences
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []

if __name__ == "__main__":
    app.run(port=5500, debug=True)
