const admin = require("firebase-admin");
const functions = require("firebase-functions");

const db = admin.firestore();

module.exports.deleteInvite = functions.https.onCall(async (data, context) => {
  let findInvite = await db
    .collection("teamInvites")
    .where("inviteeID", "==", data.deletedUID)
    .where("teamID", "==", data.teamID)
    .get();
  if (!findInvite.empty) {
    let inviteID = findInvite.docs[0].id;
    let teamRef = db.collection("teams").doc(data.teamID);
    await teamRef.update({
      teamInvites: admin.firestore.FieldValue.arrayRemove(inviteID)
    });
    await db
      .collection("teamInvites")
      .doc(inviteID)
      .delete();
    return true;
  } else {
    return false;
  }
});
