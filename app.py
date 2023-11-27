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
from spacy.lang.en import English
import re

app = Flask(__name__)

model1 = pickle.load(open('model/model_5.pkl', 'rb')) # Load your trained ML model
print("Done")
label_encoder_classes=np.array(['BACKGROUND','CONCLUSIONS','METHODS','OBJECTIVE','RESULTS'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('ABOUT.html')

@app.route('/how-it-works')
def how_it_works():
    return render_template('how-it-works.html')

@app.route('/summarize')
def summarize():
    return render_template('summarize.html') # Render home page

# def preprocess():



# @app.route("/submit", methods=["GET","POST"])
# def submit():
#     # Get data from POST request
#     if request.method==["GET"]:
#         # user_text = request.form['user_text']
#         # # Do something with the received text (e.g., print it)
#         # print("Received text:", user_text)
#         # # Here, you can perform actions like storing the text in a database, processing it, etc.
#         # return "Text received: " + user_text
#         return render_template('index.html')

    # Take the first value of prediction
    # output = prediction[0]

    # return str(output)

def spacy(data):
    nlp=English()
    sentencizer=nlp.add_pipe("sentencizer")
    doc=nlp(data["Abstract"])
    abstract_lines=[str(sent) for sent in list(doc.sents)]
    return abstract_lines

@app.route('/submit_text', methods = ['GET', 'POST'])
def submit_text():
   
   if request.method == 'POST':
      
      text = request.form['text']
      split_sentence = text.split(':')

# Extracting the key and creating the dictionary
      data = {split_sentence[0].strip(): ' '.join(map(str.strip, split_sentence[1:]))}
    #   print(text)
    #   data=extract_headings_and_info_from_text_box(text)
      print(data)


      abstract_lines=spacy(data)
      sample_lines=lines_dict(abstract_lines)
      one_hot_line_numbers=line_numbers_one_hot(sample_lines)
      one_hot_total_lines=total_lines_one_hot(sample_lines)
      abstract_chars = [split_chars(sentence) for sentence in abstract_lines]
      pred_probabilty=model1.predict(x=(one_hot_line_numbers,
                                        one_hot_total_lines,
                                        tf.constant(abstract_lines),
                                        tf.constant(abstract_chars)))
      abstract_preds=tf.argmax(pred_probabilty,axis=1)
      abstract_pred_classes = [label_encoder_classes[i] for i in abstract_preds]
      result_dict={"BACKGROUND":"","CONCLUSIONS":"","METHODS":"","OBJECTIVE":"","RESULTS":""}
      for i, line in enumerate(abstract_lines):
        result_dict[abstract_pred_classes[i]]+=line
        # print(f"{abstract_pred_classes[i] }: {line}")
        
      return render_template('summarize.html',data=result_dict)

def lines_dict(abstract_lines):
    total_lines=len(abstract_lines)
    sample_lines=[]
    for i,line in enumerate(abstract_lines):
        sample_dict={}
        sample_dict["text"]=str(line)
        sample_dict["line_number"]=i
        sample_dict["total_lines"]=total_lines - i
        sample_lines.append(sample_dict)
    return sample_lines

def line_numbers_one_hot(sample_lines):
    line_numbers=[line["line_number"] for line in sample_lines]
    one_hot_line_numbers=tf.one_hot(line_numbers,depth=15)
    return one_hot_line_numbers

def total_lines_one_hot(sample_lines):
    total_lines=[line["total_lines"] for line in sample_lines]
    one_hot_total_lines=tf.one_hot(total_lines,depth=20)
    return one_hot_total_lines

def split_chars(text):
  return " ".join(list(text))

# def extract_headings_and_info_from_text_box(lines):
   
   
#    lines = text.split('\n')

#     # Initialize an empty dictionary to store the headings and their information
#    headings_info = {}

#     # Initialize variables to hold the current heading and information
#    current_heading = None
#    current_info = []

#     # Iterate over the lines
# for line in lines:
#         # If the line ends with a colon, it's a heading
#         if re.match('.*:$', line):
#             # If there's a current heading, add it and its information to the dictionary
#             if current_heading is not None:
#                 headings_info[current_heading] = '\n'.join(current_info)

#             # Start a new heading and clear the information
#             current_heading = line[:-1]
#             current_info = []
#         else:
#             # If it's not a heading, it's information; add it to the current information
#             current_info.append(line)

#     # Add the last heading and its information to the dictionary
#     if current_heading is not None:
#         headings_info[current_heading] = '\n'.join(current_info)

#     return headings_info

def extract_headings_and_info(lines):
    data_dict = {}
    current_heading = None

    for line in lines:
        line = line.strip()
        if line.endswith(':'):  # This line is a heading
            current_heading = line[:-1]  # Remove the colon at the end
            data_dict[current_heading] = ''
        elif current_heading is not None:
            # This line is information; append it to the current heading
            line=line+' '
            data_dict[current_heading] += line
            # line=line + ' '
        line=line+'\n'
    return data_dict

def extract_text_from_pdf(filename):
                            # Open the PDF file in binary mode
    with open(filename, 'rb') as file:
                            # Create a PDF file reader object
        pdf_reader = PyPDF2.PdfReader(file)

        #                    Initialize an empty string to hold the PDF text
        pdf_text = ''

                            # Loop through each page in the PDF and extract the text
        for page_num in range(len(pdf_reader.pages)):
            # page = pdf_reader.getPage(page_num)
            page=pdf_reader.pages[page_num]
            pdf_text += page.extract_text()

    # Split the PDF text into lines
    lines = pdf_text.split('\n')
    return lines

def preprocessing(filename):
    ext=check_file_ext(filename)
    if ext==1:
      lines=extract_text_from_pdf(filename)
      data_dict=extract_headings_and_info(lines)
    elif ext==2:
      with open(filename, 'r') as file:
          lines = file.readlines()
          data_dict=extract_headings_and_info(lines)
    
    return data_dict
    

def check_file_ext(filename):
    # Get the file extension
    _, file_extension = os.path.splitext(filename)

    if file_extension == '.pdf':
        
        return 1
       
    elif file_extension == '.txt':

     
      return 2

    else:
        raise ValueError('The file must be a .pdf or .txt file')


@app.route('/upload_file', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      print("hello world")
      return "Hello world"
      

    
if __name__ == '__main__':
   app.run(debug = True)
  

# @app.route('/summarize'.methods=='POST')
# def predict():
#     if flask.request.method=='POST':
#         return (flask.render_template('index.html'))
# @app.route('')
# def read_file_to_sentences(filename):
#     try:
#         with open(file_path, 'r') as file:
#             text = file.read()
#             # Splitting text into sentences based on common punctuation marks.
#             sentences = text.split('. ')  # Splitting by period and space (assuming sentences end with ". ")
#             # If the split didn't properly capture the last sentence (without ". "), add it separately.
#             if text[-1] != '.' and sentences[-1] != text:
#                 sentences.append(text.rsplit('. ', 1)[-1])
#             return sentences
#     except FileNotFoundError:
#         print(f"File '{file_path}' not found.")
#         return []

