import typer

from tchat_server.server import ChatServer
from tchat_client.runner import run as client_run

app: typer.Typer = typer.Typer()

@app.command()
def serv():
    try:
        ChatServer().start()
    except Exception as e:
        print( f"[ SERVER ERROR ]: { e }" )

@app.command()
def cli( host: str = typer.Option( None, "--host", help="Override server IP (e.g. 127.0.0.1 for local testing)" ) ):
    try:
        client_run( host=host )
    except Exception as e:
        print( f"[ CLIENT ERROR ]: { e }" )

app()
