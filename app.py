import whisper
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import re
import requests
from dotenv import load_dotenv
import json


load_dotenv()


file_path = os.getenv('FILE_PATH')

# Load whisper model
model = whisper.load_model(file_path)



app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def process_audio(file_path):
    return model.transcribe(file_path)
#function to transcribe numbers being spoken to numeric values
def word_to_number(text):
    units = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9
    }
    teens = {
        "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
        "fourteen": 14, "fifteen": 15, "sixteen": 16,
        "seventeen": 17, "eighteen": 18, "nineteen": 19
    }
    tens = {
        "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
        "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90
    }

    text = text.lower().replace("-", " ")
    words = text.split()

    num = current = 0
    for word in words:
        if word in units:
            current += units[word]
        elif word in teens:
            current += teens[word]
        elif word in tens:
            current += tens[word]
        elif word == "hundred":
            current *= 100
        elif word == "thousand":
            current *= 1000
            num += current
            current = 0
        else:
            return None
    return num + current
#function to read and parse keywords that were related to mathematic functions
def parse(text):
    operations = {
        "add": "+", "plus": "+", "minus": "-", "subtract": "-",
        "multiply": "\\times", "times": "\\times",
        "divide": "\\div", "open parenthesis": "(", "close parenthesis": ")", "power of" : "^{"
    }

    text = text.lower().replace("-", " ")
    text = re.sub(r'(\d+)/(\d+)', r'\\frac{\1}{\2}', text)

    words = text.split()
    result = []
    i = 0

    while i < len(words):
        word = words[i]
        next_word = words[i + 1] if i + 1 < len(words) else ""
        combined = f"{word} {next_word}"

        # Special case: "divide by" for fractions
        if word == "divide" and next_word == "by" and i + 2 < len(words):
            numerator = result.pop() if result else None
            if numerator is not None and isinstance(numerator, str):
                num_value = word_to_number(numerator)
                if num_value is not None:
                    numerator = str(num_value)

            i += 2  # Skip "divide by"
            denominator_words = []
            while i < len(words) and (words[i].isdigit() or word_to_number(words[i]) is not None):
                denominator_words.append(words[i])
                i += 1
            denominator = word_to_number(' '.join(denominator_words)) if denominator_words else None

            if numerator and denominator is not None:
                result.append(f"\\frac{{{numerator}}}{{{denominator}}}")
            continue

        # Handle combined operations like "open parenthesis"
        if combined in operations:
            result.append(operations[combined])
            i += 2
            continue

        # Handle simple one-word operations
        if word in operations:
            result.append(operations[word])
            i += 1
            continue

        # Handle digits
        if word.isdigit():
            result.append(word)
            i += 1
            continue

        # Handle variables or combined numbers and variables like "3x"
        if re.match(r'^[a-zA-Z]+$', word) or re.match(r'^\d+[a-zA-Z]+$', word):
            result.append(word)
            i += 1
            continue

        # Try grouping number words (e.g., "twenty five")
        j = i
        num_words = []
        while j < len(words) and word_to_number(words[j]) is not None:
            num_words.append(words[j])
            j += 1
        if num_words:
            number = word_to_number(' '.join(num_words))
            result.append(str(number))
            i = j
            continue

        # Skip unknown words
        i += 1

    return "\\begin{align}\n" + ' '.join(result) + "\n\\end{align}"

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

@app.route('/parse_audio', methods=['POST'])
def hand_parse():
    # Check if the request is JSON or raw data
    if request.is_json:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing text in request'}), 400
        text = data['text']
    else:
        # Read raw data (plain text)
        text = request.data.decode('utf-8')
        
    if not text:
        return jsonify({'error': 'Missing text body'}), 400

    print(f"Parse request received: {text}")
    parsed_result = parse(text)
    print(f"Parse result: {parsed_result}")
    
    return parsed_result

@app.route('/parse_audio_gpt', methods=['POST'])
def gpt_parse():
    # Check if the request is JSON or raw data
    if request.is_json:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing text in request'}), 400
        text = data['text']
    else:
        # Read raw data (plain text)
        text = request.data.decode('utf-8')
        
    if not text:
        return jsonify({'error': 'Missing text body'}), 400

    print(f"GPT parse request received: {text}")
    
    # OpenAI API configuration
    openai_api_key = os.getenv('OPENAI_API_KEY')
    
    # System prompt for GPT
    system_prompt = """The user will give you a verbal natural language expression, given by someone trying to write a math expression. Please give it to me in LaTeX, respond only with LaTex, and make it so each term is on a new line, with the begin and end tags having their own lines. For terms involving functions, such as \frac, output the following format:

    \frac
    {numerator}
    {denominator}

    Example output:

    \begin{align}
    \int
    \frac
    {-4x^2}
    {x}
    dx
    \end{align}

    Ensure that there are NO "//" substrings present in the output. They will unintentionally create new lines.

    \begin{align}
    U = \\
    \ln \\
    K
    \end{align}

    THIS is bad output."""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text}
    ]
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai_api_key}"
            },
            json={
                "model": "gpt-4",
                "messages": messages
            }
        )
        
        response_data = response.json()
        if 'choices' in response_data and len(response_data['choices']) > 0:
            latex_response = response_data['choices'][0]['message']['content']
            print(f"GPT parse result: {latex_response}")
            
            # Check for slash characters
            if "/" not in latex_response:
                # No "/" found, return without rendering LaTeX
                return latex_response
            elif "//" in latex_response:
                # Replace "//" with spaces before rendering
                modified_response = latex_response.replace("//", " ")
                return modified_response  # This will be rendered as LaTeX
            else:
                # Single "/" found, render normally
                return latex_response  # This will be rendered as LaTeX
        else:
            print(f"Error in GPT response: {response_data}")
            return "Error processing with GPT. Please try again."
    
    except Exception as e:
        print(f"Error communicating with OpenAI API: {e}")
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
