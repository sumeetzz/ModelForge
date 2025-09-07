import click
from main import main as train_pipeline

@click.group()
def cli():
    pass

@cli.command()
@click.option('--config', default='configs/config.yaml', help='Path to config')
def train(config):
    """Train and register model"""
    train_pipeline()

@cli.command()
@click.option('--port', default=8000, help='Port to serve API')
def serve(port):
    """Start inference API"""
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)

if __name__ == '__main__':
    cli()
