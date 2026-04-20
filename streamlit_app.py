import sys
import os
from pathlib import Path

# Ensure the repo root is on sys.path BEFORE any app.* imports
ROOT = Path(__file__).parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Also set working directory so relative paths (like 'app/assets/...') work
os.chdir(ROOT)

from app.main import main

if __name__ == "__main__":
    main()
