#!/usr/bin/env python3
"""Turn store/privacy-policy.md into privacy.html.

Deliberately tiny: the policy is the only markdown we publish, it uses four
constructs (h1/h2, paragraphs, **bold**, links), and a dependency-free script
means the page can be rebuilt on any machine that has python.
"""
import html, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
SRC = HERE.parent / "privacy-policy.md"
EMAIL = sys.argv[1] if len(sys.argv) > 1 else "momenti.app@proton.me"

TEMPLATE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Momenti</title>
<meta name="description" content="Политика конфиденциальности приложения Momenti — журнала первых лет ребёнка.">
<link rel="stylesheet" href="style.css">
</head>
<body>
<main>
<header>
  <p class="mark">Momenti</p>
  <h1>{title}</h1>
  <p class="meta">{date}</p>
</header>
{body}
<footer>
  <a href="./">Поддержка</a><a href="privacy.html">Конфиденциальность</a>
</footer>
</main>
</body>
</html>
"""


def inline(text):
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return text


def main():
    lines = SRC.read_text().splitlines()
    title, date, out, buf = "", "", [], []

    def flush():
        if buf:
            out.append("<p>" + inline(" ".join(buf)) + "</p>")
            buf.clear()

    for line in lines:
        line = line.rstrip()
        if line.startswith("# "):
            flush()
            title = line[2:].replace("Момenti", "Momenti").removeprefix("Политика конфиденциальности ").strip() or line[2:]
            title = "Политика конфиденциальности"
        elif line.startswith("## "):
            flush()
            out.append(f"<h2>{inline(line[3:])}</h2>")
        elif line.startswith("Дата последнего изменения"):
            flush()
            date = line
        elif not line:
            flush()
        else:
            buf.append(line)
    flush()

    body = "\n".join(out).replace("[укажите почту поддержки]", f'<a href="mailto:{EMAIL}">{EMAIL}</a>')
    (HERE / "privacy.html").write_text(
        TEMPLATE.format(title=title, date=html.escape(date), body=body)
    )
    print("privacy.html written")


main()
