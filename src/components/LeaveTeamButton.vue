<template>
  <button @click="leaveTeam">Leave Team</button>
</template>

<script>
import { db, functions } from "../firebase/init";
export default {
  name: "LeaveTeamButton",
  methods: {
    leaveTeam: function() {
      // TODO: replace with a firebase function. params: None
      // - Verify that user has a team and get that team
      // - Remove that userID from team member list
      // - Remove the teamID from user record

      // ===================================
      let userID = this.$store.getters.getUser.uid;
      let userRef = db.collection("users").doc(userID);
      userRef.get().then(doc => {
        if (!doc.exists) {
          console.log(`Cannot find user id ${userID}`);
        } else {
          let teamID = doc.data().teamID;
          // remove userID from member list
          console.log("Team ID", teamID);
          if (teamID != "") {
            let teamRef = db.collection("teams").doc(teamID);
            let getTeam = teamRef.get().then(async doc => {
              if (!doc.exists) {
                console.log(`Cannot find team ${teamID}`);
              } else {
                await functions.httpsCallable("leaveTeam")({
                  teamID: teamID,
                  userID: userID
                });
              }
            });
          }
        }
      });
    }
  }
};
</script>
