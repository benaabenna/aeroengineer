from flask import Flask, request, render_template_string
import numpy as np
from aeroengineer import StandardAtmosphere, GasDynamics

app = Flask(__name__)

HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AeroEngineer Calculator</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #0f172a;
    color: #e2e8f0;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem;
  }
  .card {
    background: #1e293b;
    border-radius: 12px;
    padding: 2.5rem;
    width: 100%;
    max-width: 480px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
  }
  h1 {
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
    color: #f8fafc;
    text-align: center;
  }
  label {
    display: block;
    margin-bottom: 0.4rem;
    font-size: 0.9rem;
    color: #94a3b8;
  }
  input[type="number"] {
    width: 100%;
    padding: 0.6rem 0.8rem;
    margin-bottom: 1rem;
    border: 1px solid #334155;
    border-radius: 6px;
    background: #0f172a;
    color: #e2e8f0;
    font-size: 1rem;
  }
  input[type="number"]:focus {
    outline: none;
    border-color: #3b82f6;
  }
  button {
    width: 100%;
    padding: 0.7rem;
    border: none;
    border-radius: 6px;
    background: #3b82f6;
    color: white;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
  }
  button:hover { background: #2563eb; }
  .results {
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid #334155;
  }
  .results h2 {
    font-size: 1.1rem;
    margin-bottom: 1rem;
    color: #94a3b8;
  }
  .results ul { list-style: none; }
  .results li {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
    border-bottom: 1px solid #1e293b;
  }
  .results li:last-child { border-bottom: none; }
  .results .label { color: #94a3b8; }
  .results .value { color: #38bdf8; font-weight: 600; font-variant-numeric: tabular-nums; }
</style>
</head>
<body>
<div class="card">
  <h1>✈ AeroEngineer Calculator</h1>
  <form action="/" method="post">
    <label>Altitude (meters)</label>
    <input type="number" name="altitude" value="{{ altitude }}" step="any">
    <label>Velocity (m/s)</label>
    <input type="number" name="velocity" value="{{ velocity }}" step="any">
    <button type="submit">Calculate</button>
  </form>

  {% if results %}
  <div class="results">
    <h2>Results</h2>
    <ul>
      <li><span class="label">Temperature</span><span class="value">{{ '%.2f' % results.temperature }} K</span></li>
      <li><span class="label">Pressure</span><span class="value">{{ '%.1f' % results.pressure }} Pa</span></li>
      <li><span class="label">Density</span><span class="value">{{ '%.4f' % results.density }} kg/m³</span></li>
      <li><span class="label">Mach Number</span><span class="value">{{ '%.3f' % results.mach }}</span></li>
    </ul>
  </div>
  {% endif %}
</div>
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
        results = {
            "temperature": temperature,
            "pressure": pressure,
            "density": density,
            "mach": mach,
        }

    return render_template_string(HTML, altitude=altitude, velocity=velocity, results=results)

if __name__ == "__main__":
    app.run(debug=True)   
