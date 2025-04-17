from flask import Flask, jsonify
import requests
import redis

app = Flask(__name__)

# Conectar ao Redis
cache = redis.StrictRedis(host='localhost', port=6379, db=1, decode_responses=True)

@app.route('/recommendation/<city>', methods=['GET'])
def get_recommendation(city):
    cache_key = f'recommendation_{city}'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        print("VOCÊ BATEU EM MIM - Dados de recomendação em cache")
        return cached_data  # Retorna a recomendação do cache
    
    # Se não estiver em cache, chama a API B para pegar os dados de clima
    try:
        response = requests.get(f'http://localhost:5000/weather/{city}')
        
        if response.status_code == 200:
            data = response.json()
            temp = data["temp"]
            unit = data["unit"]
            
            # Gera a recomendação baseada na temperatura
            if temp > 30:
                recommendation = "Hidrate-se e use protetor solar."
            elif 15 <= temp <= 30:
                recommendation = "O clima está agradável."
            else:
                recommendation = "Use um casaco, está frio."
            
            result = jsonify({
                "city": city,
                "temp": temp,
                "unit": unit,
                "recommendation": recommendation
            })
            
            # Armazenar a recomendação no cache por 60 segundos
            cache.setex(cache_key, 60, result.get_data(as_text=True))  # Cache por 60 segundos
            return result
        else:
            return jsonify({"error": "Cidade não encontrada na API B!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)  # API A roda na porta 5001
