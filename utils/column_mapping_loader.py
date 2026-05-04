import yaml
from pathlib import Path

def load_column_mapping(model_class=None):
    """
    Загружает маппинг колонок из YAML файла
    """
    config_path = Path('configs/columns_mapping.yaml')
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            mapping = yaml.safe_load(f)
        
        if model_class:
            model_name = model_class.__name__
            return mapping.get(model_name, {})
        
        return mapping
        
    except FileNotFoundError:
        print(f"Файл {config_path} не найден")
        return {}
    except Exception as e:
        print(f"Ошибка загрузки YAML: {e}")
        return {}

def get_russian_name(model_class, column_name):
    """
    Возвращает русское название колонки
    """
    mapping = load_column_mapping(model_class)
    return mapping.get(column_name, column_name)