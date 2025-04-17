from flask import Flask, jsonify
import redis

app = Flask(__name__)

# Dados simulados de clima
weather_data = {
    "Curitiba": {"temp": 22, "unit": "Celsius"},
    "Maringa": {"temp": 37, "unit": "Celsius"},
    "Londrina": {"temp": 12, "unit": "Celsius"}
}

# Conectar ao Redis (certifique-se de que o Redis está em execução)
cache = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

@app.route('/weather/<city>', methods=['GET'])
def get_weather(city):
    # Tentar buscar dados no cache
    cached_data = cache.get(city)
    
    if cached_data:
        print("VOCÊ BATEU EM MIM - Dados em cache")
        return cached_data  # Retorna os dados do cache diretamente
    
    city_data = weather_data.get(city)
    
    if city_data:
        # Se os dados não estiverem no cache, armazenamos no cache por 60 segundos
        response = jsonify({"city": city, "temp": city_data["temp"], "unit": city_data["unit"]})
        cache.setex(city, 60, response.get_data(as_text=True))  # Cache por 60 segundos
        return response
    else:
        return jsonify({"error": "Cidade não encontrada!"}), 404

if __name__ == '__main__':
    app.run(port=5000)  # API B roda na porta 5000
