"""plain-words: explain confusing official letters in plain language, locally.

Talks to a local Ollama server, so the letter never leaves your machine.
"""
import argparse
import json
import sys
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3.2"

PROMPT = """You help a friend understand an official letter. Reply in {language}, \
in short, simple sentences (reading level of a 12 year old). Use exactly these headings:

WHAT IS THIS: one sentence.
WHAT DO THEY WANT FROM ME: bullet list.
DEADLINES: dates or "none found". Only dates that appear in the letter.
IS IT URGENT: yes/no and why.
WORDS EXPLAINED: any jargon from the letter, one line each.

If something is unclear, say so. Never invent facts. This is not legal advice.

LETTER:
{letter}
"""


def build_prompt(letter: str, language: str = "English") -> str:
    return PROMPT.format(letter=letter.strip(), language=language)


def explain(letter, model=DEFAULT_MODEL, language="English", url=OLLAMA_URL):
    if not letter.strip():
        raise ValueError("empty letter")
    body = json.dumps(
        {"model": model, "prompt": build_prompt(letter, language), "stream": False}
    ).encode()
    req = urllib.request.Request(url, body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        return json.load(resp)["response"].strip()


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("file", nargs="?", help="text file of the letter (default: stdin)")
    p.add_argument("-m", "--model", default=DEFAULT_MODEL)
    p.add_argument("-l", "--language", default="English")
    a = p.parse_args(argv)
    text = open(a.file, encoding="utf-8").read() if a.file else sys.stdin.read()
    try:
        print(explain(text, a.model, a.language))
    except OSError as e:
        sys.exit(f"Cannot reach Ollama ({e}). Is `ollama serve` running and `ollama pull {a.model}` done?")
    except ValueError as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()
