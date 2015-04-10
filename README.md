NY DHCR Community Housing Organization list information
=========
This is a script that pulls down information on the [New York Homes and Community Renewal](http://www.nyshcr.org/)'s list of [community housing based organizations](http://www.nyshcr.org/Rent/HousingOrgs.htm) that are currently stuck in a not so useful HTML table that contains links to the organization details such as contact info, website, service area, etc. 

These orgs perform work related to affordable housing, community development and civil legal services in New York State and New York City. 

This was originally coded as a scraper that runs on [Morph](https://morph.io) but has since been altered. To get started with Morph [see the documentation](https://morph.io/documentation).

## Installation
Requires Python with pip and Node JS with npm.

First, in terminal `cd` to the folder containing this repo.

To grab python dependencies do:  
`pip install python-requirements.txt`

To grab Node JS dependencies do:  
`npm install`

## Usage

Do `python scraper.py` to create the json file of the HCR organization list and pull down the organization details from the HCR's server. This will take a while.

Then do `node join_json.js > data_joined.json` to join the JSON files of organization list and organization details and output them to a joined JSON file.

I manually converted the data from JSON to CSV format using an [web data converter](http://konklone.io/json/).

**Note:** there are more organizations listed in the organization details JSON file. I believe this has to do with the HCR listing organizations elsewhere on their website, some of these may relate to housing and community development but for whatever reason are not listed on the original HTML table.