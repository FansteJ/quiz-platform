from flask import Flask, jsonify

# Kreiramo Flask aplikaciju
app = Flask(__name__)

# Definišemo "rutu" - URL endpoint
@app.route('/')
def hello():
    return jsonify({
        'message': 'Quiz Platform API radi!',
        'status': 'success'
    })

# Još jedan endpoint za testiranje
@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

# Pokretanje aplikacije
if __name__ == '__main__':
    # host='0.0.0.0' omogućava pristup iz Dockera
    # port=5000 je port na kome slušamo zahteve
    app.run(host='0.0.0.0', port=5000, debug=True)