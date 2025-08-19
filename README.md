# HawkMath - Math Expression to LaTeX Converter

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.0%2B-green.svg)

A web application that transcribes spoken math expressions and converts them to LaTeX format. HawkMath uses OpenAI's Whisper for speech-to-text processing and offers two distinct parsing options for maximum flexibility: a custom written parser designed during the hackathon for simple mathematic operations and functions, and a GPT powered parser for more advanced functionality.

This was created for Montclair State University HawkHacks Hackathon 2025

## ✨ Features

- 🎤 **Speech-to-Text**: Uses Whisper AI for accurate transcription of mathematical expressions
- 🧮 **Dual Parsing Options**:
  - Custom rule-based parser for simpler expressions
  - GPT-4 powered parser for complex mathematical notation
- 📝 **LaTeX Output**: Generates clean, properly formatted LaTeX code
- 🌐 **Web Interface**: User-friendly browser-based application
- ⚡ **Real-time Processing**: Quick conversion from speech to LaTeX

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.7+**
- **pip** (Python package manager)
- **Git** (optional, for cloning)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/y0useff/HawkMath
   cd HawkMath
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up Whisper model**
   
   **Option A: Automatic download** (Recommended)
   - The application will download the model automatically on first run
   
   **Option B: Manual download**
   - Download from [OpenAI Whisper GitHub](https://github.com/openai/whisper)
   - Direct link for base English model: [base.en.pt](https://openaipublic.azureedge.net/main/whisper/models/d3dd57d32accea0b295c96e26691aa14d8822fac7d9d27d5dc00b4ca2826dd03/base.en.pt)
   - Place the model file in your preferred directory

6. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   FILE_PATH=/path/to/your/whisper/model/base.en.pt
   ```
   
   **Replace:**
   - `your_openai_api_key_here` with your OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
   - `/path/to/your/whisper/model/base.en.pt` with the path to your Whisper model file

7. **Create uploads directory**
   ```bash
   mkdir uploads
   ```

## 🏃 Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open your browser**
   Navigate to: `http://127.0.0.1:5000`

## 📖 How to Use

1. **🎙️ Record**: Click the microphone button and speak your math expression clearly
2. **⚙️ Choose Parser**: Select your preferred parsing method:
   - **Custom Parser**: Best for simpler expressions (fractions, basic operations)
   - **GPT Parser**: Best for complex expressions (integrals, summations, etc.)
3. **📄 View Results**: The generated LaTeX code will appear in the editor
4. **📋 Copy**: Use the generated LaTeX in your documents, papers, or presentations

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key for GPT-4 parsing | Yes |
| `FILE_PATH` | Path to the Whisper model file | Optional* |

*If not provided, the application will use the default model location

### Supported Math Expressions

- ➕ Basic arithmetic: addition, subtraction, multiplication, division
- 📐 Fractions and mixed numbers
- 🔢 Exponents and roots
- 📊 Summations and products
- ∫ Integrals (definite and indefinite)
- 🔤 Greek letters and mathematical symbols
- 📈 Functions: sin, cos, tan, log, ln, etc.


1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
