import pandas as pd
import os
import sqlite3

def read_schedule_excel(file_path):
    try:
        return pd.read_excel(file_path, header=2)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

def clean_column_names(df):
    df.columns = df.columns.str.lower().str.replace('\n', '_').str.replace(' ', '_')
    df = df.rename(columns={
        'rest_days': 'road_team_rest_days',
        'rest_days.1': 'home_team_rest_days',
        'tournament_group': 'tournament_group'
    })
    return df

def create_team_schedules(df):
    team_schedules = {}
    for _, row in df.iterrows():
        for team_type in ['road', 'home']:
            team = row[f'{team_type}_team']
            if team not in team_schedules:
                team_schedules[team] = []
            
            opponent = row['home_team'] if team_type == 'road' else row['road_team']
            rest_days_column = f'{team_type}_team_rest_days'
            rest_days = row[rest_days_column] if rest_days_column in df.columns else None
            
            team_schedules[team].append({
                'date': row['date'],
                'opponent': opponent,
                'is_home': team_type == 'home',
                'rest_days': rest_days,
                'arena': row['arena'],
                'city': row['city']
            })
    
    return {team: pd.DataFrame(schedule) for team, schedule in team_schedules.items()}

def create_schedule_dataframe():
    file_path = os.path.join('data', 'schedule_24_25', '2024-2025_NBA_Regular_Season_Original_Schedule.xlsx')
    df = read_schedule_excel(file_path)
    
    if df is not None:
        df = clean_column_names(df)
        
        # Get unique dates and teams, keeping only year, month, and day
        dates = pd.to_datetime(df['date']).dt.date.sort_values().unique()
        teams = pd.concat([df['road_team'], df['home_team']]).unique()
        
        # Create a DataFrame with teams as rows and dates as columns
        schedule_matrix = pd.DataFrame(index=teams, columns=dates)
        
        # Fill the matrix with 1s where a team has a game, and 0s otherwise
        for _, row in df.iterrows():
            date = pd.to_datetime(row['date']).date()
            schedule_matrix.at[row['road_team'], date] = 1
            schedule_matrix.at[row['home_team'], date] = 1
        
        # Fill NaN values with 0
        schedule_matrix = schedule_matrix.fillna(0)
        
        # Create a dictionary mapping full team names to abbreviations
        team_abbr_map = {
            'Denver Nuggets': 'DEN', 'Dallas Mavericks': 'DAL', 'Milwaukee Bucks': 'MIL',
            'Sacramento Kings': 'SAC', 'Los Angeles Lakers': 'LAL', 'Oklahoma City Thunder': 'OKC',
            'San Antonio Spurs': 'SA', 'Phoenix Suns': 'PHO', 'Indiana Pacers': 'IND',
            'New York Knicks': 'NY', 'Boston Celtics': 'BOS', 'Minnesota Timberwolves': 'MIN',
            'New Orleans Pelicans': 'NO', 'Houston Rockets': 'HOU', 'Philadelphia 76ers': 'PHI',
            'Golden State Warriors': 'GS', 'Los Angeles Clippers': 'LAC', 'Orlando Magic': 'ORL',
            'Cleveland Cavaliers': 'CLE', 'Chicago Bulls': 'CHI', 'Miami Heat': 'MIA',
            'Toronto Raptors': 'TOR', 'Atlanta Hawks': 'ATL', 'Charlotte Hornets': 'CHA',
            'Washington Wizards': 'WAS', 'Brooklyn Nets': 'BKN', 'Memphis Grizzlies': 'MEM',
            'Detroit Pistons': 'DET', 'Utah Jazz': 'UTA', 'Portland Trail Blazers': 'POR'
        }
        
        # Add the abbreviation column
        schedule_matrix['team_abbr'] = schedule_matrix.index.map(team_abbr_map)
        
        # Move the 'team_abbr' column to the second position
        cols = schedule_matrix.columns.tolist()
        cols = ['team_abbr'] + [col for col in cols if col != 'team_abbr']
        schedule_matrix = schedule_matrix[cols]
        
        # Reset the index to make the team names a regular column
        schedule_matrix = schedule_matrix.reset_index()
        
        # Rename the 'index' column to 'team_name'
        schedule_matrix = schedule_matrix.rename(columns={'index': 'team_name'})
        
        # Save the schedule matrix to the database
        conn = sqlite3.connect('data/player_data.db')
        schedule_matrix.to_sql('schedule', conn, if_exists='replace', index=False)
        conn.close()
        
        print("\nSchedule Matrix saved to database.")
        print(schedule_matrix.head())
        
        return schedule_matrix
    
    return None

# Create the schedule dataframe and save it to the database
schedule_matrix = create_schedule_dataframe()