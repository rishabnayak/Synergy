const admin = require("firebase-admin");
const functions = require("firebase-functions");

const db = admin.firestore();

module.exports.declineRecommendation = functions.https.onCall(
  async (data, context) => {
    let userRef = db.collection("TTBUsers").doc(data.uid);
    await userRef.update({
      recommendations: admin.firestore.FieldValue.arrayRemove(data.declinedUID)
    });
    return;
  }
);
