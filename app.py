from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
from utils.data_scraper import get_flight_data
from utils.data_processor import process_data
from utils.api_handler import generate_insights_text
import json

app = Flask(__name__)

@app.route('/')
def index():
    try:
        # Get default date range
        today = datetime.now().strftime('%Y-%m-%d')
        next_week = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        
        # Initial load with default data
        return render_template(
            'index.html',
            today=today,
            next_week=next_week,
            initial_load=True
        )
    except Exception as e:
        return render_template('error.html', message=str(e)), 500

@app.route('/get_flight_data', methods=['POST'])
def get_flight_data_route():
    try:
        filters = request.json
        print(f"\nApplying filters: {filters}")
        
        # 1. Get raw data
        raw_data = get_flight_data()
        
        # 2. Process data
        processed = process_data(raw_data, filters)
        
        # 3. Generate insights
        insights = generate_insights_text(processed)
        
        # 4. Prepare response
        response = {
            'insights': insights,
            'chart_data': {
                'price_labels': list(processed['price_trends'].index.astype(str)),
                'price_values': list(processed['price_trends'].values),
                'demand_labels': list(processed['demand_trends'].index.astype(str)),
                'demand_values': list(processed['demand_trends'].values)
            },
            'routes': [{
                'route': f"{route[0]} → {route[1]}",
                'count': count,
                'price': f"${processed['route_prices'].get(route, 0):.2f}" 
            } for route, count in processed['popular_routes'].items()],
            'avg_price': f"${processed['avg_price']:.2f}",
            'data_status': f"Live Data • {len(raw_data)} flights",
            'success': True
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 503

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)