var joiner = require('joiner');
var fs = require('fs');

var list_data = JSON.parse(fs.readFileSync('json/hcr_comm_housing_org_list.json'));
var deets_data = JSON.parse(fs.readFileSync('json/hcr_comm_housing_org_details.json'));
var joined = joiner.left(list_data["HCR List of Community Based Housing Orgs"], 'name', deets_data["HCR Community Based Housing Org details"], 'title');

console.log(JSON.stringify(joined));
