from src.configuration import Config
from src.runner import Runner

if __name__ == '__main__':
    config_path = 'resources/config.yaml'
    config = Config.load_config(config_path)

    runner = Runner(config)
    runner.run()
