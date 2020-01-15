const admin = require("firebase-admin");
const functions = require("firebase-functions");
const aws = require("aws-sdk");

var ses = new aws.SES({
  accessKeyId: functions.config().aws.key,
  secretAccessKey: functions.config().aws.secret,
  region: "us-east-1"
});

const db = admin.firestore();

module.exports.createInvite = functions.https.onCall(async (data, context) => {
  let teamRef = db.collection("teams").doc(data.teamID);
  let ref = await db.collection("teamInvites").add(data.teamInviteData);
  let teamInviteID = ref.id;
  await teamRef.update({
    teamInvites: admin.firestore.FieldValue.arrayUnion(teamInviteID)
  });
  var eParams = {
    Destination: {
      ToAddresses: [data.email]
    },
    Message: {
      Body: {
        Html: {
          Charset: "UTF-8",
          Data:
            'You have been invited to a team. Log on to  <a class="ulink" href="https://team-synergy-bu.firebaseapp.com" target="_blank">Synergy</a> to view your invite.'
        }
      },
      Subject: {
        Data: "TechTogether[Synergy]: You have been invited to join a team!"
      }
    },
    Source: "synergy@techtogether.io"
  };
  ses.sendEmail(eParams, (err, data) => {
    if (err) console.log(err);
    else {
      console.log("===EMAIL SENT===");
      console.log(data);
    }
  });
  return;
});
