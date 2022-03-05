from bs4 import BeautifulSoup
import requests
import time
import csv

my_url = "https://www.epa.gov/enforcement/coal-fired-power-plant-enforcement"

#url list func
def get_urls_from_single_page(epa_url):
    page = requests.get(my_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    #empty list to hold all URLs
    epa_url_list = []
    #get the URLs and write them one-by-one into the list
    cast = soup.find('article')
    links = cast.find_all('a')
    for link in links:
        if 'href' in link.attrs:
            epa_url_list.append(link.attrs['href'])

    return epa_url_list

# call the function
url_list = get_urls_from_single_page(my_url)

#scrape func

test_url = "/enforcement/salt-river-project-agriculture-improvement-and-power-district-settlement"

def scrape_violation(violation_list):
    page = requests.get('https://www.epa.gov/' + violation_list)
    soup = BeautifulSoup(page.text, 'html.parser')

    #get name
    name = soup.find('h1').text.strip()

    # get penalty
    penalty = 'nothing'

    if soup.find('h2', text='Civil Penalty'):
        penalty = soup.find('h2', text='Civil Penalty').next_sibling.next_sibling.get_text()
        if penalty == 'Comment Period':
            penalty = soup.find('h2', text='Civil Penalty').next_sibling.get_text()
    elif soup.find('h3', text='Civil Penalty'):
        penalty = soup.find('h3', text='Civil Penalty').next_sibling.next_sibling.get_text()
        if penalty == 'Comment Period':
            penalty = soup.find('h3', text='Civil Penalty').next_sibling.get_text()
    elif soup.find('h3', text='Civil Penalties'):
        penalty = soup.find('h3', text='Civil Penalties').next_sibling.next_sibling.get_text()
        if penalty == None:
            soup.find('h3', text='Civil Penalties').next_sibling.get_text()
    elif soup.find(id='penalty'):
        penalty = soup.find(id='penalty').next_sibling.get_text()
        if penalty == None:
            soup.find(id='penalty').next_sibling.next_sibling.get_text()
    elif soup.find(id='civil'):
        penalty = soup.find(id='civil').next_sibling.next_sibling.get_text()
        if penalty == 'Comment Period':
            soup.find(id='civil').next_sibling.get_text()
    elif soup.find(id='civilpenalty'):
        penalty = soup.find(id='civilpenalty').next_sibling.get_text()
        if penalty == None:
            soup.find(id='civilpenalty').next_sibling.next_sibling.get_text()
    elif soup.find(id='penalties'):
        penalty = soup.find(id='penalties').next_sibling.get_text()
    elif soup.find('a', id='penalty'):
        penalty = soup.find('a', id='penalty').next_element.get_text()

    elif soup.find('p', text='Civil Penalty'):
        penalty = soup.find('p', text='Civil Penalty').get_text()
    elif soup.find('li', text='Civil Penalty'):
        penalty = soup.find('li', text='Civil Penalty').next_element.get_text()
    elif soup.find('p', id='mitigation'):
        penalty = soup.find('p', id='mitigation').get_text()
    elif soup.find('h2', text='Civil Penalties and Environmental Projects'):
        penalty = soup.find('h2', text='Civil Penalties and Environmental Projects').next_element.get_text()
    elif soup.find('strong', text="Civil Penalty"):
        penalty = soup.find('strong', text="Civil Penalty").next_sibling.get_text()
    else:
        penalty = "none found"

    #get consent
    consent = 'none'
    consent_string = soup.find_all('a', href=True, text='Consent Decree')
    for c in consent_string:
        consent = c['href']

    #get complaint
    complaint = 'none'
    complaint_string = soup.find_all('a', href=True, text='Complaint')
    for x in complaint_string:
        complaint = x['href']

    #return list
    final_list = [name, penalty, consent, complaint]
    return final_list
# call the function
vio_deets = scrape_violation(test_url)

print(vio_deets)

#csv func

def write_csv(url_list):
    csvfile = open('air_pollution.csv', 'w', newline='', encoding='utf-8')
    c = csv.writer(csvfile)

    c.writerow(['name', 'civil penalty', 'consent', 'complaint', 'partial_url'])

    for x in url_list:
        whole_list = (scrape_violation(x))
        whole_list.append(x)
        c.writerow(whole_list)
        time.sleep(1)

    # close the file - end of function
    csvfile.close()

# run the function
write_csv(url_list)
