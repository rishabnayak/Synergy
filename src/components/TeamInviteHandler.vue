<template>
  <div>
    <h2 v-if="loaded"> {{ team.teamName }} </h2>
    <button @click="respond(true)"> Accept </button>
    <button @click="respond(false)"> Decline </button>
  </div>
</template>

<script>
import { db } from "../firebase/init";

export default {
  name: "TeamInviteHandler",
  props: {
    teamInvite: Object,
    inviteID: String
  },
  data: function () {
    return {
      team: null,
      loaded: false
    }
  },
  methods: {
    respond: function(result) {
      if (result) {
        console.log("Accepting");
        // accept
        let currentUserID = this.teamInvite.inviteeID;
        let teamID = this.teamInvite.teamID;
        let updateUser = db.collection('users').doc(currentUserID).update({teamID: teamID});

        // update team
        let teamRef = db.collection('teams').doc(teamID);
        let updateTeam = teamRef.get()
          .then(doc => {
            let data = doc.data();
            let teamMembers = data.teamMembers;
            teamMembers.push(currentUserID);

            let teamInvites = data.teamInvites;
            teamRef.update({
              teamMembers: teamMembers,
              teamInvites: teamInvites.filter(inviteID => inviteID != this.inviteID)
            });
          });

          // delete invite
          let deleteInvite = db.collection('teamInvites').doc(this.inviteID).delete();
      } else {
        // decline
        console.log("Declining...");
        let updateInvite = db.collection('teamInvites').doc(this.inviteID).update({rejected: true})
      }
    }
  },
  created: function () {
    let teamID = this.teamInvite.teamID;
      let getTeam = db.collection("teams").doc(teamID).get()
        .then(doc => {
          console.log(doc.data());
          this.team = doc.data();
          this.loaded = true;
        });
  }
}

</script>