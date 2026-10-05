# AI Question Generator

An AI-powered web application that automatically generates questions and answers from uploaded PDF documents using Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG).

## Developer & Project Information

- **Developer Name**: Satyam Singh
- **Registration Number**: 23FE10CDS00413
- **Branch**: Data Science
- **Batch**: F
- **Project Title**: AI Question Answer Generator
- **GitHub**: [@satyamsingh39](https://github.com/satyamsingh39)

---

## Features

- **PDF-Based AI Question & Answer Generation**: Extract content from uploaded PDF documents to generate relevant questions and context-aware answers.
- **Pretrained LLM via Groq**: Uses Groq's high-performance inference engine with the `openai/gpt-oss-20b` model.
- **RAG Architecture**: Uses Retrieval-Augmented Generation with FAISS vector database to produce accurate, context-bound answers.
- **HuggingFace Embeddings**: Vector search powered by `sentence-transformers/all-MiniLM-L6-v2`.
- **Question Type Selection**: Choose between `MCQ`, `Short Answer`, and `True/False`.
- **Difficulty Selection**: Select question difficulty levels: `Easy`, `Medium`, or `Hard`.
- **On-Page Results Display**: Generated Q&A pairs (Question number, Question, and Answer) display directly on the webpage in a clean card layout.
- **Markdown Cleanup**: Automatically strips raw markdown tags (such as bold `**`, italic `*`, and backticks `` ` ``) for clean display.
- **CSV Export**: Option to download generated Q&A as a UTF-8 encoded CSV file compatible with Excel.
- **Clean Web Interface**: Fast HTML/CSS/JavaScript frontend powered by a FastAPI backend.

---

## Tech Stack

- **Backend**: FastAPI (Python 3.10+)
- **LLM**: Groq API (`openai/gpt-oss-20b`)
- **Embeddings**: HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`)
- **Vector Database**: FAISS (Facebook AI Similarity Search)
- **Orchestration**: LangChain
- **Frontend**: HTML5, CSS3, Vanilla JavaScript, Jinja2 Templates

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/satyamsingh39/Question_generator.git
cd Question_generator
```

### 2. Create and activate a virtual environment

**Using venv:**

```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your API key from [Groq Console](https://console.groq.com/).

---

## Running the Application

Start the server using:

```bash
python app.py
```

Open your browser and navigate to `http://localhost:8080` (or `http://127.0.0.1:8080`).

---

## How to Use

1. **Upload PDF**: Select or drag-and-drop a PDF document and click **Upload PDF**.
2. **Configure Options**:
   - Choose **Question Type** (*Short Answer*, *MCQ*, or *True/False*).
   - Choose **Difficulty** (*Easy*, *Medium*, or *Hard*).
3. **Generate Q&A**: Click **Generate Q&A**.
4. **View & Export**:
   - View generated questions and answers formatted directly on the page.
   - Click **Download CSV** to save the generated Q&A to your device.

---

## Project Structure

```
question-generator/
├── app.py                  # FastAPI server endpoints
├── requirements.txt        # Python dependencies
├── setup.py                # Package setup script
├── .env                    # Environment variables (Groq API Key)
├── README.md               # Project documentation
├── src/
│   ├── helper.py           # Document processing, RAG, and LLM pipeline
│   └── prompt.py           # Custom prompt templates
├── templates/
│   └── index.html          # Web interface
└── static/
    ├── docs/               # Uploaded PDF files
    └── output/             # Exported CSV files
```

---

## API Endpoints

### `GET /`
Renders the main web interface (`index.html`).

### `POST /upload`
Uploads a PDF file to the server.
- **Payload**: `Multipart/form-data` (`pdf_file`, `filename`)
- **Response**: `{"msg": "success", "pdf_filename": "<path>"}`

### `POST /analyze`
Processes the uploaded PDF and generates Q&A pairs according to selected options.
- **Payload**: `FormData` (`pdf_filename`, `question_type`, `difficulty`)
- **Response**: JSON array of Q&A objects `[{"question_num": 1, "question": "...", "answer": "..."}]` and CSV output path.

---

## License

This project is open-source and available under the [MIT License](LICENSE).