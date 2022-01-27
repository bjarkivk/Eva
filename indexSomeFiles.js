const http = require("http");
const fs = require("fs");
const util = require("util");

const jsonstring = fs.readFileSync(
  __dirname + "/scraper/paragraphs.json",
  "utf-8"
);

const data = jsonstring;
console.log(data);

const options = {
  hostname: "localhost",
  port: 9200,
  path: "/paragraphs/_bulk/",
  method: "PUT",
  headers: {
    "Content-Type": "application/json",
    // 'Content-Length': data.length
  },
};

const req = http.request(options, (res) => {
  console.log(`statusCode: ${res.statusCode}`);

  res.on("data", (d) => {
    process.stdout.write(d);
  });
});

req.on("error", (error) => {
  console.error(error);
});

req.write(data);
req.end();
