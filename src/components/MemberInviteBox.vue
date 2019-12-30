<template>
  <div>
    <h1>Invite an user</h1>
    <input
      v-model="invitedEmail"
      type="text"
      placeholder="Enter their email..."
    />
    <button @click="inviteUser">Invite!</button>
  </div>
</template>

<script>
import { db, functions } from "../firebase/init";

export default {
  name: "MemberInviteBox",
  data: function() {
    return {
      invitedEmail: ""
    };
  },
  computed: {
    user() {
      return this.$store.state.user;
    }
  },
  methods: {
    inviteUser: function() {
      db.collection("users")
        .where("email", "==", this.invitedEmail)
        .get()
        .then(results => {
          if (results.empty) {
            alert("Cannot find this email");
            return;
          }

          results.forEach(async inviteeDoc => {
            let teamInviteData = {
              inviterID: this.user.uid,
              inviteeID: inviteeDoc.data().uid,
              teamID: this.user.teamID
            };
            await functions.httpsCallable("createInvite")({
              teamInviteData: teamInviteData,
              teamID: this.user.teamID
            });
          });
        });
    }
  }
};
</script>
