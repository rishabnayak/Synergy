const admin = require("firebase-admin");
const functions = require("firebase-functions");
const parse = require("csv-parse");

const db = admin.firestore();

module.exports.populateRecs = functions.https.onRequest(async (req, res) => {
  let unavail_id = [];
  parse(req.body, {}, (err, output) => {
    if (err) {
      console.log("ERROR:", err);
      res.status(500).send(err);
    }

    let user_recs = output.slice(1);
    Promise.all(
      user_recs.map(async user_record => {
        let id = user_record[0];
        let recommendations = JSON.parse(user_record[2]);

        let userRef = db.collection("TTBUsers").doc(id);
        let doc = await userRef.get();

        if (doc.exists) {
          await userRef
            .update({
              recommendations: recommendations
            })
            .then(() => {
              console.log("Update recs for user with ID", id);
              return;
            })
            .catch(err => {
              console.log("Error", err);
              res.status(500).send(err);
            });
        } else {
          console.log("Cannot find user with ID", id);
          unavail_id.push(id);
        }
      })
    )
      .then(() => {
        if (unavail_id.length === 0) {
          console.log("All finished");
          res.status(200).send("Success!\n");
        } else {
          res.status(500).send(`Cannot find these ids: ${unavail_id}\n`);
        }
        return;
      })
      .catch(err => {
        console.log("Error:", err);
        res.status(500).send(err);
      });
  });
});
