from flask import Flask, request, jsonify
import random

app = Flask(__name__)


@app.route('/get_currents_data', methods=['GET'])
def get_currents_data():
    # Get longitude and latitude parameters from the request
    longitude = request.args.get('longitude')
    latitude = request.args.get('latitude')

    # Check if longitude and latitude are provided
    if longitude is None or latitude is None:
        return jsonify({'error': 'Both longitude and latitude parameters are required.'}), 400

    # Generate random values for sea_currents_speed and sea_currents_angle
    sea_currents_speed = round(random.uniform(1.0, 1.1), 2)
    sea_currents_angle = round(random.uniform(1.0, 1.1), 2)

    # Create a JSON response
    response_data = {
        'sea_currents_speed': sea_currents_speed,
        'sea_currents_angle': sea_currents_angle
    }

    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
