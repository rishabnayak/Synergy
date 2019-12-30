const admin = require("firebase-admin");
const functions = require("firebase-functions");

const db = admin.firestore();

module.exports.createTeam = functions.https.onCall(async (data, context) => {
  let userRef = db.collection("users").doc(data.userID);
  let ref = await db.collection("teams").add(data.teamData);
  let teamID = ref.id;
  await userRef.update({ teamID: teamID });
  return teamID;
});
