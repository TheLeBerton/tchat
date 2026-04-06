import typer

from chat.server.server import ChatServer
from chat.client.runner import run as client_run

app: typer.Typer = typer.Typer()

@app.command()
def serv():
    try:
        ChatServer().start()
    except Exception as e:
        print( f"[ SERVER ERROR ]: { e }" )

@app.command()
def cli():
    try:
        client_run()
    except Exception as e:
        print( f"[ CLIENT ERROR ]: { e }" )

app()
