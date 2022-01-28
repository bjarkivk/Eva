var client = require("./connection.js");

client.indices.create(
  {
    index: "paragraphs",
    body: {
      mappings: {
        properties: {
          id1: { type: "keyword" },
          id2: { type: "keyword" },
          id3: { type: "keyword" },
          id4: { type: "keyword" },
          id5: { type: "keyword" },
          paragraph: { type: "text" },
        },
      },
    },
  },
  (err, resp, status) => {
    if (err) {
      console.error(err, status);
    } else {
      console.log("Successfully Created Index", status, resp);
    }
  }
);
