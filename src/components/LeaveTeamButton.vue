<template>
  <v-btn color="error" @click="leaveTeam">Leave Team</v-btn>
</template>

<script>
import { functions } from "../firebase/init";
export default {
  name: "LeaveTeamButton",
  computed: {
    user() {
      return this.$store.state.user;
    }
  },
  methods: {
    async leaveTeam() {
      await functions.httpsCallable("leaveTeam")({
        teamID: this.user.teamID,
        userID: this.user.uid,
        userOriginUID: this.user.originUID
      });
      this.$store.dispatch("setUser").then(() => {
        location.reload();
      });
    }
  }
};
</script>
