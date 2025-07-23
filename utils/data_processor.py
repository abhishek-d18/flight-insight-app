import pandas as pd
from typing import Dict, Any
from datetime import datetime

def process_data(raw_df: pd.DataFrame, filters: Dict = None) -> Dict[str, Any]:
    """Process raw flight data with optional filters"""
    # Initialize empty results
    results = {
        'popular_routes': pd.Series(dtype='int64'),
        'price_trends': pd.Series(dtype='float64'),
        'demand_trends': pd.Series(dtype='int64'),
        'avg_price': 0.0,
        'route_prices': dict()
    }
    
    if raw_df.empty:
        return results
    
    try:
        # Clean and filter data
        df = raw_df.copy()
        df['date'] = pd.to_datetime(df['date'])
        
        # Apply filters if provided
        if filters:
            if filters.get('start_date'):
                df = df[df['date'] >= pd.to_datetime(filters['start_date'])]
            if filters.get('end_date'):
                df = df[df['date'] <= pd.to_datetime(filters['end_date'])]
            if filters.get('airline') and filters['airline'] != 'all':
                df = df[df['airline'].str.contains(filters['airline'], case=False)]
        
        # Remove invalid prices
        df = df[df['price'] > 0]
        
        if df.empty:
            return results
            
        # Calculate insights
        results.update({
            'popular_routes': (
                df.groupby(['origin', 'destination'])
                .size()
                .nlargest(10)
                .sort_values(ascending=False)
            ),
            'price_trends': (
                df.groupby(df['date'].dt.date)['price']
                .mean()
                .round(2)
            ),
            'demand_trends': (
                df['date'].dt.date
                .value_counts()
                .sort_index()
            ),
            'avg_price': round(float(df['price'].mean()), 2),
            'route_prices': (
                df.groupby(['origin', 'destination'])['price']
                .mean()
                .round(2)
                .to_dict()
            )
        })
        
        return results
        
    except Exception as e:
        print(f"Processing error: {str(e)}")
        return results