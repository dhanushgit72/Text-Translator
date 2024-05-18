# Importing the required libraries
import requests
import os
import uuid
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Route for handling the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Read the values from the form
        original_text = request.form['text']
        target_language = request.form['language']

        # Load the values from .env
        key = os.getenv('KEY')
        endpoint = os.getenv('ENDPOINT')
        location = os.getenv('LOCATION')

        # Indicate that we want to translate and the API version (3.0) and the target language
        path = '/translate?api-version=3.0'

        # Add the target language parameter
        target_language_parameter = '&to=' + target_language

        # Create the full URL
        constructed_url = endpoint + path + target_language_parameter

        # Set up the header information, which includes our subscription key
        headers = {
            'Ocp-Apim-Subscription-Key': key,
            'Ocp-Apim-Subscription-Region': location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        # Create the body of the request with the text to be translated
        body = [{'text': original_text}]

        try:
            # Make the call using post
            translator_request = requests.post(constructed_url, headers=headers, json=body)
            translator_request.raise_for_status()  # Check if the request was successful

            # Retrieve the JSON response
            translator_response = translator_request.json()

            # Retrieve the translation
            translated_text = translator_response[0]['translations'][0]['text']
        except Exception as e:
            translated_text = f"Error occurred: {str(e)}"

        # Call render template, passing the translated text, original text, and target language to the template
        return render_template('results.html', translated_text=translated_text, original_text=original_text, target_language=target_language)
    
    return render_template('index.html')

# Main entry point of the application
if __name__ == '__main__':
    app.run(debug=True)
