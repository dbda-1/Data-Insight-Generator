import os
import pandas as pd
import traceback
import matplotlib.pyplot as plt
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import uvicorn
import google.generativeai as genai

# === 0. Setup ===
app = FastAPI()
templates = Jinja2Templates(directory="templates")
UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
STRUCTURED_CSV_PATH = "structured.csv"

# === 1. Home Page ===
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# === 2. File Upload Endpoint ===
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_ext = file.filename.split('.')[-1].lower()
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    if file_ext in ("xls", "xlsx"):
        df = pd.read_excel(file_path, engine='openpyxl')

    elif file_ext == "csv":
        df = pd.read_csv(file_path)

    elif file_ext == "txt":
        with open(file_path, "r") as f:
            text = f.read()
        df = extract_structured_data(text)

    else:
        return {"error": f"Unsupported file type: {file_ext}. Please upload .csv, .txt, .xlsx, or .xls"}

    df.to_csv(STRUCTURED_CSV_PATH, index=False)
    return {"filename": file.filename, "columns": df.columns.tolist()}

# === 3. Extract structured data from .txt ===
def extract_structured_data(raw_text):
    lines = raw_text.split("\n")
    data = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 3 and any(char.isdigit() for char in line):
            data.append({"month": parts[0], "sales": parts[1], "profit": parts[2]})
    if data:
        return pd.DataFrame(data)
    else:
        return pd.DataFrame()

# === 4. Load Parsed CSV ===
@app.get("/load_structured")
def load_csv():
    if not os.path.exists(STRUCTURED_CSV_PATH):
        return {"error": "No structured.csv found. Upload a file first."}
    df = pd.read_csv(STRUCTURED_CSV_PATH)
    return {"columns": df.columns.tolist(), "preview": df.head().to_dict(orient="records")}

# === 5. Query Model ===
class Query(BaseModel):
    user_query: str

# === 6. Gemini Code Generation ===
GEMINI_API_KEY = "AIzaSyBYuVCOkAIB6pIPFPLhlltE75zHHQK_5xY"  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash-preview-04-17")

def generate_plot_code(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text if response.text else response.candidates[0].content.parts[0].text

# === 7. Generate Plot ===
@app.post("/generate_graph")
def generate_graph(query: Query):
    if not os.path.exists(STRUCTURED_CSV_PATH):
        return {"error": "No structured.csv found. Upload a file first."}

    df = pd.read_csv(STRUCTURED_CSV_PATH)
    prompt = f"""
    You are a Python data analysis assistant. Given a pandas DataFrame called `df` with the following columns:
    {df.columns.tolist()}
    Write Python matplotlib/seaborn code using this df to:
    {query.user_query}
    Do not include data loading code. Just use the variable df.
    """

    code = generate_plot_code(prompt)

    # Clean markdown formatting
    if code.startswith("```"):
        code = code.strip("`").split("python")[-1].strip()

    with open("plot_code.py", "w") as f:
        f.write(code)

    try:
        exec_globals = {"df": df, "plt": plt, "pd": pd}
        exec(code, exec_globals)
        plt.savefig("graph.png")
        plt.close()
        return {"message": "Graph generated successfully", "code": code}
    except Exception as e:
        tb = traceback.format_exc()
        return {"error": str(e), "traceback": tb, "code": code}

# # === 8. Run Server ===
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
