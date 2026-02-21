from DataBase.repository import DatabaseRepository
from sqlalchemy import func, select
from typing import Dict, Any
from DataBase.ORMModel import Encoder
from typing import Optional
import math

class FindEncoder(DatabaseRepository):
    """
    Класс для поиска энкодера с параметрами, наиболее близкими к требуемым
    """
    def __init__(self, session_factory=None):
        super().__init__(session_factory=session_factory)
    
    def find_closest_encoder_lines_count_ceil(self, orm_model, target_value, source_data, gear_data) -> Optional[Dict[str, Any]]:
        """
        Поиск энкодера с разрешающей способностью НЕ МЕНЬШЕ целевой,
        """
        with self.Session() as session:
            stmt = (
                select(orm_model)
                .where(orm_model.maximum_rotation_speed >= source_data.max_angl_speed * gear_data.i_nom * 30 / math.pi)
                .where(orm_model.lines_count >= target_value)
                .order_by(orm_model.lines_count)  
                .limit(1)
            )
            
            result = session.scalars(stmt).first()
            
            if result:
                # Конвертируем ORM объект в словарь
                d = result.__dict__.copy() 
                d.pop('_sa_instance_state', None)  
                return d
            
            return None