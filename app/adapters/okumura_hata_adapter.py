import math

from app.domain.ports import PropagationCalculatorPort
from app.domain.models import PropagationInput, PropagationResult


class OkumuraHataAdapter(PropagationCalculatorPort):
    def calculate(self, params: PropagationInput) -> PropagationResult:
        a_hm = 3.2 * (math.log10(11.75 * params.mobile_height_m))**2 - 4.97
        pl = (
            69.55
            + 26.16 * math.log10(params.frequency_mhz)
            - 13.82 * math.log10(params.base_height_m)
            - a_hm
            + (44.9 - 6.55 * math.log10(params.base_height_m)) * math.log10(params.distance_km)
        )
        received = params.tx_power_dbm + params.tx_gain_dbi + params.rx_gain_dbi - pl
        margin = received - params.receiver_sensitivity_dbm
        return PropagationResult(
            path_loss_db=round(pl, 2),
            received_power_dbm=round(received, 2),
            coverage_ok=margin >= 0,
            margin_db=round(margin, 2),
        )
