import csv

def print_csv_headers():
    with open('data/fantrax_8_9_24.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Get the first row (headers)
        print("CSV Headers:", headers)

if __name__ == "__main__":
    print_csv_headers()