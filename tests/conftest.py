import sys
from pathlib import Path

# プロジェクトルートを sys.path に追加
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
