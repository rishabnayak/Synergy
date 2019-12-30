const admin = require("firebase-admin");
const functions = require("firebase-functions");

const db = admin.firestore();

module.exports.createInvite = functions.https.onCall(async (data, context) => {
  let teamRef = db.collection("teams").doc(data.teamID);
  let ref = await db.collection("teamInvites").add(data.teamInviteData);
  let teamInviteID = ref.id;
  await teamRef.update({
    teamInvites: admin.firestore.FieldValue.arrayUnion(teamInviteID)
  });
  return;
});
