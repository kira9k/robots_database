from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Float, Numeric, ForeignKey


Base = declarative_base()

class Utils(Base):
    """ORM модель для хранения различных параметров"""
    __tablename__ = 'utils'
    id = Column(Integer, primary_key=True, autoincrement=True)
    A_e = Column(Float)
    omega_e = Column(Float)
    dyn_error = Column(Float)
    stat_error = Column(Float)

class CoefRegulators(Base):
    """ORM модель для хранения коэффициентов"""
    __tablename__ = 'coef_regulators'
    id = Column(Integer, primary_key=True, autoincrement=True)
    k_dc = Column(Float)
    k_c = Column(Float)
    k_ci = Column(Float)
    k_ds = Column(Float)
    k_s = Column(Float)
    k_si = Column(Float)
    k_da = Column(Float)
    k_a = Column(Float)
    k_ai = Column(Float)
    k_pwm = Column(Float)
    T_pwm = Column(Float)
    k_feedforward = Column(Float)

class SourceData(Base):
    """ORM модель для хранения исходных данных проектирования"""
    __tablename__ = 'source_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    max_speed = Column(Float)
    max_acc = Column(Float)
    max_speed_work = Column(Float)
    acc_duration = Column(Float)
    rel_duration = Column(Float)
    max_torque = Column(Float)
    max_inertia_torque = Column(Float)
    max_error = Column(Float)
    transition_time = Column(Float)

class Result(Base):
    """ORM модель для хранения результатов проектирования"""
    __tablename__ = 'result'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_engine = Column(Integer, ForeignKey('engine_dc.id'))
    id_gear = Column(Integer, ForeignKey('gears.id'))
    id_encoder = Column(Integer, ForeignKey('encoder.id'))
    id_source_data = Column(Integer, ForeignKey('source_data.id'))
    id_coef_regulators = Column(Integer, ForeignKey('coef_regulators.id'))
    id_utils = Column(Integer, ForeignKey('utils.id'))

    engine_rel = relationship('EngineDC', foreign_keys=[id_engine])
    gear_rel = relationship('Gear', foreign_keys=[id_gear])
    encoder_rel = relationship('Encoder', foreign_keys=[id_encoder])
    source_data_rel = relationship('SourceData', foreign_keys=[id_source_data])
    coef_regulators_rel = relationship('CoefRegulators', foreign_keys=[id_coef_regulators])
    utils_rel = relationship('Utils', foreign_keys=[id_utils])

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
    id = Column(Integer, primary_key=True, autoincrement=True)
    model = Column(String)
    p_nom = Column(Float)
    m_nom = Column(Float)
    n_nom = Column(Float)
    u_nom = Column(Float)
    i_nom = Column(Float)
    r_nom = Column(Float)
    j_nom = Column(Float)
    l_a = Column(Float)
    max_current = Column(Float)
    m = Column(Float)
    price = Column(Numeric(9, 2))
    drawing = Column(String)
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
    id = Column(Integer, primary_key=True, autoincrement=True)
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
    drawing = Column(String)
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
    id = Column(Integer, primary_key=True, autoincrement=True)
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
    drawing = Column(String)
    price = Column(Numeric(9, 2))

    company_rel = relationship('EncoderCompany')
    type_rel = relationship('EncoderType')