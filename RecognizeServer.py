import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from flask import Flask, render_template, request
from werkzeug import secure_filename

app = Flask(__name__)

@app.route('/UploadAudio', methods=['POST'])
def uploadAudioFile():
    if request.method=='POST':
        if "file" not in request.files:
            return 'Not Uploaded File'

        # Instantiates a client
        client = speech.SpeechClient()
        
        # Loads the audio into memory
        received_file = request.files.get('file')
        received_file.save("./upload/"+secure_filename(received_file.filename))

        with io.open("./upload/"+secure_filename(received_file.filename), 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)

        config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=48000,
        language_code='ko-KR')

        # Detects speech in the audio file
        response = client.recognize(config, audio)

        for result in response.results:
            result_txt = result.alternatives[0].transcript

        if result_txt:
            return result_txt
        else:
            return 'null'

@app.route('/Test', methods=['GET'])
def test():
    return "success"

if __name__ == "__main__":
    app.run(host='0.0.0.0')