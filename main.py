from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import os
import utils
import csv

def login(login_url):
    session = requests.Session()            # Setting up session
    login_page_res = session.get(login_url)     # Getting login page

    if login_page_res.status_code == 200:
        login_page_html = BeautifulSoup(login_page_res.text, 'html.parser')
        csrf_token = login_page_html.find('input', {'name': 'csrfmiddlewaretoken'})['value']       # Cross Site Request Forgery token
        payload = {
            'username': os.getenv('USER'),
            'password': os.getenv('PASSWORD'),
            'csrfmiddlewaretoken': csrf_token,
            'next': '/admin'
        }   # Auth data
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Referer': login_url        # Extremely necessary
        }   # Req header

        login_res = session.post(login_url, data=payload, headers=headers)   # Doing login
        
        if login_res.status_code == 200:
            print("Login succesfully!")
            return session
        else:
            print(f"Could not login: {login_res.status_code}")
            exit(1)


if __name__ == "__main__":
    load_dotenv()

    session = login(os.getenv('LOGIN_URL'))
    is_first_iter = True

    for x in range(100):

        url = f"{os.getenv('DATA_URL')}{x}/change/"

        res = session.get(url)
        print(res.url)
        print(url)

        if res.url != url:
            continue    

        client_data = BeautifulSoup(res.text, 'html.parser')

        # labels = client_data.find_all('label')
        # inputs = client_data.find_all('input')
        # inputs.pop(0)

        general_info = {}

        for inp_id in utils.INPT_IDS:
            input_element = client_data.find('input', id=inp_id)
            if input_element:
                general_info[inp_id.replace('id_','')] = input_element.get('value', '-')


        for slct_id in utils.SLCT_IDS:
            select_element = client_data.find('select', id=slct_id)
            if select_element:
                selected_option = select_element.find('option', selected=True)
                general_info[slct_id.replace('id_','')] = selected_option.text

        # print(general_info)


        phones = {}

        i = 0
        while True:
            phone_id = f'{utils.PARTIAL_PHONE_ID}{i}'
            tr_element = client_data.find('tr', id=phone_id)
            if not tr_element:
                break

            phone = {}
            for td_class in utils.TD_CLASSES:
                td_element = tr_element.find('td', class_=td_class)
                input_element = td_element.find('input')
                if input_element:
                    phone[td_class.replace('field-','')] = input_element.get('value', '-')
                    continue
                select_element = td_element.find('select')
                if select_element:
                    selected_option = select_element.find('option', selected=True)
                    phone[td_class.replace('field-','')] = selected_option.text
            phones[phone_id.replace('_set-','')] = phone
            i+=1

        # print(phones)


        address = {}
        for addr_id in utils.ADDR_IDS:
            input_element = client_data.find('input', id=addr_id)
            if input_element:
                address[addr_id.replace('id_endereco-0-','')] = input_element.get('value', '-')
        # print(address)


        operator = {}
        select_element = client_data.find('select', id=utils.OPERATOR_ID)
        if select_element:
            selected_option = select_element.find('option', selected=True)
            operator["operadora"] = selected_option.text
        # print(operator)


        data = {**general_info, **phones, **address, **operator}
        # print(data)

        file_name = 'data.csv'
        with open(file_name, mode='a') as csv_file:
            writer = csv.writer(csv_file)
            if is_first_iter:
                writer.writerow(data.keys())
                is_first_iter = False
            writer.writerow(data.values())
