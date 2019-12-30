<template>
  <button @click="leaveTeam">Leave Team</button>
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
        userID: this.user.uid
      });
    }
  }
};
</script>
