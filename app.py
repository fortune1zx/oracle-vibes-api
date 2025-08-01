from flask import Flask, request, jsonify
from kerykeion import KrInstance
from datetime import datetime

app = Flask(__name__)

@app.route('/astrology', methods=['POST'])
def calculate_astrology():
    try:
        data = request.get_json()
        year = int(data['year'])
        month = int(data['month'])
        day = int(data['day'])
        hour = int(data['hour'])
        minute = int(data['minute'])
        lat = float(data['lat'])
        lng = float(data['lng'])

        if not (1900 <= year <= 2040):
            return jsonify({'error': 'Year must be between 1900 and 2040'}), 400

        person = KrInstance("Person", year, month, day, hour, minute, lat, lng)

        response = {
            'sun_sign': f"{person.sun['sign']} {person.sun['degree']}° - Your identity shines in the Matrix",
            'moon_sign': f"{person.moon['sign']} - Your emotions dance with cosmic waves",
            'ascendant': f"{person.ascendant['sign']} - Your cosmic mask radiates",
            'planets': {
                'mercury': f"{person.mercury['sign']} {person.mercury['degree']}°",
                'venus': f"{person.venus['sign']} {person.venus['degree']}°",
                'mars': f"{person.mars['sign']} {person.mars['degree']}°"
            }
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
