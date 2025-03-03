# CV Analysis API - README

## 📌 Project Overview
The **CV Analysis API** is a **FastAPI-based** application that extracts, analyzes, and queries structured information from CVs. It supports **PDF and DOCX formats** and leverages **OpenAI GPT-4** for intelligent CV parsing and **MongoDB** for data storage.

---

## 🚀 Features
- **Upload CVs** (PDF/DOCX) and extract structured information
- **OCR Support** for scanned PDFs
- **MongoDB Integration** for storing and querying CVs
- **FastAPI Endpoints** for text extraction and AI-driven query analysis
- **Logging Support** (INFO, DEBUG, ERROR) for debugging and monitoring
- **AI-Powered Chatbot Querying** to search for candidates based on skills, education, and experience

---

## 🏗️ Project Structure
```
CVInsight/
│── app/
│   ├── routes/
│   │   ├── upload.py  # Handles CV upload and processing
│   │   ├── query.py   # Handles chatbot querying
│   ├── services/
│   │   ├── extractor.py  # Extracts text from PDFs and DOCX files
│   │   ├── llm_analysis.py  # Uses OpenAI GPT-4 to analyze CVs
│   │   ├── prompts.py  # AI prompt for CV extraction and query processing
│   ├── utils/
│   │   ├── logger.py  # Logging configurations
│   ├── config.py  # Configuration file (MongoDB, OpenAI API keys)
│── tests/
│   ├── unit/
│   │   ├── test_upload.py  # Test cases for CV upload
│   │   ├── test_query.py  # Test cases for chatbot queries
│── main.py  # FastAPI entry point
│── requirements.txt  # Dependencies
│── README.md  # Project Documentation
```

---

## 🛠️ Setup & Installation
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/abdullahaish/CVInsight.git
cd CVInsight
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements/requirements.txt
```

### 4️⃣ Configure Environment Variables
Create a `.env` file and add:
```
MONGO_URI=mongodb://localhost:27017
OPENAI_API_KEY=your_openai_api_key
DB_NAME=cv_analysis
COLLECTION_NAME=cvs
```

---

## 🏃‍♂️ Running the API
```bash
uvicorn main:app --reload
```
API will be available at: `http://127.0.0.1:8000`

### 🔍 Interactive API Docs
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Redoc UI: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔗 API Endpoints
### 📂 Upload CV
```http
POST /upload/
```
**Request:**
- `file`: PDF/DOCX CV file

**Response:**
```json
{
    "message": "CV uploaded and processed successfully",
    "data": {"personal_info": {}, "skills": [], "total_experience": "5"}
}
```

---

### 🔍 Chatbot Query
```http
GET /chatbot/?query=Python
```
**Request:**
- `query`: Natural language query (e.g., "Find candidates with FastAPI skills")

**Response:**
```json
{
    "query": "Python Developer",
    "results": [{"name": "John Doe", "skills": ["Python", "FastAPI"]}]
}
```

---

## 🧪 Running Tests
```bash
pytest tests/
```

---

## 📌 Logging
- Logs are saved in the `logs/` directory.
- Logs include `debug.log`, `info.log`, and `warning.log`.

---

## 📬 Contributions & Issues
Feel free to submit issues or contribute via pull requests! 🚀
