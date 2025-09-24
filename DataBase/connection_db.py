from sqlalchemy import create_engine
from sqlalchemy import text
import yaml
import psycopg2
import os

def engine():
    """
    Создает и возвращает SQLAlchemy engine для подключения к базе данных PostgreSQL.
    """
    config_path = os.path.join(os.path.dirname(__file__), '../configs/login_data.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    url = f"postgresql+psycopg2://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database_name']}"
    try:
        eng = create_engine(url=url, echo=False)
        with eng.connect() as conn:
            pass
    except Exception as e:
        raise RuntimeError('Неправильные данные для подключения к базе данных') from e
    return eng
