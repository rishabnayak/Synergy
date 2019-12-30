<template>
  <div>
    <h1>Create a Team</h1>
    <input v-model="teamName" type="text" />
    <button @click="createTeam">Create your Team</button>
  </div>
</template>

<script>
import { db, functions } from "../firebase/init";
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
        let userID = this.$store.getters.getUser.uid;
        let userRef = db.collection("users").doc(userID);
        userRef.get().then(async doc => {
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
              await functions.httpsCallable("createTeam")({
                teamData: teamData,
                userID: userID
              });
            }
          }
        });
      }
    }
  }
};
</script>
