# CLI Docs Check

[Русский](README.ru.md)

Find stale flags in fenced shell examples using saved help output.

![Example report](example.png)

```sh
git clone https://github.com/TONstories/cli-docs-check.git
cd cli-docs-check
python3 check.py examples/usage.md --help-dir examples/help
```

```text
usage.md:4: --out absent from pack build help
```

Save help in tool.txt and tool+subcommand.txt. Each option declaration starts with a dash. The longest matching command wins. Supports one command per line in shell fences, standalone short options and long options with optional =value. Shell expansion, grouped short flags and multiline commands are outside this version.

Python 3.9+. Add --json for structured results. Exit codes: 0 passes the implemented checks, 1 has findings, 2 indicates an input or invocation error.

0.039 s · macOS · Python · bundled example · single local run.

Built by TON Stories, a marketplace connecting advertisers with creators for Telegram Stories campaigns. [TON Stories](https://tonstories.com/?utm_source=github&utm_medium=referral&utm_campaign=open_source&utm_content=cli-docs-check) · [Telegram](https://t.me/TON_Storiesbot?start=gh_cli_docs_check)
