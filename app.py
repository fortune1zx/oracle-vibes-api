from flask import Flask, request, jsonify
from kerykeion import KrInstance

app = Flask(__name__)

@app.route('/astrology', methods=['POST'])
def astrology():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        year = data.get('year')
        month = data.get('month')
        day = data.get('day')
        hours = data.get('hour')  # kerykeion 'hours' bekliyor
        minuts = data.get('minute')  # kerykeion 'minuts' bekliyor
        lat = data.get('lat')
        lon = data.get('lng')  # kerykeion 'lon' bekliyor
        city = data.get('city', 'Unknown')  # Varsayılan şehir adı

        if not all([year, month, day, hours, minuts, lat, lon]):
            return jsonify({"error": "Missing required fields"}), 400

        person = KrInstance(
            name=city,
            year=year,
            month=month,
            day=day,
            hours=hours,
            minuts=minuts,
            lat=lat,
            lon=lon,
            tz_str="UTC"  # Saat dilimi sorununu çözmek için
        )
        response = {
            "sun_sign": f"{person.sun['sign']} {person.sun['degree']}° - Your identity shines in the Matrix",
            "moon_sign": f"{person.moon['sign']} - Your emotions dance with cosmic waves",
            "ascendant": f"{person.ascendant['sign']} - Your cosmic mask",
            "planets": {
                "mercury": f"{person.mercury['sign']} {person.mercury['degree']}°",
                "venus": f"{person.venus['sign']} {person.venus['degree']}°",
                "mars": f"{person.mars['sign']} {person.mars['degree']}°"
            }
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
