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
    fence = None
    for number, line in enumerate(path.read_text().splitlines(), 1):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            marks, info = marker.groups()
            if fence is None:
                fence = (marks, info.strip() in {"sh", "bash", "console", "shell", "zsh"})
            elif marks.startswith(fence[0]) and not info.strip():
                fence = None
            continue
        if not fence or not fence[1]:
            continue
        try:
            words = shlex.split(line.strip().removeprefix("$ "), comments=True)
        except ValueError:
            continue
        command = max((c for c in snapshots if list(c) == words[:len(c)]), key=len, default=None)
        if not command:
            continue
        for word in words[len(command):]:
            if word in ("--", "|", "&&", ";", "||"):
                break
            flag = word.partition("=")[0]
            if re.fullmatch(r"--[\w-]+|-[a-zA-Z]", flag) and flag not in snapshots[command]:
                findings.append(f"{path.name}:{number}: {flag} absent from {' '.join(command)} help")
    return findings

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
