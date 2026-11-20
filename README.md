# CLI Docs Check

![CLI Docs Check — Validate shell examples against saved help.](banner.webp)

[Русский](README.ru.md) · [Release notes](https://github.com/TONstories/cli-docs-check/releases) · [0BSD license](LICENSE)

Validate shell examples against saved help. Capture the help output of the CLI version you intend to document. Save top-level help as TOOL.txt and nested help as TOOL+COMMAND.txt. Keep these snapshots under version control so that a reviewer can see which interface the examples target. Pass a single Markdown file during editing, or point the checker at the documentation directory before a release. The directory scan reads Markdown one line at a time and shares the command index across files.

## Try the included example

Requires Python 3.9 or later. The example intentionally includes a finding and exits with status 1.

```sh
git clone https://github.com/TONstories/cli-docs-check.git
cd cli-docs-check
python3 check.py examples/usage.md --help-dir examples/help
```

```text
usage.md:4: --out absent from pack build help
```

## Checking a documentation tree

```sh
python3 check.py docs/ --help-dir examples/help --json
```

A diagnostic identifies the document, line, command and missing option. Check the snapshot before editing the example: a renamed flag and an outdated snapshot can produce the same symptom. The tool ignores unrelated commands and never executes fenced code. It recognizes standalone shell invocations; shell scripts with substitutions, continuations or combined short options need a separate execution test.

## CI and coding agents

Use the JSON report when consuming results programmatically. Its `findings` array contains one diagnostic per detected issue. Exit 0 means the implemented rules passed, exit 1 means review the findings, and exit 2 means the command or input could not be processed. Capture stderr separately for invocation errors. Run `python3 test_example.py` to exercise the bundled fixture and a corrected input. Agent setup is documented in [AGENTS.md](AGENTS.md).

## Performance

On a local Apple Silicon Mac, checking 3,000 command lines against 300 saved help files took **0.069 s** versus **0.168 s** with v0.1.0. Both numbers are the median of three paired CLI runs with identical local input, including interpreter startup. Timing varies with hardware, storage and input composition.

## Maintainer

Built by TON Stories, a marketplace connecting advertisers with creators for Telegram Stories campaigns. [TON Stories](https://tonstories.com/?utm_source=github&utm_medium=referral&utm_campaign=open_source&utm_content=cli-docs-check) · [Telegram](https://t.me/TON_Storiesbot?start=gh_cli_docs_check)
