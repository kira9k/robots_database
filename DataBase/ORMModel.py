from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Float, Numeric, LargeBinary, ForeignKey

Base = declarative_base()

class EngineType(Base):
    """ORM модель типа двигателя"""
    __tablename__ = 'engine_types'
    id_engine = Column(Integer, primary_key=True)
    type_name = Column(String)


class EngineCompany(Base):
    """ORM модель компании производителя двигателя"""
    __tablename__ = 'engine_companies'
    id_company = Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(String)


class EngineDC(Base):
    """ORM модель двигателя постоянного тока"""
    __tablename__ = 'engine_dc'
    id = Column(Integer, primary_key=True)
    model = Column(String)
    p_nom = Column(Float)
    m_nom = Column(Float)
    n_nom = Column(Float)
    u_nom = Column(Float)
    i_nom = Column(Float)
    r_nom = Column(Float)
    j_nom = Column(Float)
    m = Column(Float)
    price = Column(Numeric(9, 2))
    drawing = Column(LargeBinary)
    company = Column(Integer, ForeignKey('engine_companies.id_company'))
    type_id = Column(Integer, ForeignKey('engine_types.id_engine'))

    company_rel = relationship('EngineCompany')
    engine_type = relationship('EngineType')   


class GearType(Base):
    """ORM модель типа редуктора"""
    __tablename__ = 'gear_types'
    type_gear_id = Column(Integer, primary_key=True)
    type_gear = Column(String)


class GearCompany(Base):
    """ORM модель компании производителя редуктора"""
    __tablename__ = 'gear_companies'
    company_id = Column(Integer, primary_key=True)
    name_company = Column(String)
    country = Column(String)


class Gear(Base):
    """ORM модель редуктора"""
    __tablename__ = 'gears'
    gear_id = Column(Integer, primary_key=True)
    gear_name = Column(String)
    gear_company = Column(Integer, ForeignKey('gear_companies.company_id'))
    gear_type = Column(Integer, ForeignKey('gear_types.type_gear_id'))
    i = Column(Float)
    speed_norm = Column(Float)
    c = Column(Float)
    clearance = Column(Float)
    torque_nom = Column(Float)
    inertial_torque = Column(Float)
    mass = Column(Float)
    price = Column(Numeric(9, 2))
    drawing = Column(LargeBinary)
    efficiency = Column(Float)

    company_rel = relationship('GearCompany')
    type_rel = relationship('GearType')
