# import lxml.html
import bs4
import requests
import json
from time import sleep

### TO DO (for org data):
## - Get Address of Org
## - Get web url if present
## - skip info if  None such as this case https://www1.dhcr.state.ny.us/LocalHousingOrgLists/Profile.aspx?applid=79

### Note: the data table is in an iframe on the HCR's site, here is the iframe's url:
# https://www1.dhcr.state.ny.us/LocalHousingOrgLists/CommBased.aspx?type=rent

BASE_URL = "https://www1.dhcr.state.ny.us/LocalHousingOrgLists"
ORG_DATA = []
ORG_LIST = []

# soup = bs4.BeautifulSoup(urllib2.urlopen(table_url).read())
# soup = bs4.BeautifulSoup(open("html/CommBased.aspx.html"))

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

def writeJSON(name, data):
  """
  writes org data to JSON out file
  """
  json_data = {
   name : data
  }
  with open('data.json', 'w') as outfile:
    json.dump(json_data, outfile)

def get_table_data():
  """
  perform a get request to the community org data table page
  """
  # table_url = "https://www1.dhcr.state.ny.us/LocalHousingOrgLists/CommBased.aspx?type=rent"
  url = BASE_URL + "/CommBased.aspx"
  content = make_request(url)

  if content is not None:
    return strain_soup(make_soup(content))

def get_org_link_data():
  """
  enumerate over id urls for links in org names
  """
  # link_base_url = "https://www1.dhcr.state.ny.us/LocalHousingOrgLists/Profile.aspx?applid="
  count = 0
  count_finish = 1000
  
  while True:
    if count > count_finish : break
    count = str(count)    
    content = make_request(BASE_URL + "/Profile.aspx?applid=" + count)
    
    if content is not None:
      soup = make_soup(content)
      data = strain_org_deets(soup)
      ORG_DATA.append(data)
    
    print "count: %s" % count
    count = int(count)
    count += 1 
    sleep(1) # keep the server happy :)
  
  if count == count_finish: writeJSON('HCR Community Based Housing Orgs', ORG_DATA)

def strain_org_deets(soup):
  """
  parse out data from org links in data table
  """
  title = soup('h2')[0].find(text=True).title() # Org Title
  address_part1 = soup('h2')[0].next_sibling
  address_part2 = address_part1.next_sibling # line break
  address_part3 = address_part2.next_sibling
  address_comp = address_part1 + ' ' + address_part3

  web_urls = soup.find_all("a", class_="external")
  org_url = web_urls[0].string
  
  if soup.find(id="commBasedPanel") is not None:      
    info = soup.find(id="commBasedPanel").contents # array from div containing the org's info
    
      if info.count(None) != len(info):
        org_type = info[1].string.strip()
        service_area = info[4].string.strip()
        contact = info[8].string.strip()
        phone = info[12].string.strip()
        email = info[17].string.strip()
        about = ''

        for s in soup.find(id="profileLabel").next_siblings:
          if s.string is not None:
            about += s.string.strip()
    
    print "\n"
    print "count: %s" % count
    print "title: %s" % title
    print "address: %s" % address_comp
    print "url: %s" % org_url
    print "contact: %s" % contact
    print "phone: %s" % phone
    print "email: %s" % email
    print "about: %s" %about
    print "\n"

    org_data_dict = {
      "title" : title,
      "address" : address_comp,
      "website url" : org_url,
      "type" : org_type,
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

  for row in soup('table')[0].findAll('tr'):
    org_dict = {}
    td = row('td')
    
    if len(td) == 1 and td[0].b is not None:
      county = ''.join(td[0].b.find(text=True))
    
    if len(td) == 2:
      org_dict["name"] = ''.join(td[0].a.find(text=True))
      org_dict["service_area"] = ''.join(td[1].find(text=True))
      org_dict["county"] = county
      
    ORG_LIST.append(org_dict)
    print org_dict


def main():
  """
  do everything
  """
  # soup = bs4.BeautifulSoup(get_org_link_data())
  # soup = bs4.BeautifulSoup(make_request())
  # soup = bs4.BeautifulSoup(open("html/CommBased.aspx.html"))
  # strain_soup(soup)
  #   get_table_data()
  get_org_link_data()


if __name__ == "__main__":
  main()


#### TESTS #####
## successfully finds one org name:
# print soup('table')[0].findAll('tr')[3].findAll('td')[0].a.string
## successfully finds one org service area:
# print soup('table')[0].findAll('tr')[3].findAll('td')[1].string
## prints region header
# print soup('table')[0].findAll('tr')[1].findAll('td')[0].b.string