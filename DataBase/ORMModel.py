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

class EncoderType(Base):
    """ORM модель типа энкодера"""
    __tablename__ = 'type_encoder'
    id_type = Column(Integer, primary_key=True)
    encoder_type = Column(String)

class EncoderCompany(Base):
    """ORM модель компании производителя энкодера"""
    __tablename__ = 'company_encoder'
    id_company_encoder = Column(Integer, primary_key=True)
    company_name = Column(String)
    company_country = Column(String)

class Encoder(Base):
    """ORM модель энкодера"""
    __tablename__ = 'encoder'
    id_encoder = Column(Integer, primary_key=True)
    encoder_name = Column(String)
    id_company = Column(Integer, ForeignKey('company_encoder.id_company_encoder'))
    id_type_encoder = Column(Integer, ForeignKey('type_encoder.id_type'))
    shaft_diameter = Column(Float)
    rotor_breakway_torque = Column(Float)
    rotor_moment_of_inertia = Column(Float)
    maximum_rotation_speed = Column(Float)
    supply_voltage = Column(Float)
    lines_count = Column(Integer)
    weight = Column(Float)
    drawing = Column(LargeBinary)
    price = Column(Numeric(9, 2))

    company_rel = relationship('EncoderCompany')
    type_rel = relationship('EncoderType')