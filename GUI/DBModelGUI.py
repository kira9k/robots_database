from PySide6.QtCore import QAbstractTableModel, Qt
import yaml
from DataBase.ORMModel import Encoder, EngineDC, Gear


class SQLAlchemyTableModel(QAbstractTableModel):
    def __init__(self, data, columns):
        super().__init__()
        self._data = data  
        self._columns = columns 
        self._column_name = self._load_yaml()
    
    def rowCount(self, parent=None):
        return len(self._data)
    
    def columnCount(self, parent=None):
        return len(self._columns)
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole or not index.isValid():
            return None

        row = self._data[index.row()]
        col_name = self._columns[index.column()]

        # Если строка — объект ORM
        if hasattr(row, '__table__'):
            if isinstance(row, Encoder):
                if col_name == "id_company":
                    return str(row.company_rel.company_name) if row.company_rel else ""
                if col_name == "id_type_encoder":
                    return str(row.type_rel.encoder_type) if row.type_rel else ""
            elif isinstance(row, EngineDC):
                if col_name == "company":
                    return str(row.company_rel.name) if row.company_rel else ""
                if col_name == "type_id":
                    return str(row.engine_type.type_name) if row.engine_type else ""
            elif isinstance(row, Gear):
                if col_name == "gear_company":
                    return str(row.company_rel.name_company) if row.company_rel else ""
                if col_name == "gear_type":
                    return str(row.type_rel.type_gear) if row.type_rel else ""

            # по умолчанию — обычное поле модели
            return str(getattr(row, col_name, ""))

        # Если это dict
        if isinstance(row, dict):
            return str(row.get(col_name, ""))

        # На всякий случай
        return str(row)
    
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            #return self._columns[section]
            return self._column_name.get(self._columns[section], self._columns[section])
        return None
    
    def _load_yaml(self):
        with open('configs/columns_mapping.yaml', "r", encoding="utf-8") as f:
            config_maps = yaml.safe_load(f)
            
        return config_maps
