<template>
  <div>
    <h1>Create a Team</h1>
    <input v-model="teamName" type="text" />
    <button @click="createTeam">Create your Team</button>
  </div>
</template>

<script>
import { functions } from "../firebase/init";
export default {
  name: "TeamCreationForm",
  data: function() {
    return {
      teamName: ""
    };
  },
  computed: {
    user() {
      return this.$store.state.user;
    }
  },
  methods: {
    async createTeam() {
      let teamData = {
        teamName: this.teamName,
        teamMembers: [this.user.uid],
        teamInvites: []
      };
      await functions.httpsCallable("createTeam")({
        teamData: teamData,
        userID: this.user.uid
      });
    }
  }
};
</script>
