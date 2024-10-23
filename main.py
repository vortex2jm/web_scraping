from lib.popy import PopyScraping
from dotenv import load_dotenv
import csv
import os


CLIENT_FILE = 'popy_clients.csv'
OPERATOR_FILE = 'popy_operators.csv'


def write_csv(out_file, data, is_header=False):
    with open(out_file, mode='a') as csv_file:
        writer = csv.writer(csv_file)
        if is_header:
            writer.writerow(data.keys())
            return
        writer.writerow(data.values())


def main():
    load_dotenv()

    popy_box = PopyScraping(os.getenv('LOGIN_URL'), os.getenv('USER'), os.getenv('PASSWORD'))
    popy_box.login()
    
    print("Extracting...")

    # Removing previous .csv files
    os.system("rm *.csv")

    #It is for spreadsheet header    
    is_first_client = True
    is_first_operator = True

    for x in range(100):
        
        popy_box.set_scrap_url(f"{os.getenv('CLIENT_URL')}{x}/change/")
        client_data = popy_box.get_client_data()
        
        popy_box.set_scrap_url(f"{os.getenv('OPERATOR_URL')}{x}/change/")
        operator_data = popy_box.get_operator_data()        
        
        if client_data:
            if is_first_client:
                write_csv(CLIENT_FILE, client_data, is_header=True)
                is_first_client = False    
            write_csv(CLIENT_FILE, client_data)

        if operator_data:
            if is_first_operator:
                write_csv(OPERATOR_FILE, operator_data, is_header=True)
                is_first_operator = False    
            write_csv(OPERATOR_FILE, operator_data)
        
    print('Done!')


if __name__ == "__main__":
    main()
