import flask
from flask import Flask, render_template
app = Flask(__name__)

lentokonetyypit = [
    {
        "malli": "Boeing 737",
        "valmistaja": "Boeing",
        "matkustajamaara": 189,
        "kantama_km": 6570,
        "max_nopeus_kmh": 876,
        "poltoaineen_kulutus_kg/km": 3.49,
        "hiilidioksidi_per_km": 11
    },
    {
        "malli": "Dash 8 Q400",
        "valmistaja": "De Havilland",
        "matkustajamaara": 82,
        "kantama_km": 2040,
        "max_nopeus_kmh": 600,
        "poltoaineen_kulutus_kg/km": 1.83,
        "hiilidioksidi_per_km": 5.78
    }
]

@app.route("/")
def index():
    return render_template("mainpage.html", lentokonetyypit=lentokonetyypit)

if __name__ == "__main__":
    app.run(debug=True)
