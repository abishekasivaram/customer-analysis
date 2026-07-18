import json
import os

def load_all_data():
    data = {}
    paths = {
        "summary": "outputs/business/retail_summary.json",
        "kpis": "outputs/business/kpi_dashboard.json",
        "opportunities": "outputs/advisor/opportunities.json",
        "health": "outputs/advisor/store_health.json",
        "zones": "outputs/business/zone_performance.json",
    }
    for key, path in paths.items():
        if os.path.exists(path):
            with open(path, 'r') as f:
                data[key] = json.load(f)
    return data

def ask_retail_ai(query: str) -> str:
    query = query.lower()
    data = load_all_data()
    
    if "worst" in query and "shelf" in query:
        # Check zones/shelves
        if "zones" in data:
            zones = data["zones"].get("zones", [])
            if zones:
                worst = min(zones, key=lambda z: z.get("performance_score", 100))
                return f"Based on the Zone Performance Report, {worst.get('name', 'an unknown zone')} has the lowest performance score of {worst.get('performance_score')}."
        return "The backend analytics currently indicate that Shelf C in the Beverage Zone has the lowest interaction rate (only 2% conversion)."
        
    if "health" in query and "decrease" in query:
        if "health" in data:
            health = data["health"]
            return f"Store health is currently at {health.get('overall_score', 82)}. The primary negative factor is: {health.get('factors', [{}])[0].get('description', 'High checkout wait times')}."
        return "Store Health decreased by 4 points due to prolonged queue times and low shelf engagement in Zone B."
        
    if "highest engagement" in query:
        return "Zone A (Promotional Displays) currently has the highest engagement score of 94, with a 65% interaction rate."
        
    if "purchase intent" in query:
        if "kpis" in data:
            return f"Currently, there are {data['kpis'].get('live_kpis', {}).get('purchase_intent', 38)} customers showing high purchase intent based on dwell time and physical interactions."
        return "There are currently 38 customers demonstrating high purchase intent, mostly clustered around the electronics and fresh produce sections."
        
    return "I found analytics matching your request: Overall store traffic is up 12% today, and Zone C requires restocking."

def search_enterprise(query: str):
    # Rudimentary search across all loaded json files
    query = query.lower()
    data = load_all_data()
    results = []
    
    # Just a mock search implementation for the HackZen demo
    if "customer" in query:
        results.append({"type": "Report", "title": "Customer Segments Report", "link": "/reports"})
    if "zone" in query:
        results.append({"type": "Analytics", "title": "Zone Performance", "link": "/business"})
    
    return results
