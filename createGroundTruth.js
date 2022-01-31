const http = require("http");
var fs = require("fs");

// Functions

// Writes JSON object obj with elasticsearch results to a file
function write_to_file(obj) {
  fs.writeFile("groundTruthResults.json", JSON.stringify(obj), function (err) {
    if (err) throw err;
    console.log("Search results saved to groundTruthResults.json");
  });
}

// Takes arg = "[a/b/c]" and separates into array [a,b,c]
function seperate(arg) {
  let firstChar = arg.charAt(0);
  let lastChar = arg.charAt(arg.length - 1);
  if (firstChar === "[" && lastChar === "]") {
    str = arg.slice(1, -1);
    const array = str.split("/");
    return array;
  } else {
    throw "Search term not on correct format";
  }
}

const arg = process.argv[2];
searchArray = seperate(arg);

// Three Elasticsearch searches combined in one to fetch all paragraphs necessary for the ground truth of example [a/b/c/d/e]
const data = JSON.stringify({
  size: 1000,
  query: {
    bool: {
      should: [
        // First, fetch all paragraphs with exactly id=[a/b/c/d/e]
        {
          constant_score: {
            filter: {
              bool: {
                must: [
                  { match_phrase: { id1: searchArray[0] } },
                  { match_phrase: { id2: searchArray[1] || "" } },
                  { match_phrase: { id3: searchArray[2] || "" } },
                  { match_phrase: { id4: searchArray[3] || "" } },
                  { match_phrase: { id5: searchArray[4] || "" } },
                ],
              },
            },
            boost: 3,
          },
        },

        // Second, fetch all paragraphs with id=[a/b/*/*/*]
        {
          constant_score: {
            filter: {
              bool: {
                must_not: {
                  bool: {
                    must: [
                      { match_phrase: { id1: searchArray[0] } },
                      { match_phrase: { id2: searchArray[1] || "" } },
                      { match_phrase: { id3: searchArray[2] || "" } },
                      { match_phrase: { id4: searchArray[3] || "" } },
                      { match_phrase: { id5: searchArray[4] || "" } },
                    ],
                  },
                },
                must: [
                  { match_phrase: { id1: searchArray[0] } },
                  { match_phrase: { id2: searchArray[1] || "" } },
                ],
              },
            },
            boost: 2,
          },
        },

        // Third, fetch all paragraphs with id=[a/*/*/*/*]
        {
          constant_score: {
            filter: {
              bool: {
                must_not: {
                  bool: {
                    must: [
                      { match_phrase: { id1: searchArray[0] } },
                      { match_phrase: { id2: searchArray[1] || "" } },
                    ],
                  },
                },

                must: [{ match_phrase: { id1: searchArray[0] } }],
              },
            },
            boost: 1,
          },
        },
      ],
    },
  },
});

const options = {
  hostname: "localhost",
  port: 9200,
  path: "/paragraphs/_search/",
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    // "Content-Length": "data.length",
  },
  body: data,
};

const req = http.request(options, (res) => {
  console.log(`statusCode: ${res.statusCode}`);

  //   res.on("data", (d) => {
  //     process.stdout.write(d);
  //   });

  var str = "";
  res
    .on("data", (d) => {
      str += d;
    })
    .on("end", () => {
      // write to file
      const obj = JSON.parse(str);
      write_to_file(obj);
    });
});

req.on("error", (error) => {
  console.error(error);
});

req.write(data);
req.end();
