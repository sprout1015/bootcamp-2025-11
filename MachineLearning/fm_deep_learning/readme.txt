python -m uvicorn main:app --reload

pip install -r requirements.txt

# Windows
pip install torch --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt

# MAC
pip install torch --index-url https://download.pytorch.org/whl/cpu