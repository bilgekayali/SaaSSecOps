from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "schemas"
TARGET = ROOT / "src" / "saassecops" / "schemas"
TARGET.mkdir(parents=True, exist_ok=True)

for source in sorted(SOURCE.glob("*.schema.json")):
    shutil.copyfile(source, TARGET / source.name)
