from lib.popy import PopyScraping
from dotenv import load_dotenv
import csv
import os

OUT_FILE_NAME = 'out.csv'

def main():
    load_dotenv()

    popy_box = PopyScraping(os.getenv('LOGIN_URL'), os.getenv('USER'), os.getenv('PASSWORD'))
    popy_box.login()
    
    print("Extracting...")
    is_first_iter = True
    for x in range(100):
        
        popy_box.set_scrap_url(f"{os.getenv('DATA_URL')}{x}/change/")
        client_data = popy_box.get_client_data()
        if not client_data:
            continue
        
        with open(OUT_FILE_NAME, mode='a') as csv_file:
            writer = csv.writer(csv_file)
            if is_first_iter:
                writer.writerow(client_data.keys())
                is_first_iter = False
            writer.writerow(client_data.values())
    print('Done!')

if __name__ == "__main__":
    main()
