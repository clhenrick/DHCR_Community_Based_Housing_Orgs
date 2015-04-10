var joiner = require('joiner');
var fs = require('fs');

var list_data = JSON.parse(fs.readFileSync('hcr_comm_housing_org_list.json'));
var deets_data = JSON.parse(fs.readFileSync('hcr_comm_housing_org_details.json'));
var joined = joiner.left(list_data, 'name', deets_data, 'title');

console.log(JSON.stringify(joined));
