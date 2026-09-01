import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WHY_HEADING = re.compile(r"^#{1,6}\s+Why(?:\s|$)", re.IGNORECASE)


class RepositoryContractTests(unittest.TestCase):
    def test_public_and_packaged_schemas_are_identical(self):
        public = ROOT / "schemas"
        packaged = ROOT / "src" / "saassecops" / "schemas"
        names = sorted(path.name for path in public.glob("*.schema.json"))
        self.assertEqual(names, sorted(path.name for path in packaged.glob("*.schema.json")))
        for name in names:
            self.assertEqual((public / name).read_bytes(), (packaged / name).read_bytes(), name)

    def test_markdown_does_not_use_why_headings(self):
        markdown_files = [ROOT / "README.md", ROOT / "ROADMAP.md", ROOT / "COMPATIBILITY.md"]
        markdown_files.extend((ROOT / "docs").rglob("*.md"))
        offenders = []
        for path in markdown_files:
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                if WHY_HEADING.match(line):
                    offenders.append(f"{path.relative_to(ROOT)}:{number}:{line}")
        self.assertEqual(offenders, [], "Avoid `Why ...` Markdown headings: " + "; ".join(offenders))


if __name__ == "__main__":
    unittest.main()
