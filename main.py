from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import os

load_dotenv()

login_url = os.getenv('LOGIN_URL')
data_url = os.getenv('DATA_URL')

# Setting up session
session = requests.Session()

# Getting login page
login_page = session.get(login_url)

if login_page.status_code == 200:

    login_page_html = BeautifulSoup(login_page.text, 'html.parser')
    
    # Cross Site Request Forgery token
    csrf_token = login_page_html.find('input', {'name': 'csrfmiddlewaretoken'})['value']

    # Authentication data
    payload = {
        'username': os.getenv('USER'),
        'password': os.getenv('PASSWORD'),
        'csrfmiddlewaretoken': csrf_token,
        'next': '/admin'
    }

    # Request header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': login_url        # Extremely necessary
    }

    # Doing login
    response = session.post(login_url, data=payload, headers=headers)
    if response.status_code == 200:
        print("Login succesfully!")
    else:
        print(f"Could not login: {response.status_code}")
        exit(1)

    # for i in range(100):
        # url = f"{os.getenv('DATA_URL')}{i}/change/"
        # res =session.head(url) 
        # if res.status_code == 200:
            # print(i, res.url)
            

    url = f"{os.getenv('DATA_URL')}{37}/change/"
    res = session.get(url)
    client_data = BeautifulSoup(res.text, 'html.parser')
    
    labels = client_data.find_all('label')
    inputs = client_data.find_all('input')

    for label, input_field in zip(labels, inputs):
        label_text = label.get_text(strip=True)
        # input_value = input_field['value']
        input_value = input_field.get('value', 'Valor não disponível') 
        print(f"Texto do Label: {label_text}, Valor do Input: {input_value}")

    # print(client_data)


    # print(page_id)

    # Accessing clients pages
    # data_response = session.get(data_url)

    # Analisar o conteúdo
    # client_data = BeautifulSoup(data_response.text, 'html.parser')

    # Extrair os dados desejados
    # Por exemplo, extrair todos os títulos de uma lista
    # for title in client_data.find_all('h1'):
        # print(title.get_text())


# if __name__ == "__main__":
