from abc import ABC, abstractmethod

from .models import PropagationInput, PropagationResult, TrafficInput, TrafficResult


class PropagationCalculatorPort(ABC):
    @abstractmethod
    def calculate(self, params: PropagationInput) -> PropagationResult:
        raise NotImplementedError


class TrafficEstimatorPort(ABC):
    @abstractmethod
    def estimate_blocking(self, params: TrafficInput) -> TrafficResult:
        raise NotImplementedError
