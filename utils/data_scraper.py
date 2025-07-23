import requests
import pandas as pd
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, List

load_dotenv()

def get_flight_data() -> pd.DataFrame:
    """
    Get REAL flight data from AviationStack API only
    Returns:
        pd.DataFrame: Columns [date, origin, destination, price, airline]
    Raises:
        Exception: If API fails
    """
    print("\n" + "="*50)
    print("FETCHING LIVE FLIGHT DATA".center(50))
    print("="*50)
    
    API_KEY = os.getenv('AVIATIONSTACK_API_KEY')
    if not API_KEY:
        raise ValueError("❌ Missing API key in .env file")

    try:
        params = {
            'access_key': API_KEY,
            'limit': 100,
            'flight_status': 'scheduled'  # Gets upcoming flights
        }
        
        print("\n🌐 Requesting data from AviationStack...")
        response = requests.get(
            'http://api.aviationstack.com/v1/flights',
            params=params,
            timeout=15
        )
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Received {len(data.get('data', []))} flights")
        
        # Print raw sample
        print("\n📄 Raw API Sample (first flight):")
        print(json.dumps(data['data'][0], indent=2))
        
        # Process data
        flights = []
        for flight in data.get('data', []):
            try:
                flights.append({
                    'date': flight.get('flight_date'),
                    'origin': flight['departure'].get('iata', ''),
                    'destination': flight['arrival'].get('iata', ''),
                    'price': float(flight.get('price', 0)),
                    'airline': flight['airline'].get('name', 'Unknown')
                })
            except (KeyError, TypeError) as e:
                print(f"⚠️ Skipping malformed flight: {e}")
                continue
        
        df = pd.DataFrame(flights)
        
        print("\n🛫 Processed Data (first 3 rows):")
        print(df.head(3).to_markdown(tablefmt="grid"))
        print(f"\nTotal flights processed: {len(df)}")
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"\n🔴 API Request Failed: {str(e)}")
        raise Exception("Could not connect to AviationStack API")
    except Exception as e:
        print(f"\n🔴 Data Processing Error: {str(e)}")
        raise Exception("Failed to process flight data")