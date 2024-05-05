from pathlib import Path

BASE_DIR: Path = Path(__file__).parent.parent.parent.resolve()
DATA_DIR: Path = BASE_DIR / "data"
RAW_DATA_DIR: Path = DATA_DIR / "raw"
PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
OUTPUT_DIR: Path = BASE_DIR / "output"
LOG_DIR: Path = OUTPUT_DIR / "logs"

INPUT_FNAME: str = "iris.csv"

TITLE: str = "Iris Dataset Analysis"
AUTHORS: list[str] = ["Michał Górski"]
