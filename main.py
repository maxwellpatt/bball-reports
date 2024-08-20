from src.data_processing.modify_fantasy_data import main as modify_data
from src.data_processing.fetch_nba_data import main as fetch_data
from src.email.email_nba_data import job as email_job

def main():
    print("Modifying fantasy data...")
    modify_data()
    
    print("Fetching NBA data...")
    fetch_data()
    
    print("Sending email...")
    email_job()

if __name__ == "__main__":
    main()