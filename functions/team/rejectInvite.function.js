const admin = require("firebase-admin");
const functions = require("firebase-functions");

const db = admin.firestore();

module.exports.rejectInvite = functions.https.onCall(async (data, context) => {
  await db
    .collection("teamInvites")
    .doc(data.inviteID)
    .update({ rejected: true });
  return;
});
