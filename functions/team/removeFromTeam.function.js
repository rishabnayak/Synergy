const admin = require("firebase-admin");
const functions = require("firebase-functions");

const db = admin.firestore();

module.exports.removeFromTeam = functions.https.onCall(
  async (data, context) => {
    let teamRef = db.collection("teams").doc(data.teamID);
    await teamRef.update({
      teamMembers: admin.firestore.FieldValue.arrayRemove(data.uid)
    });
    let userDoc = db
      .collection("users")
      .where("originUID", "==", data.uid)
      .get();
    let userID = userDoc.docs[0].id;
    await db
      .collection("users")
      .doc(userID)
      .update({
        teamID: ""
      });
  }
);
