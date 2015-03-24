# import lxml.html
import bs4
import requests
from time import sleep
from multiprocessing import Pool

### Note: the data table is in an iframe on the HCR's site, here is the iframe's url:
# https://www1.dhcr.state.ny.us/LocalHousingOrgLists/CommBased.aspx?type=rent

BASE_URL = "https://www1.dhcr.state.ny.us/LocalHousingOrgLists"

# table_url = "https://www1.dhcr.state.ny.us/LocalHousingOrgLists/CommBased.aspx?type=rent"

# soup = bs4.BeautifulSoup(urllib2.urlopen(table_url).read())
# soup = bs4.BeautifulSoup(open("html/CommBased.aspx.html"))
org_list = []
org_data = []
headers = {
  'User-Agent' : 'Mozilla/5.0',
  'Host' : 'www1.dhcr.state.ny.us',
  'DNT' : '1',
  'Connection' : 'keep-alive',
  'Cache-control' : 'max-age=0',
  'Accept-Language' : 'en-US',
  'Accept-Encoding' : 'gzip',
  'Accept' : 'text/html',
  'Cookie' : 'ASP.NET_SessionId=bttvatye1qdzah34nfby2d45'
  }

def make_soup(content):
  soup = bs4.BeautifulSoup(content)
  return soup

def make_request(url):
  """
  perform a get request to the dhcr site
  """
  r = requests.get(url, headers=headers)
  
  if r.status_code == requests.codes.ok:
    return r.content

def get_table_data():
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
      org_data.append(content)
      print "org data: %s \n count: %s" % (content, count)
      print "count: %s" % count
    
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

  # print soup

  for row in soup('table')[0].findAll('tr'):
    org_dict = {}
    td = row('td')
    
    if len(td) == 1 and td[0].b is not None:
      county = ''.join(td[0].b.find(text=True))
    
    if len(td) == 2:
      org_dict["name"] = ''.join(td[0].a.find(text=True))
      org_dict["service_area"] = ''.join(td[1].find(text=True))
      org_dict["county"] = county
      
    org_list.append(org_dict)
    print org_dict


def main():
  """
  do everything
  """
  # soup = bs4.BeautifulSoup(get_org_link_data())
  # soup = bs4.BeautifulSoup(make_request())
  # soup = bs4.BeautifulSoup(open("html/CommBased.aspx.html"))
  # strain_soup(soup)
  get_table_data()
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