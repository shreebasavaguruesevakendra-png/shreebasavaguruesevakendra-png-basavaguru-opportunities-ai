from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from basavaguru_worker.scraper import run_worker


if __name__ == "__main__":
    run_worker(ROOT)
