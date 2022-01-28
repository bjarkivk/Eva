const http = require("http");

// Functions

// takes arg = "[a/b/c]"  separates into array [a,b,c]
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

// Three searches to fetch all paragraphs necessary for the ground truth of example [a/b/c/d/e]

// First, fetch all paragraphs with exactly id=[a/b/c/d/e] and

// Second, fetch all paragraphs with id=[a/b/*/*/*]

// Third, fetch all paragraphs with id=[a/*/*/*/*]

const data = JSON.stringify({
  size: 1000,
  query: {
    constant_score: {
      filter: {
        bool: {
          must: [
            { match_phrase: { id1: "Polisen i Finland" } },
            { match_phrase: { id2: "" } },
          ],
        },
      },
    },
  },
});

console.log(data);

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
      console.log(str);
      // write to file
    });
});

req.on("error", (error) => {
  console.error(error);
});

req.write(data);
req.end();
