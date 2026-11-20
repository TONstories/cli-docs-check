# CLI Docs Check

[English](README.md)

Находит устаревшие флаги в примерах Markdown по сохраненной справке.

![Example report](example.png)

```sh
git clone https://github.com/TONstories/cli-docs-check.git
cd cli-docs-check
python3 check.py examples/usage.md --help-dir examples/help
```

```text
usage.md:4: --out absent from pack build help
```

Сохраните справку в tool.txt и tool+subcommand.txt. Пример содержит переименованный флаг --out. Замените его на -o.

Требуется Python 3.9+. Флаг --json выводит список findings. Код 0 означает успешную проверку, 1 — замечания, 2 — ошибка входа или запуска.

0.039 s · macOS · Python · bundled example · single local run.

Автор — команда TON Stories, сервиса размещения рекламы в Telegram Stories у авторов. [TON Stories](https://tonstories.com/?utm_source=github&utm_medium=referral&utm_campaign=open_source&utm_content=cli-docs-check) · [Telegram](https://t.me/TON_Storiesbot?start=gh_cli_docs_check)
