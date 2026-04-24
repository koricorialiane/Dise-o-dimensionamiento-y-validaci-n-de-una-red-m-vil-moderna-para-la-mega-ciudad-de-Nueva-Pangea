import math

from app.domain.ports import TrafficEstimatorPort
from app.domain.models import TrafficInput, TrafficResult


class ErlangBAdapter(TrafficEstimatorPort):
    def estimate_blocking(self, params: TrafficInput) -> TrafficResult:
        a = params.traffic_load_erlang
        u = params.channels
        numerator = a**u / math.factorial(u)
        denominator = sum(a**k / math.factorial(k) for k in range(u + 1))
        blocking = numerator / denominator
        return TrafficResult(
            blocking_probability=round(blocking, 6),
            accepted=blocking <= 0.02,
        )
