# import lxml.html
import bs4
import requests
from time import sleep
from multiprocessing import Pool

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
      title = soup('h2')[0].find(text=True) # Org Title
      info = soup.find(id="commBasedPanel") # div containing the org's info
      org_type = info.contents[1].string
      service_area = info.contents[4].string
      contact = info.contents[8].string
      phone = info.contents[12].string
      email = info.contents[17].string
      
      if info.contents[-2].string is not None:
        about = info.contents[-2].string + ' ' + info.contents[-1].find(text=True)  
      else:
        about = info.contents[-1].find(text=True)
      
      print "count: %s" % count
      print "title: %s" % title
      print "contact: %s" % contact
      print "phone: %s" % phone
      print "email: %s" % email
      print "about: %s" %about
    
    count = int(count)
    count += 1 
    sleep(1) # keep the server happy :)


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