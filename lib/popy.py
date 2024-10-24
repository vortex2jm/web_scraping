from bs4 import BeautifulSoup
import lib.popy_utils as utils
import requests

class PopyScraping:
    def __init__(self, login_url, user, passwd) -> None:
        self.__scrap_url = None
        self.__login_url = login_url
        self.__user = user
        self.__passwd = passwd
        self.__session = None

    #========================================
    # Set the page to scrap. Only for intern popybox pages!
    def set_scrap_url(self, url: str) -> None:
        self.__scrap_url = url


    #===============
    def login(self):
        try:
            session = requests.Session()            # Setting up session
            login_page_res = session.get(self.__login_url)     # Getting login page

            if login_page_res.status_code == 200:

                login_page_html = BeautifulSoup(login_page_res.text, 'html.parser')
                csrf_token = login_page_html.find('input', {'name': 'csrfmiddlewaretoken'})['value']       # Cross Site Request Forgery token

                payload = {
                    'username': self.__user,
                    'password': self.__passwd,
                    'csrfmiddlewaretoken': csrf_token,
                    'next': '/admin'
                }   # Auth data

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                    'Referer': self.__login_url        # Extremely necessary
                }   # Req header

                login_res = session.post(self.__login_url, data=payload, headers=headers)   # Logging in

                if login_res.url == self.__login_url:   # If it not redirects to admin page
                    raise Exception("Could not login - Incorrect user or password!")

                elif login_res.status_code == 200:  # If it redirect to admin page with accepted status code
                    self.__session = session
                else:   
                    raise Exception(f"Could not login: {login_res.status_code}")
        
        except Exception as e:
            print(f"Login error - {e}")
            exit(1)


    #==========================
    # Gets all client data
    def get_client_data(self):
        if not self.__session:
            print("You must login before get data!")
            exit(1)
        
        try:
            res = self.__session.get(self.__scrap_url)

            if res.url != self.__scrap_url: # If the user does not exists (verify scrap_url)
                return None    

            soup = BeautifulSoup(res.text, 'html.parser')
            general_info = self.__get_client_general_info(soup)
            phones = self.__get_client_phones(soup)
            address = self.__get_client_address(soup)
            operator = self.__get_client_operator(soup)

            return {**general_info, **phones, **address, **operator}        
        except Exception as e:
            print(f"Could not get client data - {e}")
            exit(1)


    #========================================
    def __get_client_general_info(self, soup):
        general_info = {}

        for inp_id in utils.CLIENT_GENERAL_INFO_INPT_IDS:   # Find all input values
            input_element = soup.find('input', id=inp_id)
            if input_element:
                general_info[inp_id.replace('id_','')] = input_element.get('value', '-')

        for slct_id in utils.CLIENT_GENERAL_INFO_SLCT_IDS:  # Find selected option in toggle select
            select_element = soup.find('select', id=slct_id)
            if select_element:
                selected_option = select_element.find('option', selected=True)
                general_info[slct_id.replace('id_','')] = selected_option.text
        
        return general_info


    #==============================
    def __get_client_phones(self, soup):
        phones = {}

        for i in range(9):  # Iter over 9 possible phones
            phone_id = f'{utils.CLIENT_PARTIAL_PHONE_ID}{i}'
            tr_element = soup.find('tr', id=phone_id)
            if not tr_element:
                phones[phone_id.replace('_set-','')] = '{}'
                continue

            phone = {}
            for td_class in utils.CLIENT_PHONES_TD_CLASSES:   # Iter only over existent phones
                td_element = tr_element.find('td', class_=td_class)
                input_element = td_element.find('input')
                if input_element:
                    phone[td_class.replace('field-','')] = input_element.get('value', '-')
                    continue
                select_element = td_element.find('select')
                if select_element:  # Select phone's owner
                    selected_option = select_element.find('option', selected=True)
                    phone[td_class.replace('field-','')] = selected_option.text
            phones[phone_id.replace('_set-','')] = phone
        
        return phones


    #====================================
    def __get_client_address(self, soup):
        address = {}    
        for addr_id in utils.CLIENT_ADDR_IDS:
            input_element = soup.find('input', id=addr_id)
            if input_element:
                address[addr_id.replace('id_endereco-0-','')] = input_element.get('value', '-')
        
        return address


    #=====================================
    def __get_client_operator(self, soup):
        operator = {}
        select_element = soup.find('select', id=utils.CLIENT_OPERATOR_ID)
        if select_element:
            selected_option = select_element.find('option', selected=True)
            operator["operadora"] = selected_option.text

        return operator

    #===========================
    def get_operator_data(self):
        if not self.__session:
            print("You must login before get data!")
            exit(1)
        
        try:
            res = self.__session.get(self.__scrap_url)

            if res.url != self.__scrap_url: # If the operator does not exists (verify scrap_url)
                return None    

            soup = BeautifulSoup(res.text, 'html.parser')
            
            general_info = self.__get_operator_general_info(soup)
            phones = self.__get_operator_phones(soup)
            address = self.__get_operator_address(soup)
            clients = self.__get_operator_clients(soup)

            return {**general_info, **phones, **address, **clients}
                
        except Exception as e:
            print(f"Could not get operator data - {e}")
            exit(1)
    
    #==========================================
    def __get_operator_general_info(self, soup):
        general_info = {}

        for inp_id in utils.OPERATOR_GENERAL_INFO_INPT_IDS:   # Find all input values
            input_element = soup.find('input', id=inp_id)
            if input_element:
                general_info[inp_id.replace('id_','')] = input_element.get('value', '-')

        for slct_id in utils.OPERATOR_GENERAL_INFO_SLCT_IDS:  # Find selected option in toggle select
            select_element = soup.find('select', id=slct_id)
            if select_element:
                selected_option = select_element.find('option', selected=True)
                general_info[slct_id.replace('id_','')] = selected_option.text
        
        return general_info


    def __get_operator_phones(self, soup):
        phones = {}

        for i in range(15):  # Iter over 9 possible phones
            phone_id = f'{utils.OPERATOR_PARTIAL_PHONE_ID}{i}'
            tr_element = soup.find('tr', id=phone_id)
            if not tr_element:
                phones[phone_id.replace('_set-','')] = '{}'
                continue

            phone = {}
            for td_class in utils.OPERATOR_PHONE_TD_CLASSES:   # Iter only over existent phones
                td_element = tr_element.find('td', class_=td_class)
                input_element = td_element.find('input')
                if input_element:
                    phone[td_class.replace('field-','')] = input_element.get('value', '-')
                    continue
                select_element = td_element.find('select')
                if select_element:  # Select phone's owner
                    selected_option = select_element.find('option', selected=True)
                    phone[td_class.replace('field-','')] = selected_option.text
            phones[phone_id.replace('_set-','')] = phone
        
        return phones

    #=====================================
    def __get_operator_clients(self, soup):
        clients = {}

        for i in range(15):
            client_id = f'{utils.OPERATOR_PARTIAL_CLIENT_ID}{i}'
            tr_element = soup.find('tr', id=client_id)
            if not tr_element:
                clients[client_id.replace('_set-','')] = '{}'
                continue

            client = {}
            td_element = tr_element.find('td', class_=utils.OPERATOR_CLIENT_TD_CLASS)
            select_element = td_element.find('select')
            if select_element:
                selected_option = select_element.find('option', selected=True)
                client[utils.OPERATOR_CLIENT_TD_CLASS.replace('field-','')] = selected_option.text

            clients[client_id.replace('_set-','')] = client
        return clients

    #=====================================
    def __get_operator_address(self, soup):
        address = {}    
        for addr_id in utils.OPERATOR_ADDR_IDS:
            input_element = soup.find('input', id=addr_id)
            if input_element:
                address[addr_id.replace('id_endereco-0-','')] = input_element.get('value', '-')
        
        return address


    #=========================
    def get_circuit_data(self):
        if not self.__session:
            print("You must login before get data!")
            exit(1)
        
        try:
            res = self.__session.get(self.__scrap_url)

            if res.url != self.__scrap_url: # If the operator does not exists (verify scrap_url)
                return None    

            soup = BeautifulSoup(res.text, 'html.parser')
            
            circuits = []
            circuit_table = soup.find('table', id='result_list')

            table_rows = circuit_table.find_all('tr')

            for row in table_rows:
                circuit = {}
                th_element = row.find('th', class_=utils.CIRCUIT_DESIGNATION_ID)
                if th_element:
                    circuit[utils.CIRCUIT_DESIGNATION_ID.replace('field-','')] = th_element.get_text()
                for td_id in utils.CIRCUIT_ROW_IDS:
                    td_element = row.find('td', class_=td_id)
                    if td_element:
                        circuit[td_id.replace('field-','')] = td_element.get_text()
                circuits.append(circuit)    

            return list(filter(bool, circuits))
                
        except Exception as e:
            print(f"Could not get circuit data - {e}")
            exit(1)
