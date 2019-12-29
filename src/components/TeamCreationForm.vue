<template>
  <div>
    <h1>Create a Team</h1>
    <input v-model="teamName" type="text" />
    <button @click="createTeam">Create your Team</button>
  </div>
</template>

<script>
import { db } from "../firebase/init";
export default {
  name: "TeamCreationForm",
  data: function() {
    return {
      teamName: ""
    };
  },
  methods: {
    createTeam: function() {
      let teamName = this.teamName;
      if (teamName == "") {
        // throwing error
        alert("You should enter a name!");
      } else {
        // TODO: replace with a firebase function
        // - Check that the user does not have a team
        // - Create a Team
        // - Link user to that team via teamID

        // =======================================
        let userID = this.$store.getters.getUser.uid;
        let userRef = db.collection("users").doc(userID);
        let getUser = userRef.get().then(doc => {
          if (!doc.exists) {
            console.log(`Cannot find user id ${userID}!!`);
          } else {
            console.log("Found following user data", doc.data());
            console.log(doc.data().teamID);

            if (!doc.data().teamID) {
              console.log("Creating teams...", teamName);
              let teamData = {
                teamName: teamName,
                teamMembers: [userID],
                teamInvites: []
              };

              let addTeam = db
                .collection("teams")
                .add(teamData)
                .then(ref => {
                  let teamID = ref.id;
                  let updateUserTeamID = userRef.update({ teamID: teamID });
                  console.log(`Updating user ${userID} with teamID ${teamID}`);
                });
            }
          }
        });
        // ======================================== END OF FIREBASE FUNCTION
      }
    }
  }
};
</script>
