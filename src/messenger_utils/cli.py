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

# Global objects
app = Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]}
)
console = Console()

###  CLI commands  ###

@app.command()
def test():
    print("test command")


def main():
    app()

if __name__ == "__main__":
    main()
