# CSV FAQ App

An AI-powered Streamlit application that allows users to upload CSV files and ask natural language questions about their data.

## Features

- Upload multiple CSV files
- Switch between uploaded files
- Interactive chat interface
- AI-powered Q&A
- Chat history support
- CSV preview
- Column inspection
- Error handling

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd csv-faq-app
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key
```

---

## Run Application

```bash
streamlit run app.py
```

---

## Project Structure

```text
project/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
│
└── data/
```

---

## Technologies

- Streamlit
- Pandas
- OpenAI API
- Python Dotenv

---

## Future Enhancements

- Vector Search
- Embedding-based Retrieval
- Charts and Graphs
- Download Chat History
- Multi-file Question Answering
- SQL Agent Integration