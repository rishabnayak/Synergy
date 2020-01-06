<template>
  <div>
    <h2 v-if="loaded">{{ team.teamName }}</h2>
    <button @click="respond(true)">Accept</button>
    <button @click="respond(false)">Decline</button>
  </div>
</template>

<script>
import { db, functions } from "../firebase/init";

export default {
  name: "TeamInviteHandler",
  props: {
    teamInvite: {
      type: Object,
      required: true
    },
    inviteID: {
      type: String,
      required: true
    }
  },
  data: function() {
    return {
      team: null,
      loaded: false
    };
  },
  created: function() {
    let teamID = this.teamInvite.teamID;
    db.collection("teams")
      .doc(teamID)
      .get()
      .then(doc => {
        this.team = doc.data();
        this.loaded = true;
      });
  },
  methods: {
    async respond(result) {
      if (result) {
        // accept
        await functions.httpsCallable("acceptInvite")({
          userID: this.user.uid,
          inviteeID: this.teamInvite.inviteeID,
          teamID: this.teamInvite.teamID,
          inviteID: this.inviteID
        });
      } else {
        // decline
        await functions.httpsCallable("rejectInvite")({
          inviteID: this.inviteID
        });
      }
    }
  }
};
</script>
