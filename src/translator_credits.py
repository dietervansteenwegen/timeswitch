import json
from pathlib import Path


def _candidate_credit_paths() -> list[Path]:
    package_dir = Path(__file__).resolve().parent
    project_root = package_dir.parent

    return [
        package_dir / "CREDITS.json",
        project_root / "po" / "CREDITS.json",
    ]


def get_translator_credits() -> str:
    for credits_path in _candidate_credit_paths():
        try:
            with credits_path.open("r", encoding="utf-8") as handle:
                credits_json = json.load(handle)

            lines = []
            for translator in sorted(credits_json.keys()):
                data = credits_json[translator]
                langs = data["lang"]
                if isinstance(langs, list):
                    langs = ", ".join(sorted(langs))

                line = f"{translator} ({langs})"
                if "url" in data:
                    line += f" {data['url']}"
                elif "email" in data:
                    line += f" <{data['email']}>"
                lines.append(line)

            return "\n".join(lines)
        except Exception:
            continue

    return ""
