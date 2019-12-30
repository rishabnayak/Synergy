const admin = require("firebase-admin");
const functions = require("firebase-functions");

const db = admin.firestore();

module.exports.acceptInvite = functions.https.onCall(async (data, context) => {
  let userRef = db.collection("users").doc(data.inviteeID);
  let teamRef = db.collection("teams").doc(data.teamID);
  await userRef.update({
    teamID: data.teamID
  });
  await teamRef.update({
    teamMembers: admin.firestore.FieldValue.arrayUnion(data.inviteeID),
    teamInvites: admin.firestore.FieldValue.arrayRemove(data.inviteID)
  });
  await db
    .collection("teamInvites")
    .doc(data.inviteID)
    .delete();
  return;
});
