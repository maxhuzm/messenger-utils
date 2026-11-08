# AGENTS.md

Utilities + CLI for MAX and Telegram bots, published to PyPI as `messenger-utils`.

## Commands

Always go through `uv` (the system `python` is 3.10, the project needs >= 3.12; `.python-version` pins 3.13).

```sh
uv sync                                  # install deps + self into .venv
uv run python -m pytest                  # run tests (see env vars below)
uv run python -m pytest tests/test_receiver.py -q
uv run python -m pytest tests/test_models.py::test_create_keyboard
uv run -m messenger_utils --help         # CLI
uv run -m messenger_utils version
uv build                                 # sdist + wheel into dist/
```

Use `uv run python -m pytest`: bare `uv run pytest` fails here with `Failed to canonicalize script path` (pytest is only installed as a module/console-script shim). `ruff` isn't installed at all. There is **no** linter, formatter, typechecker, or CI test job in this repo (the only workflow builds and publishes); do not invent configs for them.

## Tests

- `tests/__init__.py` raises on import unless `MESSENGER_UTILS_MAX_BOT_TOKEN` is set, and `tests/test_sender.py` raises unless `MESSENGER_UTILS_CHAT_ID` is set — so even *collecting* the suite needs both variables. Dummy values work for offline tests:
  ```powershell
  $env:MESSENGER_UTILS_MAX_BOT_TOKEN="dummy"; $env:MESSENGER_UTILS_CHAT_ID="123"
  ```
- Offline-safe (pass with dummy tokens): `tests/test_receiver.py` (webhook parsing against inline fixtures), most of `tests/test_models.py`, keyboard serialization.
- `tests/test_cli.py::test_cli_version` is excluded by `@pytest.mark.skip` ("control chars for color ruin the test"). Don't re-enable it as part of unrelated work; Rich adds ANSI codes to the captured output.
- Hits the live MAX API (needs a real token): `tests/test_cli.py::test_cli_remove_command`, and `tests/test_sender.py` which is additionally gated behind `RUN_IGNORED=true`. Treat failures there as network/credential noise, not regressions.
- Known failure at HEAD: `tests/test_models.py::test_button_types` calls `OpenAppButton(text="test")`, but `web_app` is required. Don't "fix" unrelated tests to make the suite green silently.
- Tests import as a package (`from . import MAX_TOKEN`); run pytest from the repo root.

## Layout

- `src/messenger_utils/` — src layout, built by `uv_build`.
  - `sender.py` — `Sender` ABC; async `get/post/patch/delete` helpers, one `httpx.AsyncClient` per call, auth header is the raw bot token (no `Bearer`).
  - `receiver.py` — `Receiver` ABC (generic over webhook event type) plus handler-registration decorators.
  - `max/` — `MaxSender`, `MaxReceiver`, `MaxKeyboard` + button dataclasses.
  - `models/max_webhook_event.py` — dataclasses for MAX webhook events.
  - `cli.py` — Typer app; `__main__.py` calls `main()`.
- `src/messenger_utils/telegram/__init__.py` is empty and every `--messenger telegram` branch in `cli.py` is a `TODO` no-op. README advertises Telegram, but MAX is the only implemented backend.

## Gotchas

- `Receiver` decorators (`@MaxReceiver.command("x")`, `@MaxReceiver.callback("token")`, `@MaxReceiver.create_message`, …) are **classmethods writing to class-level dicts/attributes**. Handlers are therefore global per subclass, shared by all instances, and take precedence over any per-instance state. Handlers are `await`ed, so they must be `async`.
- `MaxReceiver.parse_webhook()` only builds the event; `process_webhook()` dispatches it. `process_webhook()` calls `parse_webhook()` itself if the event hasn't been parsed yet.
- `MaxReceiver.__init__` already validates `update_type` and raises `ValueError`; body-shape mismatches raise `ValueError` later in `parse_webhook()` (structural `match`).
- MAX API specifics: base `https://platform-api.max.ru` (`max/__init__.py`); message target is a query param (`url_params={"chat_id": target}`), not a body field; message bodies are sent as `format: "markdown"`.
- `MaxSender.send_message` is the current API. `send_text_message` / `send_keyboard_message` / `send_image_message` are deprecated (they emit `DeprecationWarning`) yet `cli.py`'s `send` command still calls `send_text_message`.
- `MaxKeyboard.to_json()` / button `to_json()` emit exactly-formatted JSON (spaces after `:` and `,`, `btn_type` renamed to `type`, `None` fields dropped); tests assert byte-identical strings. Any serializer change breaks `tests/test_models.py`.

## Release

- Version appears in **three** places and must stay in sync: `pyproject.toml` `project.version`, `src/messenger_utils/__init__.py` `__version__`, and the `CHANGELOG.md` entry.
- Add a Keep-a-Changelog entry under a new `## [x.y.z] - YYYY-MM-DD` heading.
- Publishing is tag-driven: pushing a tag matching `v[0-9].[0-9]*` runs `.github/workflows/publish-pypi.yml` (`uv build` + `uv publish` via PyPI Trusted Publisher). No token secrets are configured.
- Git remotes: `github` (canonical, `maxhuzm/messenger-utils`) and `gitverse` (mirror, also has a `dev` branch).
