const admin = require("firebase-admin");
const functions = require("firebase-functions");

const db = admin.firestore();

module.exports.updateOriginUID = functions.https.onCall(
  async (data, context) => {
    const mydb = db.collection("users").doc(data.uid);
    await mydb.update({
      originUID: data.originUID,
      displayName: data.name
    });
    return;
  }
);
