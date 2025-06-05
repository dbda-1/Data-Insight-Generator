import os
import pandas as pd
import traceback
import matplotlib.pyplot as plt
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def index():
    with open("templates/index.html", "r") as f:
        return f.read()

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
STRUCTURED_CSV_PATH = "structured.csv"

# === 1. Upload Document and Process (Excel and Text only) ===
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_ext = file.filename.split('.')[-1].lower()
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    if file_ext in ("xls", "xlsx"):
        df = pd.read_excel(file_path, engine='openpyxl')

    elif file_ext == "txt":
        with open(file_path, "r") as f:
            text = f.read()
        df = extract_structured_data(text)

    else:
        return {"error": f"Unsupported file type: {file_ext}. Please upload .txt or .xlsx/.xls"}

    df.to_csv(STRUCTURED_CSV_PATH, index=False)
    return {"filename": file.filename, "columns": df.columns.tolist()}

# === 2. Parse Structured Data from Raw Text ===
def extract_structured_data(raw_text):
    lines = raw_text.split("\n")
    data = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 3 and any(char.isdigit() for char in line):
            data.append({"month": parts[0], "sales": parts[1], "profit": parts[2]})
    if data:
        df = pd.DataFrame(data)
        return df
    else:
        print("no data load")

# === 3. Load Structured CSV ===
@app.get("/load_structured")
def load_csv():
    if not os.path.exists(STRUCTURED_CSV_PATH):
        return {"error": "No structured.csv found. Upload a file first."}
    df = pd.read_csv(STRUCTURED_CSV_PATH)
    return {"columns": df.columns.tolist(), "preview": df.head().to_dict(orient="records")}

# === 4. Query Schema ===
class Query(BaseModel):
    user_query: str

# === 5. Gemini LLM Code Generation ===
import google.generativeai as genai
GEMINI_API_KEY = "GEMINI_API_KEY"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash-preview-04-17")

def generate_plot_code(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text if response.text else response.candidates[0].content.parts[0].text

# === 6. Generate Graph Code & Plot ===
@app.post("/generate_graph")
def generate_graph(query: Query):
    df = pd.read_csv("structured.csv")
    prompt = f"""
    You are a Python data analysis assistant. Given a pandas DataFrame called `df` with the following columns:
    {df.columns.tolist()}
    Write Python matplotlib/seaborn code using this df to:
    {query.user_query}
    Do not include data loading code. Just use the variable df.
    """

    code = generate_plot_code(prompt)

    if code.startswith("```"):
        code = code.strip("`").split("python")[-1].strip()

    with open("plot_code.py", "w") as f:
        f.write(code)

    try:
        exec_globals = {"df": df, "plt": plt, "pd": pd}
        exec(code, exec_globals)
        plt.savefig("graph.png")
        plt.close()
    except Exception as e:
        tb = traceback.format_exc()
        return {"error": str(e), "traceback": tb, "code": code}

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
