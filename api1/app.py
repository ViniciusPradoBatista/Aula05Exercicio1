from flask import Flask, jsonify

app = Flask(__name__)

weather_data = {
    "Curitiba": {"temp": 22, "unit": "Celsius"},
    "Maringa": {"temp": 37, "unit": "Celsius"},
    "Londrina": {"temp": 12, "unit": "Celsius"}
}

@app.route('/weather/<city>', methods=['GET'])
def get_weather(city):
    city_data = weather_data.get(city)
    
    if city_data:
        return jsonify({"city": city, "temp": city_data["temp"], "unit": city_data["unit"]})
    else:
        return jsonify({"error": "Cidade não encontrada!"}), 404

if __name__ == '__main__':
    app.run(port=5000)
