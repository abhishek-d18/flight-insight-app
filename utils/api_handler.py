def generate_insights_text(data_insights):
    """Convert processed data into readable insights"""
    try:
        # Popular routes
        top_route = data_insights['popular_routes'].index[0] if not data_insights['popular_routes'].empty else ("N/A", "N/A")
        route_text = f"{top_route[0]} → {top_route[1]}" if top_route != ("N/A", "N/A") else "No route data"
        
        # Price analysis
        avg_price = data_insights.get('avg_price', 0)
        price_text = f"${avg_price:.2f}" if avg_price > 0 else "No price data"
        
        # Demand analysis
        if not data_insights['demand_trends'].empty:
            busiest_day = data_insights['demand_trends'].idxmax()
            demand_text = f"{busiest_day} ({data_insights['demand_trends'].max()} flights)"
        else:
            demand_text = "No demand data"
        
        insights = [
            f"Top Route: {route_text}",
            f"Average Price: {price_text}",
            f"Busiest Day: {demand_text}",
            "Trend: Prices are stable" if avg_price > 0 else ""
        ]
        
        return "✈️ Flight Insights:\n- " + "\n- ".join(filter(None, insights))
    
    except Exception as e:
        print(f"Insight generation error: {e}")
        return "✈️ No insights available (data processing failed)"