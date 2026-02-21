"""Стратегии проверки."""

from .base import IThermalVerificationStrategy
from .motor_torque_strategy import MotorTorqueVerificationStrategy
#from .safety_factor_strategy import SafetyFactorVerificationStrategy

__all__ = [
    'IThermalVerificationStrategy',
    'MotorTorqueVerificationStrategy', 
#    'SafetyFactorVerificationStrategy'
]