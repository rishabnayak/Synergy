<template>
  <TeamView v-if="user.teamID" :team-i-d="user.teamID" />
  <TeamCreationForm v-else />
</template>

<script>
import TeamCreationForm from "../components/TeamCreationForm";
import TeamView from "../components/TeamView";

export default {
  name: "TeamCreation",
  components: {
    TeamCreationForm,
    TeamView
  },
  computed: {
    user() {
      return this.$store.state.user;
    }
  }
};
</script>
