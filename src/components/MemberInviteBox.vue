<template>
  <v-form v-model="valid" @submit.prevent="inviteUser">
    <h2>Invite an user</h2>
    <v-text-field
      v-model="invitedEmail"
      :rules="emailRules"
      label="Email"
      required
    >
    </v-text-field>
    <v-btn type="submit" :disabled="!valid"> Invite </v-btn>
  </v-form>
</template>

<script>
import { db, functions } from "../firebase/init";

export default {
  name: "MemberInviteBox",
  data: function() {
    return {
      invitedEmail: "",
      valid: false,
      emailRules: [
        v =>
          /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) ||
          "E-mail must be valid"
      ]
    };
  },
  computed: {
    user() {
      return this.$store.state.user;
    }
  },
  methods: {
    inviteUser: function() {
      db.collection("TTBUsers")
        .where("email", "==", this.invitedEmail)
        .get()
        .then(results => {
          if (results.empty) {
            alert("Cannot find this email");
            return;
          }
          results.forEach(async inviteeDoc => {
            let teamInviteData = {
              inviterID: this.user.originUID,
              inviteeID: inviteeDoc.data().originUID,
              teamID: this.user.teamID
            };
            await functions.httpsCallable("createInvite")({
              teamInviteData: teamInviteData,
              teamID: this.user.teamID,
              email: this.invitedEmail
            });
          });
        });
    }
  }
};
</script>
