var client = require("./connection.js");

client.indices.create(
  {
    index: "paragraphs",
    body: {
      mappings: {
        properties: {
          id: { type: "text" },
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
