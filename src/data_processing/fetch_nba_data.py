import requests
from datetime import datetime

def fetch_nba_scores():
    # Assuming you have an API endpoint that provides the scores
    url = f"https://api.sportsdata.io/v3/nba/scores/json/GamesByDate/{datetime.now().strftime('%Y-%m-%d')}"
    headers = {"Ocp-Apim-Subscription-Key": "your_api_key_here"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        games = response.json()
        report = "NBA Scores for " + datetime.now().strftime('%Y-%m-%d') + ":\n"
        for game in games:
            report += f"{game['HomeTeam']} {game['HomeTeamScore']} - {game['AwayTeam']} {game['AwayTeamScore']}\n"
        return report
    else:
        return "Failed to fetch NBA scores."

if __name__ == "__main__":
    scores_report = fetch_nba_scores()
    print(scores_report)
