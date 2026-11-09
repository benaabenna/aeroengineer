from flask import Flask, request, render_template_string
import json
import numpy as np
from aeroengineer import StandardAtmosphere, GasDynamics

app = Flask(__name__)

# --- Atmosphere profile data (generated once) ---
def build_atmosphere_profile():
    altitudes = np.arange(0, 31000, 100)
    temps, pressures, densities = [], [], []
    for alt in altitudes:
        t, p, d = StandardAtmosphere.properties(alt)
        temps.append(t)
        pressures.append(p)
        densities.append(d)
    return {
        "altitudes": [int(a) for a in altitudes],
        "temperatures": temps,
        "pressures": pressures,
        "densities": densities,
    }

ATMO_PROFILE = build_atmosphere_profile()

# --- Sutherland's formula for air viscosity ---
def sutherland_viscosity(T):
    mu0, T0, S = 1.716e-5, 273.15, 111.0
    return mu0 * (T / T0) ** 1.5 * (T0 + S) / (T + S)

HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AeroEngineer</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #0f172a;
    color: #e2e8f0;
    min-height: 100vh;
    padding: 2rem;
  }
  .container { max-width: 900px; margin: 0 auto; }
  h1 {
    font-size: 1.8rem;
    margin-bottom: 0.3rem;
    color: #f8fafc;
    text-align: center;
  }
  .subtitle { text-align: center; color: #64748b; margin-bottom: 2rem; font-size: 0.9rem; }
  .card {
    background: #1e293b;
    border-radius: 12px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
  }
  .card h2 {
    font-size: 1.1rem;
    margin-bottom: 1.2rem;
    color: #94a3b8;
    font-weight: 600;
  }
  .form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }
  label { display: block; margin-bottom: 0.3rem; font-size: 0.85rem; color: #94a3b8; }
  input[type="number"] {
    width: 100%;
    padding: 0.6rem 0.8rem;
    border: 1px solid #334155;
    border-radius: 6px;
    background: #0f172a;
    color: #e2e8f0;
    font-size: 1rem;
  }
  input[type="number"]:focus { outline: none; border-color: #3b82f6; }
  button {
    grid-column: 1 / -1;
    padding: 0.7rem;
    border: none;
    border-radius: 6px;
    background: #3b82f6;
    color: white;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
    margin-top: 0.5rem;
  }
  button:hover { background: #2563eb; }
  .results-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 0.8rem;
  }
  .result-item {
    background: #0f172a;
    border-radius: 8px;
    padding: 1rem;
  }
  .result-item .label { font-size: 0.75rem; color: #64748b; margin-bottom: 0.3rem; }
  .result-item .value { font-size: 1.1rem; color: #38bdf8; font-weight: 600; font-variant-numeric: tabular-nums; }
  .result-item .unit { font-size: 0.8rem; color: #64748b; margin-left: 0.2rem; }
  .chart-container { position: relative; height: 300px; }
  .tabs { display: flex; gap: 0.5rem; margin-bottom: 1rem; }
  .tab {
    padding: 0.4rem 1rem;
    border-radius: 6px;
    font-size: 0.85rem;
    cursor: pointer;
    background: #0f172a;
    color: #94a3b8;
    border: 1px solid #334155;
  }
  .tab.active { background: #3b82f6; color: white; border-color: #3b82f6; }
  .chart-panel { display: none; }
  .chart-panel.active { display: block; }
</style>
</head>
<body>
<div class="container">
  <h1>✈ AeroEngineer</h1>
  <p class="subtitle">Standard Atmosphere &amp; Gas Dynamics Calculator</p>

  <!-- Calculator -->
  <div class="card">
    <h2>Calculate</h2>
    <form action="/" method="post">
      <div class="form-grid">
        <div>
          <label>Altitude (m)</label>
          <input type="number" name="altitude" value="{{ altitude }}" step="any">
        </div>
        <div>
          <label>Velocity (m/s)</label>
          <input type="number" name="velocity" value="{{ velocity }}" step="any">
        </div>
        <button type="submit">Calculate</button>
      </div>
    </form>
  </div>

  <!-- Results -->
  {% if results %}
  <div class="card">
    <h2>Results @ {{ '%.0f' % results.altitude }} m</h2>
    <div class="results-grid">
      <div class="result-item">
        <div class="label">Temperature</div>
        <div class="value">{{ '%.2f' % results.temperature }}<span class="unit">K</span></div>
      </div>
      <div class="result-item">
        <div class="label">Pressure</div>
        <div class="value">{{ '%.1f' % results.pressure }}<span class="unit">Pa</span></div>
      </div>
      <div class="result-item">
        <div class="label">Density</div>
        <div class="value">{{ '%.4f' % results.density }}<span class="unit">kg/m³</span></div>
      </div>
      <div class="result-item">
        <div class="label">Speed of Sound</div>
        <div class="value">{{ '%.2f' % results.speed_of_sound }}<span class="unit">m/s</span></div>
      </div>
      <div class="result-item">
        <div class="label">Mach Number</div>
        <div class="value">{{ '%.3f' % results.mach }}</div>
      </div>
      <div class="result-item">
        <div class="label">Dynamic Pressure</div>
        <div class="value">{{ '%.1f' % results.dynamic_pressure }}<span class="unit">Pa</span></div>
      </div>
      <div class="result-item">
        <div class="label">Viscosity</div>
        <div class="value">{{ '%.3e' % results.viscosity }}<span class="unit">Pa·s</span></div>
      </div>
      <div class="result-item">
        <div class="label">Reynolds Number</div>
        <div class="value">{{ '%.3e' % results.reynolds }}<span class="unit">(chord=1m)</span></div>
      </div>
      <div class="result-item">
        <div class="label">Density Altitude</div>
        <div class="value">{{ '%.0f' % results.density_altitude }}<span class="unit">m</span></div>
      </div>
    </div>
  </div>
  {% endif %}

  <!-- Atmosphere Profile Chart -->
  <div class="card">
    <h2>Standard Atmosphere Profile</h2>
    <div class="tabs">
      <span class="tab active" onclick="switchTab(0)">Temperature</span>
      <span class="tab" onclick="switchTab(1)">Pressure</span>
      <span class="tab" onclick="switchTab(2)">Density</span>
    </div>
    <div class="chart-panel active" id="panel0">
      <div class="chart-container"><canvas id="chart0"></canvas></div>
    </div>
    <div class="chart-panel" id="panel1">
      <div class="chart-container"><canvas id="chart1"></canvas></div>
    </div>
    <div class="chart-panel" id="panel2">
      <div class="chart-container"><canvas id="chart2"></canvas></div>
    </div>
  </div>
</div>

<script>
const altitudes = {{ profile.altitudes | tojson }};
const temps = {{ profile.temperatures | tojson }};
const pressures = {{ profile.pressures | tojson }};
const densities = {{ profile.densities | tojson }};

const baseOpts = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    x: { title: { display: true, text: 'Altitude (m)', color: '#64748b' }, ticks: { color: '#64748b' }, grid: { color: '#1e293b' } },
    y: { title: { display: true, color: '#64748b' }, ticks: { color: '#64748b' }, grid: { color: '#1e293b' } }
  }
};

function makeChart(id, data, yLabel, color) {
  new Chart(document.getElementById(id), {
    type: 'line',
    data: {
      labels: altitudes,
      datasets: [{ data: data, borderColor: color, borderWidth: 2, pointRadius: 0, fill: true, backgroundColor: color + '22' }]
    },
    options: { ...baseOpts, scales: { ...baseOpts.scales, y: { ...baseOpts.scales.y, title: { display: true, text: yLabel, color: '#64748b' } } } }
  });
}

makeChart('chart0', temps, 'Temperature (K)', '#f97316');
makeChart('chart1', pressures, 'Pressure (Pa)', '#3b82f6');
makeChart('chart2', densities, 'Density (kg/m³)', '#22c55e');

function switchTab(i) {
  document.querySelectorAll('.tab').forEach((t, j) => t.classList.toggle('active', j === i));
  document.querySelectorAll('.chart-panel').forEach((p, j) => p.classList.toggle('active', j === i));
}
</script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    altitude = 10000
    velocity = 340
    results = None

    if request.method == "POST":
        altitude = float(request.form.get("altitude", 10000))
        velocity = float(request.form.get("velocity", 340))

        temperature, pressure, density = StandardAtmosphere.properties(altitude)
        gd = GasDynamics()
        mach = gd.mach_from_velocity(velocity, temperature)
        speed_of_sound = velocity / mach if mach != 0 else 340.0
        dynamic_pressure = 0.5 * density * velocity ** 2
        viscosity = sutherland_viscosity(temperature)
        reynolds = density * velocity * 1.0 / viscosity  # chord = 1 m
        # Density altitude: altitude where standard density equals local density
        density_altitude = altitude  # simplified; for ISA this equals geometric altitude
        # For non-standard conditions you'd solve iteratively

        results = {
            "altitude": altitude,
            "temperature": temperature,
            "pressure": pressure,
            "density": density,
            "speed_of_sound": speed_of_sound,
            "mach": mach,
            "dynamic_pressure": dynamic_pressure,
            "viscosity": viscosity,
            "reynolds": reynolds,
            "density_altitude": density_altitude,
        }

    return render_template_string(HTML, altitude=altitude, velocity=velocity, results=results, profile=ATMO_PROFILE)

if __name__ == "__main__":
    app.run(debug=True)   
