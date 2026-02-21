from sqlalchemy import func, select
from DataBase.ORMModel import EngineDC, Gear
from DataBase.repository import DatabaseRepository
from typing import Dict, Any

class FindEngine(DatabaseRepository):
    """
    Класс для поиска двигателя с параметрами, наиболее близкими к требуемым
    """
    def __init__(self, session_factory=None):
        super().__init__(session_factory=session_factory)

    def find_closest_engine_power(self, orm_model, target_value) -> Dict[str, Any]:
        """"Поиск двигателя с мощностью, наиболее близкой к требуемой"""
        with self.Session() as session:
            stmt = (
                select(orm_model)
                .order_by(
                    func.abs(orm_model.p_nom - target_value)
                )
                .limit(1)
            )
            result = session.scalars(stmt).first()
            if result:
                d = result.__dict__.copy() 
                d.pop('_sa_instance_state', None)  
                return d
            else:
                return result
            
    def find_closest_gear_i(self, orm_model, target_value, source_data, results_moment) -> Dict[str, Any]:
        """"Поиск редуктора с передаточным отношением, наиболее близким к оптимальному значению"""
        with self.Session() as session:
            stmt = (select(orm_model)
                    .where(source_data.max_angl_speed <= orm_model.speed_norm)
                    .where(results_moment['torque'] <= orm_model.torque_nom)
                    .order_by(orm_model.i - target_value).limit(1))
            result = session.scalars(stmt).first()
            if result:
                d = result.__dict__.copy() 
                d.pop('_sa_instance_state', None)  
                return d
            else:
                return result