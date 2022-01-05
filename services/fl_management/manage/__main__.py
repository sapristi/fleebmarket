import typer

from pathlib import Path
from dotenv import load_dotenv

from . import alerts
from . import services

app = typer.Typer(add_completion=False, no_args_is_help=True)
app.add_typer(alerts.app, name="alerts")
app.add_typer(services.app, name="services")


default_dotenv = Path(__file__).parent.parent.parent.parent / ".env"

@app.callback()
def load_dotenv_callback(
    dotenv_path: Path = typer.Option(
        default_dotenv, exists=True, file_okay=True, dir_okay=False),
):
    load_dotenv(dotenv_path=dotenv_path)


if __name__ == "__main__":
    app()
