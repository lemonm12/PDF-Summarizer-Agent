import os
import httpx
import streamlit as st
import tempfile
import pdfplumber
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
 
 
 
 
headers = {
    "Ocp-Apim-Subscription-Key": "",
    "Content-Type": "application/json",
}
 
httpx_client = httpx.Client(headers=headers, verify=True)
 
llm = AzureChatOpenAI(
    azure_deployment="gpt-4o",
    azure_endpoint="",
    api_key="",
    api_version="",
    temperature=0.0,
    default_headers=headers,
)
 
 
# Function that handles the extraction of text from a PDF file using pdfplumber
 
 
def extract_pdf_text(pdf_file) -> str:
    # Use pdfplumber to read PDF
    all_text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text += text + "\n"
    return all_text.strip()
 
 
# Function to run the summarization agent using the extracted text and any extra instructions
 
 
def run_summarization_agent(document_text: str, extra_instruction: str = "") -> str:
    # Prompt instruction for the LLM
    instruction = "Summarize the following PDF document for a technical audience."
    if extra_instruction:
        instruction += f" {extra_instruction.strip()}"
        # Importing Chat PromptTemplate from Langchain Libary
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert technical assistant specializing in concise, accurate summaries of complex documents. Given a text, produce a clear and structured summary that highlights the key technical concepts, important data, and actionable insights. Use precise language suitable for a technical audience familiar with the subject matter..",
            ),
            ("human", f"{instruction}\n\n---\n\n{document_text}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    # No tools used here (Simple Agent), Goal: plain summarization
    agent = create_openai_tools_agent(llm, [], prompt)  # Initialize Agent
    agent_executor = AgentExecutor(agent=agent, tools=[], handle_parsing_errors=True)
    response = agent_executor.invoke({"input_text": ""})
    return response.get("output", "No summary produced")
 
 
# Streamlit UI setup
 
st.set_page_config(page_title="PDF Summarizer Agent", layout="centered")
st.title("📄 PDF Summarizer Agent")
st.write("Upload a PDF file, and this agent will summarize its contents for you.")
 
uploaded_pdf = st.file_uploader("Choose a PDF file", type="pdf")
 
if uploaded_pdf is not None:
    # Instructions for User
    with st.expander(
        "💬 Add specific instructions to the summarizer (optional)", expanded=False
    ):
        user_instr = st.text_area(
            "Enter any specific summarization instructions (e.g., be concise, answer specific questions, etc.):",
            height=80,
        )
 
    with st.spinner("Extracting PDF text..."):
        # Save to a temporary location for pdfplumber
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            tmpfile.write(uploaded_pdf.getbuffer())
            tmpfile.flush()
            pdf_text = extract_pdf_text(tmpfile.name)
 
        if not pdf_text.strip():
            st.error(
                "No text could be extracted from the PDF. It may be a scanned/image-only file."
            )
        else:
            st.success("PDF text extracted! Ready for summarization.")
 
            if st.button("Summarize PDF"):
                if len(pdf_text) > 12000:
                    st.warning(
                        "PDF is large—summarization may be truncated due to model limits. Try summarizing specific sections if needed."
                    )
 
                with st.spinner("Summarizing via language model..."):
                    try:
                        summary = run_summarization_agent(
                            document_text=pdf_text, extra_instruction=user_instr
                        )
                        st.subheader("Summary")
                        st.write(summary)
                    except Exception as e:
                        st.error(f"Summarization failed: {e}")
else:
    st.info("Please upload a PDF to begin.")
 
# Optional: Simple FAQ/Help section
with st.expander("ℹ️ About this app", expanded=False):
    st.markdown(
        """
    **PDF Summarizer Agent** uses an LLM to help summarize PDFs.
   
    - Single-Agent.
    - No documents are stored after processing.
    - Text-based PDFs only.
    """
    )