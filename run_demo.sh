# Run the Autocorrect Prototype Demo

echo "1. Training N-Gram Model..."
python project/src/ngram_module.py --train project/data/corpus.txt --out project/models/ngram_counts.pkl

echo "2. Starting FastAPI Backend..."
# Run in background or just run it. For simplicity in script, we just run it. 
# User can't use the shell effectively if it blocks, but for a "demo script" it's standard to block.
echo "   (Press Ctrl+C to stop)"
python project/main.py
