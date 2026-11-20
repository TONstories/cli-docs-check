"""Compare standalone fenced shell commands with saved help snapshots."""
import re
import shlex


def inspect(path, help_dir):
    snapshots = {}
    for item in help_dir.glob("*.txt"):
        command = tuple(item.stem.split("+"))
        flags = set()
        for line in item.read_text().splitlines():
            if line.lstrip().startswith("-"):
                flags.update(re.findall(r"(?<![\w-])--?[\w][\w-]*", re.split(r"\s{2,}", line.strip())[0]))
        snapshots[command] = flags
    if not snapshots:
        raise ValueError("expected help-dir/tool.txt or tool+command.txt")
    findings = []
    lengths = sorted({len(command) for command in snapshots}, reverse=True)
    documents = sorted(path.rglob("*.md")) if path.is_dir() else [path]
    if not documents:
        raise ValueError("directory contains no Markdown files")
    for document in documents:
        label = document.relative_to(path) if path.is_dir() else document.name
        with document.open(encoding="utf-8") as lines:
            findings.extend(scan(lines, label, snapshots, lengths))
    return findings


def scan(lines, label, snapshots, lengths):
    fence = None
    for number, line in enumerate(lines, 1):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            marks, info = marker.groups()
            if fence is None:
                language = info.split(maxsplit=1)
                fence = (marks, bool(language) and language[0] in {"sh", "bash", "console", "shell", "zsh"})
            elif marks.startswith(fence[0]) and not info.strip():
                fence = None
            continue
        if not fence or not fence[1]:
            continue
        if not line.strip():
            continue
        try:
            words = shlex.split(line.strip().removeprefix("$ "), comments=True)
        except ValueError:
            continue
        command = None
        for length in lengths:
            prefix = tuple(words[:length])
            if prefix in snapshots:
                command = prefix
                break
        if not command:
            continue
        for word in words[len(command):]:
            if word in ("--", "|", "&&", ";", "||"):
                break
            flag = word.partition("=")[0]
            if re.fullmatch(r"--[\w-]+|-[a-zA-Z]", flag) and flag not in snapshots[command]:
                yield f"{label}:{number}: {flag} absent from {' '.join(command)} help"

if __name__ == "__main__":
    import argparse
    import json
    import sys
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--help-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        findings = inspect(args.path, args.help_dir)
    except (ValueError, OSError) as error:
        parser.exit(2, f"{error}\n")
    result = {"findings": findings}
    print(json.dumps(result, ensure_ascii=False) if args.json else "\n".join(findings) or "OK: checked rules passed")
    sys.exit(bool(findings))
