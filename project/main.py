import uvicorn
import os
import sys

# Add the parent directory (project root) to Python path
# This ensures 'project' module can be imported
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

if __name__ == "__main__":
    print("Starting Autocorrect Keyboard Application...")
    print("Ensure you have trained the model first!")
    print("Run: python project/src/ngram_module.py --train project/data/corpus.txt --out project/models/ngram_counts.pkl")
    print("------------------------------------------------")
    print("OPEN BROWSER TO: http://127.0.0.1:8000")
    print("------------------------------------------------")
    
    # Run Uvicorn
    # 'project.src.api:app' refers to the FastAPI app instance in api.py
    uvicorn.run("project.src.api:app", host="127.0.0.1", port=8000, reload=True)
