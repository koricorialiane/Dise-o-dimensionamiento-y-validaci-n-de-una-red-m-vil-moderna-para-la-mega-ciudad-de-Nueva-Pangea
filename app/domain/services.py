from .ports import PropagationCalculatorPort, TrafficEstimatorPort
from .models import PropagationInput, TrafficInput


class RadioPlanningService:
    def __init__(self, propagation_calculator: PropagationCalculatorPort, traffic_estimator: TrafficEstimatorPort):
        self.propagation_calculator = propagation_calculator
        self.traffic_estimator = traffic_estimator

    def calculate_coverage(self, params: PropagationInput):
        return self.propagation_calculator.calculate(params)

    def calculate_blocking(self, params: TrafficInput):
        return self.traffic_estimator.estimate_blocking(params)
