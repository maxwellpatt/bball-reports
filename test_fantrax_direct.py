import fantraxapi
from src.config.config import config
import json
import requests

def print_json(data):
    print(json.dumps(data, indent=2))  # Print the full response

def login_to_fantrax(username, password):
    login_url = "https://www.fantrax.com/login"
    login_data = {
        "username": username,
        "password": password,
        "rememberMe": True
    }
    session = requests.Session()
    response = session.post(login_url, json=login_data)
    if response.status_code == 200:
        print("Login successful")
        return session
    else:
        print(f"Login failed with status code: {response.status_code}")
        return None

def explore_raw_request(session, league_id, method):
    print(f"\nExploring raw request for '{method}':")
    try:
        payload = {
            "msgs": [{
                "method": method,
                "data": {
                    "leagueId": league_id,
                    "view": "STATS"
                }
            }]
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = session.post(
            "https://www.fantrax.com/fxpa/req",
            json=payload,
            headers=headers
        )
        
        print("Raw response:")
        print_json(response.json())
    except Exception as e:
        print(f"Error making raw request: {type(e).__name__} - {str(e)}")

try:
    print(f"Attempting to log in with username: {config.FANTRAX_USERNAME}")
    session = login_to_fantrax(config.FANTRAX_USERNAME, config.FANTRAX_PASSWORD)
    
    if session:
        methods_to_explore = [
            'getLeagueTeams',
            'getLeagueStandings',
            'getLeagueRosters',
            'getLeagueInfo',
            'getPlayerStats'
        ]
        for method in methods_to_explore:
            explore_raw_request(session, config.FANTRAX_LEAGUE_ID, method)
    else:
        print("Failed to log in. Cannot proceed with API requests.")

except Exception as e:
    print(f"Error: {type(e).__name__}")
    print(f"Error details: {str(e)}")

print("\nScript execution completed.")