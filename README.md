# Document Assistant

An AI-powered document assistant built with Python and Streamlit. It allows users to upload documents, ask questions, summarize content, compare files, and maintain a personal conversation history tied to a login system.

## Overview

This project combines:

- Streamlit for the frontend UI
- Gemini models for document understanding and answer generation
- FAISS + embeddings for semantic retrieval over uploaded text
- MySQL for user authentication and chat history storage
- Python file readers for PDFs, Word docs, spreadsheets, presentations, and text-based formats

The app is designed for a document-centric workflow where users can:

1. Create an account or log in
2. Upload one or more files
3. Summarize large documents
4. Compare two files side by side
5. Ask questions based on uploaded documents or general chat
6. Review previous interactions from their account history

## Features

- User registration and authentication using Aadhaar number + email
- Session-based access control with login/logout flow
- Multi-format document ingestion:
  - PDF
  - DOCX
  - TXT
  - MD
  - PPTX
  - CSV
  - XLSX
  - XLS
  - JSON
- Summarization of uploaded documents
- Comparison between exactly two documents
- Context-aware Q&A using semantic search over indexed chunks
- Persistent conversation history stored in MySQL
- Modern UI with a research-dashboard style layout

## Project Structure

- `genai.py` – main Streamlit application and AI workflow
- `login.py` – login and registration interface
- `database.py` – MySQL connection, schema creation, and user/history functions
- `reader.py` – document text extraction logic
- `chunk.py` – chunking, embeddings, and vector-store creation
- `requirements.txt` – Python dependencies
- `uploaded_documents/` – folder for uploaded or local documents
- `.env` – environment configuration file (not committed in some setups)

## Tech Stack

- Python 3
- Streamlit
- LangChain
- Google Generative AI / Gemini
- FAISS
- MySQL Connector
- PyPDF2
- python-docx
- python-pptx
- pandas
- openpyxl / Excel support

## Setup

### 1. Clone the project

```bash
git clone <repository-url>
cd Hackathon
```

### 2. Create a virtual environment

On Windows:

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root with your credentials:

```env
GEMINI_API_KEY=your_google_gemini_api_key

MYSQLHOST=your_mysql_host
MYSQLPORT=3306
MYSQLUSER=root
MYSQLPASSWORD=your_mysql_password
MYSQLDATABASE=railway
```

The application also includes default MySQL connection values in `database.py`, but using `.env` is the preferred setup.

## Run the Application

Start the app with:

```bash
streamlit run genai.py
```

Then open the URL shown by Streamlit in your browser.

## Usage

### Sign in / create account

- Enter Aadhaar card number and email on the login screen
- Or create a new account from the registration tab

### Summarize documents

- Upload one or more supported files
- Enter a summarization instruction
- Click Run
- The app builds a vector index from the document text and sends the relevant chunks to the Gemini model

### Compare documents

- Upload exactly two files
- Enter a comparison prompt
- Click Compare
- The app analyzes both documents and highlights differences or similarities

### Ask questions

- Upload optional files to ground the answer in local document context
- Enter a question in the chat area
- If no files are uploaded, the model responds as a general assistant

### View history

- Open the sidebar history panel
- Previous questions and answers for the logged-in user are stored in MySQL

## Database Behavior

On startup, `database.py` automatically creates the required tables if they do not already exist:

- `user`
- `history`

This is done through the `createtable()` function called at the end of the file.

## Important Notes

- The app requires a valid Gemini API key for model access.
- If the API key is missing, the app displays a warning and model-based tasks will fail until it is configured.
- File types are validated in `genai.py` using the supported list defined in the app.
- Uploaded files are processed in memory, chunked, and embedded before retrieval.

## Troubleshooting

### Model errors

Check that:

- `GEMINI_API_KEY` is set in `.env`
- The API key is valid
- The required LangChain Google AI packages are installed

### Database errors

Check that:

- MySQL is running
- The specified host, port, user, password, and database are correct
- The database user has permission to create tables and insert records

### File processing issues

Verify the upload is one of the supported formats and the file is not corrupt.

## License

This project is intended for educational or hackathon use unless another license is specified by the repository owner.

## Credits

This project was built as a document intelligence and retrieval assistant combining LLM-based reasoning with local document indexing and storage.
