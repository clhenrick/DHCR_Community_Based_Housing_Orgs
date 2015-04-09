import bs4
import requests
import json
from time import sleep

### Note: the data table is in an iframe on the HCR's site, here is the iframe's url:
# https://www1.dhcr.state.ny.us/LocalHousingOrgLists/CommBased.aspx?type=rent

BASE_URL = "https://www1.dhcr.state.ny.us/LocalHousingOrgLists"
ORG_DATA = []
ORG_LIST = []

def make_soup(content):
  """
  convert content from a requests response to be parsable by BeautifulSoup
  """
  soup = bs4.BeautifulSoup(content)
  return soup

def make_request(url):
  """
  perform a get request for a given url
  """
  r = requests.get(url) 
  if r.status_code == requests.codes.ok:
    return r.content

def writeJSON(name, data, filename):
  """
  writes org data to JSON out file
  """
  json_data = {
   name : data
  }
  with open(filename, 'w') as outfile:
    json.dump(json_data, outfile)

def get_table_data_from_url():
  """
  perform a get request to the community org data table page
  """
  # table_url = "https://www1.dhcr.state.ny.us/LocalHousingOrgLists/CommBased.aspx?type=rent"
  url = BASE_URL + "/CommBased.aspx"
  content = make_request(url)

  if content is not None:
    return strain_soup(make_soup(content))

def get_table_data_from_file():
  """
  grab the table data from a local file
  """
  f = open('html/CommBased.aspx.html')
  strain_soup(make_soup(f))

def get_org_link_data():
  """
  enumerate over id urls for links in org names
  """
  # link_base_url = "https://www1.dhcr.state.ny.us/LocalHousingOrgLists/Profile.aspx?applid="
  count = 8
  count_finish = 10000
  
  while True:
    if count > count_finish: 
      writeJSON('HCR Community Based Housing Org details', ORG_DATA, 'hcr_comm_housing_org_details.json')
      break
    
    count = str(count)    
    content = make_request(BASE_URL + "/Profile.aspx?applid=" + count)
    
    if content is not None:
      soup = make_soup(content)

      if 'Runtime Error' not in soup.title.string:    
        data = strain_org_deets(soup, count)

        if data is not None:
          ORG_DATA.append(data)
    
    print "count: %s" % count
    count = int(count)
    count += 1 
    sleep(1) # keep the server happy :)

def check_length(string):
  """
  Check a values length to determine whether to keep it or not
  """
  if len(string) > 0:
    return string
  else:
    return 'not listed'

def find_address(bs4_tag):
  """
  grab each line after the h2 org title and before the div#commBasedPanel
  """
  address = []
  for s in bs4_tag.next_siblings:
    if type(s) == bs4.element.NavigableString:
      address.append(s.string.strip())
    elif type(s) == bs4.element.Tag:
      if s.get('id') is not None:
        return ' '.join(address).strip()    
      else:
        continue
    elif type(s) == None:
      continue
    else:
      return

def strain_org_deets(soup, applid):
  """
  parse out data from org links in data table
  """
  hcr_data_url = BASE_URL + "/Profile.aspx?applid=" + applid
  title = soup('h2')[0].find(text=True).title() # Org Title
  address = find_address(soup('h2')[0])
  web_urls = soup.find_all("a", class_="external")
  
  if len(web_urls) > 0:
    org_url = web_urls[0].string
  else:
    org_url = ''
  
  if soup.find(id="commBasedPanel") is not None:      
    info = soup.find(id="commBasedPanel").contents # array from div containing the org's info
    service_area = check_length(soup.find(id="serviceAreaLabel").next_sibling.string.strip())
    contact = check_length(soup.find(id="contactLabel").next_sibling.string.strip())
    phone = check_length(soup.find(id="phoneLabel").next_sibling.string.strip())
    email_pre = soup.find(id="emailLabel").next_sibling

    if email_pre.next_sibling.string is not None:
      email = check_length(email_pre.next_sibling.string.strip())
    else:
      email = 'not listed'
    about = ''

    for s in soup.find(id="profileLabel").next_siblings:
      if s.string is not None:
        about += s.string.strip()
    
    print "\n"
    print "hcr data url: %s" % hcr_data_url
    print "title: %s" % title
    print "address: %s" % address
    print "url: %s" % org_url
    print "contact: %s" % contact
    print "phone: %s" % phone
    print "email: %s" % email
    print "about: %s" %about
    print "\n"

    org_data_dict = {
      "hcr_data_url" : hcr_data_url,
      "title" : title,
      "address" : address,
      "website url" : org_url,
      "service area" : service_area,
      "contact person" : contact,
      "phone no." : phone,
      "email" : email,
      "description" : about
    }
    
    return org_data_dict


def strain_soup(soup):
  """
  iterate over html table and pull out county, org name & org service area
  """
  ### The code below works when loading a local html file,
  ### but not parsing a response from a server...
  ### issue seems to do with python on my mac?
  #

  t_length = len(soup('table')[0].findAll('tr'))
  count = 1

  while True:
    if count > t_length: 
      writeJSON('HCR List of Community Based Housing Orgs', ORG_LIST, 'hcr_comm_housing_org_list.json')
      break

    for row in soup('table')[0].findAll('tr'):
      org_dict = {}
      td = row('td')
      
      if len(td) == 1 and td[0].b is not None:
        county = ''.join(td[0].b.find(text=True)).strip()
      
      if len(td) == 2:
        org_dict["name"] = ''.join(td[0].a.find(text=True)).strip().title()
        org_dict["service_area"] = ''.join(td[1].find(text=True)).strip()
        org_dict["county"] = county
      
      print org_dict
      count +=1

      if not org_dict:
        continue
      else:
        ORG_LIST.append(org_dict)

def main():
  """
  do everything
  """
  get_table_data_from_file()
  get_org_link_data()


if __name__ == "__main__":
  main()
