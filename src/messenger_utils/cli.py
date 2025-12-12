"""
Messengers API Utils: 
CLI interface.

For help use:

Via pure python:
```python -m messenger_utils -h```

Via UV:
``` uv run -m uessenger_utils -h```
"""

from typer import Typer
from rich.console import Console
from messenger_utils.sender import Sender
from messenger_utils import __version__

# Global objects
app = Typer(
    name="Messenger Utils",
    help="Utilites and CLI tool for Telegram & MAX messengers.",
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    rich_markup_mode="rich"
)
console = Console(highlight=False)
ENV_PREFIX = "MESSENGER_UTILS_"

###  CLI commands  ###

@app.command()
def test():
    console.print("test", style="green")


@app.command()
def version():
    console.print(__version__, style="cyan")

    


def main():
    app()

if __name__ == "__main__":
    main()
