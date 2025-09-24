from DriverCalculation.Interfaces import IDatabaseEditer
from DataBase.connection_db import engine
from sqlalchemy import text
from typing import Dict, Any, List

class DatabaseRepository(IDatabaseEditer):
    """
    Класс-репозиторий для работы с базой данных PostgreSQL
    Реализует методы для CRUD-операций и подключения к базе
    """

    @staticmethod
    def get_engine():
        """Получить объект engine для подключения к базе данных"""
        return engine()

    def __init__(self):
        self.engine = self.get_engine()

    def delete_data(self, table_name: str, data_id: int, data: Dict[str, Any]) -> None:
        with self.engine.connect() as conn:
            query = text(f"DELETE FROM {table_name} WHERE id = :id")
            conn.execute(query, {"id": data_id})
            conn.commit()

    def get_all_data_from_table(self, table_name: str) -> List[Dict[str, Any]]:
        with self.engine.connect() as conn:
            query = text(f"SELECT * FROM {table_name}")
            result = conn.execute(query)
            return [dict(row._mapping) for row in result.fetchall()]
        
    def add_data(self, table_name: str, data: Dict[str, Any]) -> None:
        with self.engine.connect() as conn:
            columns = ', '.join(data.keys())
            values = ', '.join([f":{k}" for k in data.keys()])
            query = text(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")
            conn.execute(query, data)
            conn.commit()

    def update_data(self, table_name: str, data_id: int, data: Dict[str, Any]) -> None:
        with self.engine.connect() as conn:
            set_clause = ', '.join([f"{k} = :{k}" for k in data.keys()])
            query = text(f"UPDATE {table_name} SET {set_clause} WHERE id = :id")
            data_with_id = dict(data)
            data_with_id["id"] = data_id
            conn.execute(query, data_with_id)
            conn.commit()
