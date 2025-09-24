from abc import ABC, abstractmethod
from typing import Protocol, List, Dict, Any

# ==================== ИНТЕРФЕЙСЫ И ПРОТОКОЛЫ ====================

class ISourceData(Protocol):
    """Протокол для исходных данных привода"""
    max_angl_speed: float
    max_angl_acc: float
    max_stat_torque: float
    max_dyn_torque: float

class IGearData(Protocol):
    """Протокол для данных редуктора"""
    i_nom: float
    m: float
    kpd: float

class IMotorData(Protocol):
    """Протокол для данных двигателя"""
    J: float  # Момент инерции
    name: str

class IPowerCalculator(ABC):
    """Интерфейс для расчета мощности"""
    @abstractmethod
    def calculate_power(self) -> float: ...

class ITorqueCalculator(ABC):
    """Интерфейс для расчета момента"""
    @abstractmethod
    def calculate_torque(self) -> float: ...

class IGearRatioCalculator(ABC):
    """Интерфейс для расчета передаточного отношения"""
    @abstractmethod
    def calculate_gear_ratio(self) -> float: ...

class IDatabaseEditer(ABC):
    """Интерфейс для работы с базой данных"""
    @abstractmethod
    def delete_data(self, table_name: str, data_id: int, data: Dict[str, Any]) -> None: ...
    
    @abstractmethod
    def get_all_data_from_table(self, table_name: str) -> List[Dict[str, Any]]: ...

    @abstractmethod
    def add_data(self, table_name: str, data: Dict[str, Any]) -> None: ...

    @abstractmethod
    def update_data(self, table_name: str, data_id: int, data: Dict[str, Any]) -> None: ...