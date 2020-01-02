const admin = require("firebase-admin");
const functions = require("firebase-functions");
const parse = require("csv-parse");

const db = admin.firestore();

module.exports.populateTTBdata = functions.https.onRequest(async (req, res) => {
  parse(
    req.body,
    {
      record_delimiter: "\n",
      delimiter: ","
    },
    (err, output) => {
      if (err) {
        console.log("ERROR", err);
        res.status(500).send(err);
      }

      let num_records = output.length - 1;
      let num_fields = output[0].length;

      let field_names = output[0];
      let user_records = output.slice(1);

      Promise.all(
        user_records.map(async user_record => {
          let id = user_record[0];
          let user_data = {};
          for (
            let feature_index = 0;
            feature_index < num_fields;
            feature_index++
          ) {
            let feature_value = user_record[feature_index];
            let feature_name = field_names[feature_index];

            if (isArray(feature_value)) {
              user_data[feature_name] = JSON.parse(feature_value);
            } else {
              user_data[feature_name] = feature_value;
            }
          }

          await db
            .collection("TTBUsers")
            .doc(id)
            .set(user_data)
            .then(() => {
              console.log("Set user record with ID", id);
              return;
            })
            .catch(err => {
              console.log("Error:", err);
              res.status(500).send(err);
            });
        })
      )
        .then(() => {
          console.log("All finished");
          res.status(200).send("Success!");
          return;
        })
        .catch(err => {
          console.log("Error:", err);
          res.status(500).send(err);
        });
    }
  );
});

function isArray(input) {
  return input[0] === "[";
}