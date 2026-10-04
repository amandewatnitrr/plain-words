# plain-words

Built for a friend who gets official letters in a language they're still learning.
Paste the letter, get a plain-language summary: what it is, what they want, deadlines, jargon explained.

Runs on an **open-weight model through local Ollama**. Letters hold tax, visa, and medical details;
none of it is sent to a cloud API. Open weights are what make that possible.

*Hacktoberfest Weekend Challenge: Build for a Friend.*

## Use

```bash
ollama pull llama3.2
python3 plainwords.py examples/tax_notice.txt
python3 plainwords.py -l Hindi -m qwen2.5 letter.txt
cat letter.txt | python3 plainwords.py
```

No dependencies beyond Python 3.8+. Tests: `python3 -m unittest`.

Not legal advice. Always check deadlines against the original letter.

MIT licensed.
