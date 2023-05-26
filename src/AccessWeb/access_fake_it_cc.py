import requests
import sqlite3
import random
import pytz
import json
import urllib3
from bs4 import BeautifulSoup
from datetime import datetime

class BrowserAccess():
    def decode(self, cfemail):
        enc = bytes.fromhex(cfemail)
        return bytes([c ^ enc[0] for c in enc[1:]]).decode('utf8')

    def search_name_and_address(self, soup: BeautifulSoup, count: int):
        table = soup.find("table")
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            for cell in range(len(cells)):
                if count == 1:
                    name = cells[cell].text
                elif count == 2:
                    address = cells[cell].text
                count += 1
        return name, address

    def check_lenght_of_names(self, name: str):
        name = name.split()
        if len(name) >= 3:
            first_name = name[0]
            last_name = name[2]
        else:
            first_name = name[0]
            last_name = name[1]
        return first_name, last_name

    def fetch_last_element_table(self, id_pessoa: str):
        return id_pessoa

    def get_and_decript_email(self, soup: BeautifulSoup):
        count_email = 0
        for encrypted_email in soup.select('a.__cf_email__'):
            if count_email == 1:
                mail = self.decode(encrypted_email['data-cfemail'])
                count_email = 0
                break
            count_email += 1
        return mail


    def access_method(self, message: str):
        arr_elements = []
        count = 0
        dataQuery = {}

        s = json.loads(message)
        message = s['value']

        with open('src//configs//config.json') as f:
            path = json.loads(f.read())

        today = datetime.utcnow().replace(tzinfo=pytz.utc)
        url = path['uri']
        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        #### connect with PersonAPI ####
        dataQuery = {
            'Nome': self.search_name_and_address(soup, count)[0], 
            'Address': self.search_name_and_address(soup, count)[1], 
            'Email': self.get_and_decript_email(soup)
        }

        ### insert element dataLoad ###
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        data_tuple = (
            self.fetch_last_element_table(message), 
            self.check_lenght_of_names(self.search_name_and_address(soup, count)[0])[0], 
            self.check_lenght_of_names(self.search_name_and_address(soup, count)[0])[1], 
            str(dataQuery['Email']), 
            today.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), 
            random.randint(0, 1000)
            )

        print(data_tuple)

        ### Post element build in PersonAPI for create person
        payload = {
            "pessoas": {
                "id_Pessoas": data_tuple[0],
                "nome": data_tuple[1],
                "sobrenome": data_tuple[2],
                "email": data_tuple[3],
                "pessoas_Calc_Number": data_tuple[5],
                "dataHora": data_tuple[4]
            }
        }

        return payload

    