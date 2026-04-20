import sys
   from pathlib import Path
   
   # Add the repo root to Python's path so `from app.xxx import yyy` works
   sys.path.insert(0, str(Path(__file__).parent))
   
   from app.main import main
   
   if __name__ == "__main__":
       main()
