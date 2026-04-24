from dataclasses import dataclass

@dataclass
class PropagationInput:
    frequency_mhz: float
    base_height_m: float
    mobile_height_m: float
    distance_km: float
    tx_power_dbm: float
    tx_gain_dbi: float
    rx_gain_dbi: float
    receiver_sensitivity_dbm: float

@dataclass
class PropagationResult:
    path_loss_db: float
    received_power_dbm: float
    coverage_ok: bool
    margin_db: float

@dataclass
class TrafficInput:
    traffic_load_erlang: float
    channels: int

@dataclass
class TrafficResult:
    blocking_probability: float
    accepted: bool
