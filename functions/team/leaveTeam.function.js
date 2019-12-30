const admin = require("firebase-admin");
const functions = require("firebase-functions");

const db = admin.firestore();

module.exports.leaveTeam = functions.https.onCall(async (data, context) => {
  let userRef = db.collection("users").doc(data.userID);
  let teamRef = db.collection("teams").doc(data.teamID);
  await teamRef.update({
    teamMembers: admin.firestore.FieldValue.arrayRemove(data.userID)
  });
  await userRef.update({
    teamID: ""
  });
  if ((await teamRef.get()).data().teamMembers.length === 0) {
    await teamRef.delete();
  }
  return;
});
