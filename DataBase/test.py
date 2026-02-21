from sqlalchemy.orm import joinedload
from .ORMModel import Encoder
from DataBase.connection_db import engine
from sqlalchemy.orm import Session

session = Session(bind=engine())
# Загружаем все связанные данные одним запросом
encoders = session.query(Encoder)\
    .options(
        joinedload(Encoder.company_rel),
        joinedload(Encoder.type_rel)
    ).all()

for encoder in encoders:
    print(f"""
    Encoder: {encoder.encoder_name}
    Company: {encoder.company_rel.company_name}
    Type: {encoder.type_rel.encoder_type}
    Rotation speed: {encoder.maximum_rotation_speed}
    Weight: {encoder.weight}
    """)