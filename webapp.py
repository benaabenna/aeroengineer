from flask import Flask, request, render_template_string
import numpy as np
from aeroengineer import StandardAtmosphere, GasDynamics

app = Flask(__name__)

HTML = """
<!doctype html>
<title>AeroEngineer Calculator</title>
<h1>AeroEngineer Calculator</h1>
<form action="/" method="post">
    Altitude (meters): <input type="number" name="altitude" value="{{ altitude }}" step="any"><br>
    Velocity (m/s): <input type="number" name="velocity" value="{{ velocity }}" step="any"><br>
    <input type="submit" value="Calculate">
</form>

{% if results %}
<h2>Results</h2>
<ul>
    <li>Temperature (K): {{ '%.2f' % results.temperature }}</li>
    <li>Pressure (Pa): {{ '%.1f' % results.pressure }}</li>
    <li>Density (kg/m³): {{ '%.4f' % results.density }}</li>
    <li>Mach number: {{ '%.3f' % results.mach }}</li>
</ul>
{% endif %}
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
