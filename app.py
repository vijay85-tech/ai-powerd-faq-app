import os
import logging

from dotenv import load_dotenv
import pandas as pd
import streamlit as st
from openai import OpenAI

# --------------------------------------------------
# Configuration
# --------------------------------------------------

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY not found.")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)
logging.basicConfig(level=logging.INFO)

# --------------------------------------------------
# Session State
# --------------------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --------------------------------------------------
# OpenAI Function
# --------------------------------------------------

def ask_openai(question: str, df: pd.DataFrame):
    columns = ", ".join(df.columns.tolist())
    data_sample = df.head(100).to_csv(index=False)
    prompt = f"""You are a spreadsheet analysis assistant. Available columns: {columns}
Important Rules:
- Use the exact column names.
- Never say a column does not exist if it is listed above.
- Answer only from provided data.
- If unavailable, clearly state it.

Data Sample:
{data_sample}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert spreadsheet analyst."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=500,
        temperature=0
    )

    return response.choices[0].message.content

# --------------------------------------------------
# UI
# --------------------------------------------------

st.set_page_config(
    page_title="Spreadsheet FAQ App",
    layout="wide"
)
st.title("Spreadsheet: Frequently Asked Questions")
st.caption(
    "Upload CSV or Excel files and ask questions about their data."
)

# --------------------------------------------------
# Upload Files
# --------------------------------------------------

uploaded_files = st.file_uploader(
    "Upload CSV or Excel files",
    type=["csv", "xlsx", "xls"],
    accept_multiple_files=True
)

dataframes = {}
if uploaded_files:
    for file in uploaded_files:
        try:
            if file.name.lower().endswith(".csv"):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            blank_rows = df.astype("string").apply(
                lambda column: column.str.strip().eq("").fillna(True)
            ).all(axis=1)
            df = df.loc[~blank_rows]
            df.columns = (
                df.columns
                .str.strip()
                .str.replace("\n", " ", regex=False)
            )
            dataframes[file.name] = df
        except Exception as e:
            st.error(f"Error loading {file.name}: {e}")

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

if dataframes:
    st.sidebar.subheader("Select file")
    selected_file = st.sidebar.selectbox(
        "",
        list(dataframes.keys())
    )

    df = dataframes[selected_file]
    st.write(f"### Showing: {selected_file.upper()}")
    with st.expander("Columns"):
        st.write(df.columns.tolist())

    st.dataframe(
        df,
        use_container_width=True
    )

    # --------------------------------------------------
    # Display Chat History
    # --------------------------------------------------

    for item in st.session_state.chat_history:
        st.chat_message("user").write(
            item["question"]
        )

        st.chat_message("assistant").write(
            item["answer"]
        )

    # --------------------------------------------------
    # Chat Input
    # --------------------------------------------------

    question = st.chat_input(
        "Ask a question about spreadsheet data..."
    )

    if question:
        st.chat_message("user").write(question)
        try:
            with st.spinner("Analyzing data..."):

                answer = ask_openai(
                    question,
                    df
                )

            st.chat_message("assistant").write(
                answer
            )

            st.session_state.chat_history.append(
                {
                    "question": question,
                    "answer": answer
                }
            )

        except Exception as e:
            st.error(
                f"Error generating answer: {e}"
            )