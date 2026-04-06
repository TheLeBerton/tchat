import typer

import server
import client

app: typer.Typer = typer.Typer()

@app.command()
def serv():
    try:
        server.run()
    except Exception as e:
        print( f"[ SERVER ERROR ]: { e }" )

@app.command()
def cli():
    try:
        client.run()
    except Exception as e:
        print( f"[ CLIENT ERROR ]: { e }" )

app()
