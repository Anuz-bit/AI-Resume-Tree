import os
import shutil
import uuid
import json
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from m1_parser.resume_parser import ResumeParser
from m2_tree.tree_builder import ResumeTreeBuilder
from m3_jd.jd_parser import JDParser
from m4_eval.eval_agent import EvaluationAgent

app = FastAPI()

# Enable CORS so the separate frontend can talk to us
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure data directories exist
DATA_DIRS = ["data/tmp", "data/parsed", "data/trees", "data/evals"]
for d in DATA_DIRS:
    os.makedirs(d, exist_ok=True)

@app.post("/evaluate")
async def evaluate(resume: UploadFile = File(...), jd_text: str = Form(...)):
    # 1. Save uploaded file temporarily
    file_id = str(uuid.uuid4())
    ext = resume.filename.split('.')[-1]
    tmp_path = f"data/tmp/{file_id}.{ext}"
    
    with open(tmp_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)
    
    try:
        # 2. Run ResumeTree Pipeline
        print(f"[{file_id}] Parsing Resume...")
        parser = ResumeParser()
        
        # Extract raw text for the frontend preview
        raw_text, _ = parser._extract_text(tmp_path)
        
        resume_json = parser.parse(tmp_path)
        
        print(f"[{file_id}] Building Resume Tree...")
        builder = ResumeTreeBuilder()
        resume_tree = builder.build_tree(resume_json)
        
        print(f"[{file_id}] Parsing JD...")
        tmp_jd_path = f"data/tmp/{file_id}_jd.txt"
        with open(tmp_jd_path, "w", encoding="utf-8") as f:
            f.write(jd_text)
            
        jd_parser = JDParser()
        jd_tree = jd_parser.parse(tmp_jd_path)
        
        print(f"[{file_id}] Evaluating...")
        agent = EvaluationAgent()
        result = agent.evaluate(resume_tree, jd_tree)
        result["resume_tree"] = resume_tree
        result["resume_json"] = resume_json
        result["resume_raw_text"] = raw_text
        
        # 3. Clean up and return
        os.remove(tmp_path)
        if os.path.exists(tmp_jd_path):
            os.remove(tmp_jd_path)
        return result

    except Exception as e:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        
        # Clean up jd text if it exists
        tmp_jd_path = f"data/tmp/{file_id}_jd.txt"
        if os.path.exists(tmp_jd_path):
            os.remove(tmp_jd_path)
            
        print(f"Error during evaluation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/results/{eval_id}")
async def get_results(eval_id: str):
    path = f"data/evals/{eval_id}.json"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Evaluation results not found")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
