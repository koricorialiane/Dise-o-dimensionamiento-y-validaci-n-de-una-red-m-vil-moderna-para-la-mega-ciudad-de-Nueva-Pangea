import base64
import io

from flask import Flask, render_template_string, request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from app.adapters.okumura_hata_adapter import OkumuraHataAdapter
from app.adapters.erlang_adapter import ErlangBAdapter
from app.domain.models import PropagationInput, TrafficInput
from app.domain.services import RadioPlanningService

app = Flask(__name__)

SERVICE = RadioPlanningService(
    propagation_calculator=OkumuraHataAdapter(),
    traffic_estimator=ErlangBAdapter(),
)

FORM_TEMPLATE = '''
<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <title>Demo de planificación RF</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 2rem; }
      label { display: block; margin-top: 1rem; }
      input { width: 100%; max-width: 320px; padding: 0.4rem; }
      button { margin-top: 1rem; padding: 0.6rem 1rem; }
      .result { margin-top: 2rem; padding: 1rem; border: 1px solid #ccc; background: #f9f9f9; }
      .graphs { display: flex; flex-wrap: wrap; gap: 1rem; margin-top: 1.5rem; }
      .graph { width: 100%; max-width: 560px; border: 1px solid #ddd; padding: 0.8rem; background: #fff; }
      .graph img { width: 100%; height: auto; }
    </style>
  </head>
  <body>
    <h1>Prueba de concepto RF</h1>
    <form method="post">
      <h2>Parámetros de cobertura</h2>
      <label>Frecuencia (MHz)<input name="frequency_mhz" type="number" step="any" value="2600" required></label>
      <label>Altura de estación base (m)<input name="base_height_m" type="number" step="any" value="30" required></label>
      <label>Altura móvil (m)<input name="mobile_height_m" type="number" step="any" value="1.5" required></label>
      <label>Distancia (km)<input name="distance_km" type="number" step="any" value="1" required></label>
      <label>Potencia TX (dBm)<input name="tx_power_dbm" type="number" step="any" value="43" required></label>
      <label>Ganancia TX (dBi)<input name="tx_gain_dbi" type="number" step="any" value="15" required></label>
      <label>Ganancia RX (dBi)<input name="rx_gain_dbi" type="number" step="any" value="0" required></label>
      <label>Sensibilidad RX (dBm)<input name="receiver_sensitivity_dbm" type="number" step="any" value="-100" required></label>

      <h2>Parámetros de tráfico</h2>
      <label>Carga de tráfico (Erlang)<input name="traffic_load_erlang" type="number" step="any" value="10" required></label>
      <label>Canales disponibles<input name="channels" type="number" value="5" required></label>

      <button type="submit">Calcular</button>
    </form>

    {% if coverage_result and traffic_result %}
    <div class="result">
      <h2>Resultados</h2>
      <p><strong>Pérdida de propagación:</strong> {{ coverage_result.path_loss_db }} dB</p>
      <p><strong>Potencia recibida:</strong> {{ coverage_result.received_power_dbm }} dBm</p>
      <p><strong>Margen de cobertura:</strong> {{ coverage_result.margin_db }} dB</p>
      <p><strong>Cobertura:</strong> {{ 'OK' if coverage_result.coverage_ok else 'Insuficiente' }}</p>
      <hr>
      <p><strong>Probabilidad de bloqueo Erlang B:</strong> {{ traffic_result.blocking_probability }}</p>
      <p><strong>Aceptación de bloqueo:</strong> {{ 'Aceptable' if traffic_result.accepted else 'Alto bloqueo' }}</p>
    </div>
    <div class="graphs">
      <div class="graph">
        <h3>Propagación: pérdida y potencia vs distancia</h3>
        <img src="data:image/png;base64,{{ propagation_graph }}" alt="Gráfica de propagación">
      </div>
      <div class="graph">
        <h3>Erlang B: bloqueo vs número de canales</h3>
        <img src="data:image/png;base64,{{ traffic_graph }}" alt="Gráfica de tráfico">
      </div>
    </div>
    {% endif %}
  </body>
</html>
'''


def figure_to_base64(fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    encoded = base64.b64encode(buffer.read()).decode('ascii')
    plt.close(fig)
    return encoded


def build_propagation_graph(params: PropagationInput) -> str:
    distances = [0.1 * i for i in range(1, 51)]
    path_loss = []
    received = []

    for d in distances:
        sample = PropagationInput(
            frequency_mhz=params.frequency_mhz,
            base_height_m=params.base_height_m,
            mobile_height_m=params.mobile_height_m,
            distance_km=d,
            tx_power_dbm=params.tx_power_dbm,
            tx_gain_dbi=params.tx_gain_dbi,
            rx_gain_dbi=params.rx_gain_dbi,
            receiver_sensitivity_dbm=params.receiver_sensitivity_dbm,
        )
        result = SERVICE.calculate_coverage(sample)
        path_loss.append(result.path_loss_db)
        received.append(result.received_power_dbm)

    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.plot(distances, path_loss, label='Pérdida de propagación (dB)', color='#1f77b4')
    ax.plot(distances, received, label='Potencia recibida (dBm)', color='#ff7f0e')
    ax.set_xlabel('Distancia (km)')
    ax.set_ylabel('Valor')
    ax.set_title('Modelo Okumura-Hata vs distancia')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()
    return figure_to_base64(fig)


def build_traffic_graph(params: TrafficInput) -> str:
    channel_range = list(range(1, max(6, params.channels + 5)))
    blocking_values = []

    for ch in channel_range:
        sample = TrafficInput(traffic_load_erlang=params.traffic_load_erlang, channels=ch)
        result = SERVICE.calculate_blocking(sample)
        blocking_values.append(result.blocking_probability)

    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.plot(channel_range, blocking_values, marker='o', color='#2ca02c')
    ax.set_xlabel('Número de canales')
    ax.set_ylabel('Probabilidad de bloqueo')
    ax.set_title('Erlang B: bloqueo vs canales')
    ax.grid(True, linestyle='--', alpha=0.5)
    return figure_to_base64(fig)


@app.route('/', methods=['GET', 'POST'])
def home():
    coverage_result = None
    traffic_result = None
    propagation_graph = None
    traffic_graph = None

    if request.method == 'POST':
        coverage_params = PropagationInput(
            frequency_mhz=float(request.form['frequency_mhz']),
            base_height_m=float(request.form['base_height_m']),
            mobile_height_m=float(request.form['mobile_height_m']),
            distance_km=float(request.form['distance_km']),
            tx_power_dbm=float(request.form['tx_power_dbm']),
            tx_gain_dbi=float(request.form['tx_gain_dbi']),
            rx_gain_dbi=float(request.form['rx_gain_dbi']),
            receiver_sensitivity_dbm=float(request.form['receiver_sensitivity_dbm']),
        )
        traffic_params = TrafficInput(
            traffic_load_erlang=float(request.form['traffic_load_erlang']),
            channels=int(request.form['channels']),
        )

        coverage_result = SERVICE.calculate_coverage(coverage_params)
        traffic_result = SERVICE.calculate_blocking(traffic_params)
        propagation_graph = build_propagation_graph(coverage_params)
        traffic_graph = build_traffic_graph(traffic_params)

    return render_template_string(
        FORM_TEMPLATE,
        coverage_result=coverage_result,
        traffic_result=traffic_result,
        propagation_graph=propagation_graph,
        traffic_graph=traffic_graph,
    )
