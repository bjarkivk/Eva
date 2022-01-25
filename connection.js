//This client var can be used whenever we want to perform an operation on the deployment by including the following line
// in any other file we create: var client = require('./connection.js');

// Create an instance of ElasticSearch (ES)
var elasticsearch = require("elasticsearch");

// Create a new ES client
var client = new elasticsearch.Client({
  hosts: ["http://127.0.0.1:9200/"],
});

module.exports = client;

/*
client.ping({
  requestTimeout: 30000
  }, function(error) {
  if (error) {
  console.error('Error Encountered! Elasticsearch cluster is down');
  console.trace('Error:', error);
  
  } else {
  console.log('Connected!');
  }
  // on finish
  client.close();
  });
  */
