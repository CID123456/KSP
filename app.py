# -*- coding: utf-8 -*-
"""Sent_Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10rDNW6OxdHc-KDWrv-eg1aFDF5BpoXi8
"""
import pandas as pd
import numpy as np
import streamlit as st
"""# **Models**"""

from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

model_name = "deepset/roberta-base-squad2"

# a) Get predictions
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

# b) Load model & tokenizer
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def model(sentence):
    """# **Preprocessing**"""
    
    suspicious_words = [
        "robbery", "crime", "exchange", "extortion", "threat", "suspicious", "fraud", "laundering",
        "illegal", "contraband", "smuggling", "burglary", "assault", "hijacking", "kidnapping", "ransom",
        "hostage", "terrorism", "homicide", "murder", "manslaughter", "weapon", "gun", "explosive", "bomb", "knives",
        "threaten", "blackmail", "intimidate", "menace", "harassment", "stalking", "kidnap", "abduction", "guns", "bombs",
        "abuse", "trafficking", "prostitution", "pimping", "drug", "narcotic", "cocaine", "heroin", "methamphetamine",
        "amphetamine", "opiate", "meth", "gang", "gangster", "mafia", "racket", "extort", "embezzle", "corruption",
        "bribe", "scam", "forgery", "counterfeit", "fraudulent", "cybercrime", "hacker", "phishing", "identity", "theft",
        "credit card", "fraud", "identity", "fraud", "ponzi", "scheme", "pyramid", "scheme", "money", "scam", "swindle", "deception",
        "conspiracy", "scheme", "plot", "coercion", "corrupt", "criminal", "felony", "misdemeanor", "felon", "fugitive",
        "wanted", "arson", "arsonist", "arsony", "stolen", "steal", "loot", "heist", "launder", "hitman", "racketeer",
        "hijack", "smuggle", "terrorist", "kidnapper", "perpetrator", "ringleader", "prowler", "vigilante", "sabotage",
        "saboteur", "suicide", "discreet", "hide", "action", "profile", "alert", "vigilant", "clandestine", "riot", "arms", "deal"
    ]
    
    q = ["","",""]
    a = ["","",""]
    
    q[0] = "What event is going to take place?"
    q[1] = "Where is it going to happen"
    q[2] = "What time is it going to happen?"
    
    QA_input = [{} for i in range(3)]
    res = [{} for i in range(3)]
    
    """# **Output**"""
    
    
    for i in range(3):
      QA_input[i] = {
        'question': q[i],
        'context': sentence
      }
      res[i] = nlp(QA_input[i])
      a[i] = res[i]['answer']
    
    a1 = a[0].lower()
    a1s = set(a1.split())
    sus = set(suspicious_words)
    cw = a1s.intersection(sus)
    
    if len(cw) != 0:
      print("The crime detected is: ",a[0])
      if len(a[1]) != 0:
        print("The location of crime detected is: ",a[1])
      elif len(a[1]) == 0:
        print("No location detected")
      if len(a[2]) != 0:
        print("The time of crime detected is: ",a[2])
      elif len(a[2]) == 0:
        print("No time detected")
    elif len(cw) == 0:
      print("No crime detected")

"""# **Integration**"""

#!pip install flask-ngrok

#from flask import Flask, request, jsonify
#from flask_ngrok import run_with_ngrok

"""
app = Flask(__name__)
run_with_ngrok(app)  # Start ngrok when app is run

# Load your model and any necessary preprocessing steps
# Make sure to adjust this according to your model setup
def predict(sentence):
    # Your prediction code here
    # Replace this with your actual prediction logic
    from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
    model_name = "deepset/roberta-base-squad2"
    # a) Get predictions
    nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
    # b) Load model & tokenizer
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)


    suspicious_words = [
    "robbery", "crime", "exchange", "extortion", "threat", "suspicious", "fraud", "laundering",
    "illegal", "contraband", "smuggling", "burglary", "assault", "hijacking", "kidnapping", "ransom",
    "hostage", "terrorism", "homicide", "murder", "manslaughter", "weapon", "gun", "explosive", "bomb", "knives",
    "threaten", "blackmail", "intimidate", "menace", "harassment", "stalking", "kidnap", "abduction", "guns", "bombs",
    "abuse", "trafficking", "prostitution", "pimping", "drug", "narcotic", "cocaine", "heroin", "methamphetamine",
    "amphetamine", "opiate", "meth", "gang", "gangster", "mafia", "racket", "extort", "embezzle", "corruption",
    "bribe", "scam", "forgery", "counterfeit", "fraudulent", "cybercrime", "hacker", "phishing", "identity", "theft",
    "credit card", "fraud", "identity", "fraud", "ponzi", "scheme", "pyramid", "scheme", "money", "scam", "swindle", "deception",
    "conspiracy", "scheme", "plot", "coercion", "corrupt", "criminal", "felony", "misdemeanor", "felon", "fugitive",
    "wanted", "arson", "arsonist", "arsony", "stolen", "steal", "loot", "heist", "launder", "hitman", "racketeer",
    "hijack", "smuggle", "terrorist", "kidnapper", "perpetrator", "ringleader", "prowler", "vigilante", "sabotage",
    "saboteur", "suicide", "discreet", "hide", "action", "profile", "alert", "vigilant", "clandestine", "riot", "arms", "deal"
    ]

    q = ["","",""]
    a = ["","",""]

    q[0] = "What event is going to take place?"
    q[1] = "Where is it going to happen"
    q[2] = "What time is it going to happen?"

    QA_input = [{} for i in range(3)]
    res = [{} for i in range(3)]

    for i in range(3):
      QA_input[i] = {
        'question': q[i],
        'context': sentence
      }
      res[i] = nlp(QA_input[i])
      a[i] = res[i]['answer']

    a1 = a[0].lower()
    a1s = set(a1.split())
    sus = set(suspicious_words)
    cw = a1s.intersection(sus)


    return {
        'time': a[2],
        'location': a[1],
        'event': a[0]
    }

@app.route('/predict', methods=['POST'])
def predict_api():
    data = request.json
    sentence = data['sentence']

    # Call your model to extract time, location, and event
    result = predict(sentence)

    return jsonify(result)

if __name__ == '__main__':
    app.run(port = 4040)
"""

def main():
    sent = input("Enter sentence")
    model(sent)


if __name__=="__main__": 
    main() 
