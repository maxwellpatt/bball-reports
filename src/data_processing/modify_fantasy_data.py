import csv
import os

def simple_modify_csv(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile)
        
        # Print the first row to see what we're working with
        first_row = next(reader)
        print("First row:", first_row)
        
        # Reset the reader
        infile.seek(0)
        reader = csv.DictReader(infile)

        # Rename 'Status' to 'fantasy_team' in the fieldnames
        fieldnames = reader.fieldnames
        if 'Status' in fieldnames:
            fieldnames[fieldnames.index('Status')] = 'fantasy_team'
        
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        rows_written = 0
        for row in reader:
            if 'Status' in row:
                row['fantasy_team'] = row.pop('Status')
            writer.writerow(row)
            rows_written += 1

        print(f"Rows written: {rows_written}")

def main():

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    input_file = os.path.join(project_root, 'data', 'raw', 'fantrax_8_9_24.csv')
    output_file = os.path.join(project_root, 'data', 'processed', 'fantrax_8_9_24_modified.csv')

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    simple_modify_csv(input_file, output_file)
    print(f"CSV file has been modified and saved to {output_file}")

if __name__ == "__main__":
    main()