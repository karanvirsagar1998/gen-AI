# first, lets' install the hugging face: pip install transformers datasets

#second:

from transformers import pipeline

#ABOVE will import the pipeline function from the hugging face transfromers library
# What is pipeline: It's a high-level API that makes it very easy to use pre-trained models for a variety of tasks
# (e.g., sentiment analysis, summarization, translation, etc.)
# It handles loading the model, tokenizer, and preprocessing the input/output automatically.

# List some supported tasks (we cn choose ny of them based on our requirements)
tasks = [
    "sentiment-analysis", #Determines the sentiment of a piece of text (positive, negative, or neutral).
    "text-classification", #Classifies text into predefined categories or labels.
    "ner", #Identifies and classifies entities in text (e.g., names of people, organizations, dates).
    "question-answering", #Given a context (text) and a question, it extracts the correct answer from the context.
    "text-generation", #Generates new text based on a given prompt.
    "summarization", #Produces a shorter version of a longer text while retaining the key points.
    "translation_en_to_fr", #Translates text from English to French.
    "text-to-speech", # Converts written text into spoken words.
    "automatic-speech-recognition", #Converts spoken language into written text (speech-to-text).
    "fill-mask", #Predicts the missing word(s) in a sentence, given a masked word (e.g., [MASK]).
    "zero-shot-classification" #Classifies text into categories without needing labeled data specific to those categories.
]

#Le'ts just use any of them:
classification = pipeline("sentiment-analysis")
result = classification("I love using Chat GPT") # The text is tokenized (split into smaller pieces like words or subwords).
# The tokenized input is fed into the pre-trained model, which predicts the sentiment (e.g., positive or negative).
# The output is returned as a list of dictionaries. Each dictionary contains:
    # The label of the sentiment (e.g., "POSITIVE" or "NEGATIVE").
    # The score, which is the confidence level of the prediction (a value between 0 and 1).
print(result) #output: [{'label': 'POSITIVE', 'score': 0.9950802326202393}]

# Why Are We Writing This Code?
# Hugging Face pipelines make it extremely simple to use pre-trained models for real-world tasks with just a few lines of code.
# You don’t need to worry about downloading models, preprocessing input, or writing boilerplate code.

# Practical Application:
# This code can be used in many scenarios:
    # Analyze customer feedback.
    # Process social media comments.
    # Build automated tools for detecting sentiment in large datasets

new = classification("I hate mathemetics")
print(new)


#Translate to FRENCH
french = pipeline("translation_en_to_fr")
eng_to_fr = french("Hello")
print(eng_to_fr)


#Text-Generator
generator = pipeline("text-generation")
result = generator("Once upon a time, in a land far away, there was a village")
print(result)

