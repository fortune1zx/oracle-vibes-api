from flask import Flask, request, jsonify
from kerykeion import AstrologicalSubject
import logging
from datetime import datetime, timedelta
import ephem

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ELEMENTS = {
    'Ari': 'Fire', 'Leo': 'Fire', 'Sag': 'Fire',
    'Tau': 'Earth', 'Vir': 'Earth', 'Cap': 'Earth',
    'Gem': 'Air', 'Lib': 'Air', 'Aqu': 'Air',
    'Can': 'Water', 'Sco': 'Water', 'Pis': 'Water'
}

def get_transits(year, month, day):
    observer = ephem.Observer()
    observer.date = f"{year}/{month}/{day}"
    moon = ephem.Moon(observer)
    return {
        "moon_position": f"{ephem.constellation(moon)[1]} {moon.ra:.2f}°"
    }

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Oracle Vibes API! Use POST /astrology to get astrological data."}), 200

@app.route('/astrology', methods=['POST'])
def astrology():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        year = data.get('year')
        month = data.get('month')
        day = data.get('day')
        hours = data.get('hour')
        minutes = data.get('minute')
        lat = data.get('lat')
        lng = data.get('lng')
        city = data.get('city', 'Unknown')

        if not all([year, month, day, hours, minutes, lat, lng]):
            return jsonify({"error": "Missing required fields"}), 400

        person = AstrologicalSubject(
            year=year,
            month=month,
            day=day,
            hour=hours,
            minute=minutes,
            lng=lng,
            lat=lat,
            tz_str="UTC"
        )

        logger.info(f"Calculating for {year}-{month}-{day} {hours}:{minutes}, lat: {lat}, lng: {lng}")
        
        element_counts = {'Fire': 0, 'Earth': 0, 'Air': 0, 'Water': 0}
        for planet in [person.sun, person.moon, person.mercury, person.venus, person.mars,
                       person.jupiter, person.saturn, person.uranus, person.neptune, person.pluto]:
            element = ELEMENTS.get(planet['sign'][:3], 'Unknown')
            if element != 'Unknown':
                element_counts[element] += 1

        calendar = []
        today = datetime.now()
        for i in range(30):
            date = today + timedelta(days=i)
            transits = get_transits(date.year, date.month, date.day)
            calendar.append({
                "date": date.strftime("%Y-%m-%d"),
                "moon_position": transits["moon_position"]
            })

        planets_response = {
            "sun": {"sign": person.sun['sign'], "house": person.sun['house'], "position": f"{person.sun.get('position', 0)}°"},
            "moon": {"sign": person.moon['sign'], "house": person.moon['house'], "position": f"{person.moon.get('position', 0)}°"},
            "mercury": {"sign": person.mercury['sign'], "house": person.mercury['house'], "position": f"{person.mercury.get('position', 0)}°"},
            "venus": {"sign": person.venus['sign'], "house": person.venus['house'], "position": f"{person.venus.get('position', 0)}°"},
            "mars": {"sign": person.mars['sign'], "house": person.mars['house'], "position": f"{person.mars.get('position', 0)}°"},
            "jupiter": {"sign": person.jupiter['sign'], "house": person.jupiter['house'], "position": f"{person.jupiter.get('position', 0)}°"},
            "saturn": {"sign": person.saturn['sign'], "house": person.saturn['house'], "position": f"{person.saturn.get('position', 0)}°"},
            "uranus": {"sign": person.uranus['sign'], "house": person.uranus['house'], "position": f"{person.uranus.get('position', 0)}°"},
            "neptune": {"sign": person.neptune['sign'], "house": person.neptune['house'], "position": f"{person.neptune.get('position', 0)}°"},
            "pluto": {"sign": person.pluto['sign'], "house": person.pluto['house'], "position": f"{person.pluto.get('position', 0)}°"}
        }
        if hasattr(person, 'chiron'):
            planets_response["chiron"] = {"sign": person.chiron['sign'], "house": person.chiron['house'], "position": f"{person.chiron.get('position', 0)}°"}
        if hasattr(person, 'mean_lilith'):
            planets_response["lilith"] = {"sign": person.mean_lilith['sign'], "house": person.mean_lilith['house'], "position": f"{person.mean_lilith.get('position', 0)}°"}
        if hasattr(person, 'north_node'):
            planets_response["north_node"] = {"sign": person.north_node['sign'], "house": person.north_node['house'], "position": f"{person.north_node.get('position', 0)}°"}
        if hasattr(person, 'south_node'):
            planets_response["south_node"] = {"sign": person.south_node['sign'], "house": person.south_node['house'], "position": f"{person.south_node.get('position', 0)}°"}

        response = {
            "sun_sign": f"{person.sun['sign']} {person.sun.get('position', 0)}°",
            "moon_sign": f"{person.moon['sign']} {person.moon.get('position', 0)}°",
            "ascendant": f"{person.first_house['sign']} {person.first_house.get('position', 0)}°",
            "planets": planets_response,
            "houses": {
                "house_1": f"{person.first_house['sign']} {person.first_house.get('position', 0)}°",
                "house_2": f"{person.second_house['sign']} {person.second_house.get('position', 0)}°",
                "house_3": f"{person.third_house['sign']} {person.third_house.get('position', 0)}°",
                "house_4": f"{person.fourth_house['sign']} {person.fourth_house.get('position', 0)}°",
                "house_5": f"{person.fifth_house['sign']} {person.fifth_house.get('position', 0)}°",
                "house_6": f"{person.sixth_house['sign']} {person.sixth_house.get('position', 0)}°",
                "house_7": f"{person.seventh_house['sign']} {person.seventh_house.get('position', 0)}°",
                "house_8": f"{person.eighth_house['sign']} {person.eighth_house.get('position', 0)}°",
                "house_9": f"{person.ninth_house['sign']} {person.ninth_house.get('position', 0)}°",
                "house_10": f"{person.tenth_house['sign']} {person.tenth_house.get('position', 0)}°",
                "house_11": f"{person.eleventh_house['sign']} {person.eleventh_house.get('position', 0)}°",
                "house_12": f"{person.twelfth_house['sign']} {person.twelfth_house.get('position', 0)}°"
            },
            "elements": element_counts,
            "calendar": calendar
        }
        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
