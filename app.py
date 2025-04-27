

import whisper
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
model = whisper.load_model("./models/base.en.pt")


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def process_audio(file_path):
    # Your Python function to process the audio
    return model.transcribe(file_path)


@app.route('/', methods=["GET"])
def home():
    return render_template('index.html')  # <== This will load your HTML file

@app.route('/process_audio', methods=['POST'])
def handle_audio_upload():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file sent"}), 400
    
    audio_file = request.files['audio']
    filename = secure_filename(audio_file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    audio_file.save(file_path)

    # Run your function
    result = process_audio(file_path)
    print(result["text"])
    return jsonify(result["text"])
    #transcribed text is returned, must feed into model in the morning

if __name__ == '__main__':
    app.run(debug=True)



#sample output
# {'text': ' 4x squared', 'segments': [{'id': 0, 'seek': 0, 'start': 0.0, 'end': 4.0, 'text': ' 4x squared', 'tokens': [50363, 604, 87, 44345, 50563], 
# 'temperature': 0.0, 'avg_logprob': -0.629383365313212, 'compression_ratio': 0.5555555555555556, 'no_speech_prob': 0.09730338305234909}], 'language': 'en'}
#4 x squared


