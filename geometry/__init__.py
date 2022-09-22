from .config import Config

def run():
    config = Config.triangle()
    config.run(50)

