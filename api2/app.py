from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/recommendation/<city>', methods=['GET'])
def get_recommendation(city):
    try:
        response = requests.get(f'http://localhost:5000/weather/{city}')
        
        if response.status_code == 200:
            data = response.json()
            temp = data["temp"]
            unit = data["unit"]
            
            if temp > 30:
                recommendation = "Hidrate-se e use protetor solar."
            elif 15 <= temp <= 30:
                recommendation = "O clima está agradável."
            else:
                recommendation = "Use um casaco, está frio."
            
            return jsonify({
                "city": city,
                "temp": temp,
                "unit": unit,
                "recommendation": recommendation
            })
        else:
            return jsonify({"error": "Cidade não encontrada na API B!"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)
