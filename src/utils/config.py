import yaml
import os

def load_email_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'config', 'email_config.yml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)