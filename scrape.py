import csv
import json
from bs4 import BeautifulSoup as bs
import requests

states = ['AL', 'AK', 'AZ', 'AR', 'CA',
          'CO', 'CT', 'DE', 'DC', 'FL',
          'GA', 'HI', 'ID', 'IL', 'IN',
          'IA', 'KS', 'KY', 'LA', 'ME',
          'MD', 'MA', 'MI', 'MN', 'MS',
          'MO', 'MT', 'NE', 'NV', 'NH',
          'NJ', 'NM', 'NY', 'NC', 'ND',
          'OH', 'OK', 'OR', 'PA', 'RI',
          'SC', 'SD', 'TN', 'TX', 'UT',
          'VT', 'VA', 'WA', 'WV', 'WI',
          'WY']
BASE = 'https://agents.farmers.com'
POST_EMAIL = '@farmersagent.com'

with open('data.csv', 'w') as f:
    writer = csv.writer(f,
                        delimiter=',',
                        quotechar='"',
                        quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Name', 'Address', 'Phone', 'Email', 'URL'])

    for i in states:
        print("Scraping state: {}".format(i))
        search = "{}/search.html".format(BASE)
        params = {
            'state': i
        }
        state_page = requests.get(search, params=params)
        state = bs(state_page.content, 'html.parser')

        if state.find('div', {'class': 'no-results-message'}):
            print('Unable to find any agents by that state')
            continue

        # with open('hihi.html', 'w') as f:
        #   f.write(str(soup))

        items = state.find_all('div', {'class':  'location-item'})

        for i in items:
            ar = i.find('a', {'class': 'location-title-link'})['href']
            link = f"{BASE}/{ar}"
            agent_page = requests.get(link)
            agent = bs(agent_page.content, 'html.parser')

            agent_info = json.loads(agent.find(
                'script', {'id': 'js-agentInfo'}).text)
            name = agent_info['customByName']['AgentName']
            email = f"{agent_info['customByName']['Agent Vanity Url Path']}{POST_EMAIL}"
            print(name, end='\t')
            
            agent_info = json.loads(agent.find(
                'script', {'id': 'js-contact-modal-0'}).text)
            address = agent_info['address1']
            numbers = agent_info['phones']
            main = list(filter(lambda x: x["type"] == "MAIN", numbers))[0]
            phone = main['number']

            writer.writerow([name, address, phone, email, link])

        print('\n----------------\n')
