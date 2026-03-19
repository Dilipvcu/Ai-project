import logging.config
import os

# Configure logging
log_config_path = os.path.join(os.path.dirname(__file__), 'logging.yaml')

if os.path.exists(log_config_path):
    import yaml
    with open(log_config_path, 'r') as f:
        config = yaml.safe_load(f)
        logging.config.dictConfig(config)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
