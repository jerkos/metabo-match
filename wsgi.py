from metabomatch.app import create_app
from metabomatch.configs.default import DefaultConfig as Config


flaskbb = create_app(Config)


if __name__ == "__main__":
    flaskbb.run()
