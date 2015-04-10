var joiner = require('joiner');
var fs = require('fs');
var jsoncsv = require('json-csv');

var list_data = JSON.parse(fs.readFileSync('hcr_comm_housing_org_list.json'));
var deets_data = JSON.parse(fs.readFileSync('hcr_comm_housing_org_details.json'));
var joined = joiner.left(list_data, 'name', deets_data, 'title');

console.log(JSON.stringify(joined));

function json2csv(data, options, callback) {
  jsoncsv.csvBuffered(data, options, callback);
}

function writeFile() {
  // easier to pipe console.log to some-file.csv in terminal
  return;
}

csv_options = {
  fields : [
    {
      name : 'name',
      label : 'organization name'
    },
    {
      name : 'county',
      label : 'county'
    },
    {
      name : 'service_area',
      label : 'service area'
    },
    {
      name : 'website url',
      label : 'website'
    },
    {
      name : 'email',
      label : 'email'
    },
    {
      name : 'phone no',
      label : 'phone',
    },
    {
      name : 'contact person',
      label : 'contact person'
    },
    {
      name : 'service area',
      label : 'service area'
    },
    {
      name : 'address',
      label : 'address'
    },
    {
      name  : 'hcr_data_url',
      label : 'hcr url'
    },
    {
      name : 'description',
      label : 'description'
    }
  ]
};

// json2csv(deets_data, csv_options, function(err,csv){
//   if (err) { console.log(err); return; }
//   console.log(csv);
// });