# import lxml.html
import bs4
import urllib2

# the table is in an iframe, here is the iframe's url:
table_url = "https://www1.dhcr.state.ny.us/LocalHousingOrgLists/CommBased.aspx?type=rent"

#soup = bs4.BeautifulSoup(urllib2.urlopen(table_url).read())
soup = bs4.BeautifulSoup(open("html/CommBased.aspx.html"))

org_list = []

def main():
  """
  iterate over html table and pull out county, org name & org service area
  """

  for row in soup('table')[0].findAll('tr'):
    org_dict = {}
    td = row('td')

    if len(td) == 1:
      county = ''.join(td[0].b.find(text=True))      

    if len(td) == 2:
      org_dict["name"] = ''.join(td[0].a.find(text=True))
      org_dict["service_area"] = ''.join(td[1].find(text=True))
      org_dict["county"] = county
    
    print org_dict

if __name__ == "__main__":
  main()

#### TESTS #####
## successfully finds one org name:
# print soup('table')[0].findAll('tr')[3].findAll('td')[0].a.string
## successfully finds one org service area:
# print soup('table')[0].findAll('tr')[3].findAll('td')[1].string
## prints region header
# print soup('table')[0].findAll('tr')[1].findAll('td')[0].b.string