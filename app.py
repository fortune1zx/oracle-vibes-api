from flask import Flask, request, jsonify
from kerykeion import KrInstance
import logging

app = Flask(__name__)

# Loglama ayarları
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
        # Person nesnesinin yapısını logla
        logger.debug(f"Person sun: {person.sun}")
        logger.debug(f"Person moon: {person.moon}")
        logger.debug(f"Person first_house: {person.first_house}")
        logger.debug(f"Person mercury: {person.mercury}")
        logger.debug(f"Person venus: {person.venus}")
        logger.debug(f"Person mars: {person.mars}")

        response = {
            "sun_sign": f"{person.sun['sign']} {person.sun.get('position', 0)}° - Your identity shines in the Matrix",
            "moon_sign": f"{person.moon['sign']} - Your emotions dance with cosmic waves",
            "ascendant": f"{person.first_house['sign']} - Your cosmic mask",
            "planets": {
                "mercury": f"{person.mercury['sign']} {person.mercury.get('position', 0)}°",
                "venus": f"{person.venus['sign']} {person.venus.get('position', 0)}°",
                "mars": f"{person.mars['sign']} {person.mars.get('position', 0)}°"
            }
        }
        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
