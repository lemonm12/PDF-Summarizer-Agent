📄 PDF Summarizer Agent
 Streamlit-basAed web app that extracts text from PDF files and generates concise, structured summaries using Azure OpenAI (GPT-4) via LangChain agents.

✅ Features
Upload PDF and extract text using pdfplumber.

Summarize technical documents using Azure OpenAI's GPT-4 model.

Optional extra instructions to customize summaries.

User-friendly Streamlit UI with status indicators and error handling.

Secure HTTP requests using httpx and truststore.

🛠️ Tech Stack
Python 3.9+

Streamlit for UI

LangChain for prompt orchestration

Azure OpenAI for LLM inference

pdfplumber for text extraction

httpx for HTTP requests

📂 Project Structure
bash
Copy
Edit
pdf-summarizer-agent/
│
├── app.py                # Main Streamlit app (your code)
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
⚙️ Installation
1. Clone the repository
bash
Copy
Edit
git clone https://github.com/yourusername/pdf-summarizer-agent.git
cd pdf-summarizer-agent
2. Create a virtual environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
3. Install dependencies
Create a requirements.txt file with the following:

nginx
Copy
Edit
streamlit
pdfplumber
httpx
truststore
langchain
langchain-openai
Then install:

bash
Copy
Edit
pip install -r requirements.txt
🔑 Azure OpenAI Setup
You need an Azure OpenAI resource with a deployed GPT-4 model.

Update the following values in your code:

python
Copy
Edit
azure_deployment="gpt-4o"     # Your deployment name
azure_endpoint="https://<your-endpoint>.azure-api.net/..."
api_key="YOUR_AZURE_OPENAI_KEY"
Also update your Ocp-Apim-Subscription-Key in headers.

▶️ Run the App
bash
Copy
Edit
streamlit run pdf_agent.py
Open the provided URL in your browser (default: http://localhost:8501).

🖼️ How It Works
Upload a PDF via the UI.

Extract text using pdfplumber.

Generate a summary with Azure GPT-4 through LangChain Agent.

Display summary in a clean UI.

❗Limitations
Only works with text-based PDFs (not scanned images).

Large PDFs (>12,000 tokens) may be truncated due to model limits.

Requires a valid Azure OpenAI subscription.

✅ Future Enhancements
Support for image-based PDFs (via OCR).

Export summaries as PDF or Word.

Multi-file summarization.

📜 License
MIT License.