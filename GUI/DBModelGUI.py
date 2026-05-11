import yaml
from PySide6.QtCore import QAbstractTableModel, Qt
from DataBase.ORMModel import Encoder, EngineDC, Gear

class SQLAlchemyTableModel(QAbstractTableModel):
    def __init__(self, data, columns, model_class=None):
        super().__init__()
        self._data = data  
        self._columns = columns
        self._model_class = model_class
        self._column_mapping = self._load_yaml_mapping()
    
    def rowCount(self, parent=None):
        return len(self._data) if self._data else 0
    
    def columnCount(self, parent=None):
        return len(self._columns) if self._columns else 0
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole or not index.isValid():
            return None

        if not self._data or index.row() >= len(self._data):
            return None
            
        row = self._data[index.row()]
        col_name = self._columns[index.column()]

        # Если строка — объект ORM
        if hasattr(row, '__table__'):
            # Обработка связанных полей для Encoder
            if isinstance(row, Encoder):
                if col_name == "id_company":
                    return str(row.company_rel.company_name) if row.company_rel else ""
                if col_name == "id_type_encoder":
                    return str(row.type_rel.encoder_type) if row.type_rel else ""
                    
            # Обработка связанных полей для EngineDC
            elif isinstance(row, EngineDC):
                if col_name == "company":
                    return str(row.company_rel.name) if row.company_rel else ""
                if col_name == "type_id":
                    return str(row.engine_type.type_name) if row.engine_type else ""
                    
            # Обработка связанных полей для Gear
            elif isinstance(row, Gear):
                if col_name == "gear_company":
                    return str(row.company_rel.name_company) if row.company_rel else ""
                if col_name == "gear_type":
                    return str(row.type_rel.type_gear) if row.type_rel else ""
                    
            # Обработка связанных полей для Result
            # elif isinstance(row, Result):
            #     if col_name == "id_engine":
            #         return str(row.engine_rel.model) if row.engine_rel else ""
            #     if col_name == "id_gear":
            #         return str(row.gear_rel.gear_name) if row.gear_rel else ""
            #     if col_name == "id_encoder":
            #         return str(row.encoder_rel.encoder_name) if row.encoder_rel else ""

            # по умолчанию — обычное поле модели
            value = getattr(row, col_name, "")
            return str(value) if value is not None else ""

        # Если это dict
        if isinstance(row, dict):
            value = row.get(col_name, "")
            return str(value) if value is not None else ""

        # На всякий случай
        return str(row) if row is not None else ""
    
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            if section < len(self._columns):
                eng_name = self._columns[section]
                # Получаем русское название из маппинга для конкретной модели
                if self._model_class and self._column_mapping:
                    model_name = self._model_class.__name__
                    if model_name in self._column_mapping:
                        return self._column_mapping[model_name].get(eng_name, eng_name)
                return eng_name
        return None
    
    def _load_yaml_mapping(self):
        """Загружает маппинг из YAML файла"""
        try:
            with open('configs/columns_mapping.yaml', "r", encoding="utf-8") as f:
                config_maps = yaml.safe_load(f)
            return config_maps
        except FileNotFoundError:
            print("Файл configs/columns_mapping.yaml не найден")
            return {}
        except Exception as e:
            print(f"Ошибка загрузки YAML: {e}")
            return {}