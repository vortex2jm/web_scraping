from lib.popy import PopyScraping
from dotenv import load_dotenv
import csv
import os


CLIENT_FILE = 'popy_clients.csv'
OPERATOR_FILE = 'popy_operators.csv'
CIRCUIT_FILE = 'popy_circuits.csv'


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
    
    print("Logging in...\n")
    popy_box.login()

    # Removing previous .csv files
    os.system("rm *.csv")

    #It is for spreadsheet header    
    is_first_client = True
    is_first_operator = True
    is_first_circuit = True
    
    for x in range(100):
        
        # Cleints
        popy_box.set_scrap_url(f"{os.getenv('CLIENT_URL')}{x}/change/")
        client_data = popy_box.get_client_data()
        
        # Operators
        popy_box.set_scrap_url(f"{os.getenv('OPERATOR_URL')}{x}/change/")
        operator_data = popy_box.get_operator_data()        

        if client_data:
            if is_first_client:
                print("Extracting clients...\n")
                write_csv(CLIENT_FILE, client_data, is_header=True)
                is_first_client = False    
            write_csv(CLIENT_FILE, client_data)

        if operator_data:
            if is_first_operator:
                print("Extracting operators...\n")
                write_csv(OPERATOR_FILE, operator_data, is_header=True)
                is_first_operator = False    
            write_csv(OPERATOR_FILE, operator_data)
        
    # Circuits
    popy_box.set_scrap_url(f"{os.getenv('CIRCUIT_URL')}")
    circuit_data = popy_box.get_circuit_data()
    
    for circuit in circuit_data:
        if is_first_circuit:
            write_csv(CIRCUIT_FILE, circuit, is_header=True)
            is_first_circuit = False
        write_csv(CIRCUIT_FILE, circuit)

    print('Done!')

if __name__ == "__main__":
    main()
