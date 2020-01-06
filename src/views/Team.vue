<template>
  <TeamView v-if="user.teamID && !teamID" :team-i-d="user.teamID" />
  <OtherTeamView v-else-if="teamID" :team-i-d="teamID" />
  <TeamCreationForm v-else />
</template>

<script>
import TeamCreationForm from "../components/TeamCreationForm";
import TeamView from "../components/TeamView";
import OtherTeamView from "../components/OtherTeamView";

export default {
  name: "TeamCreation",
  components: {
    TeamCreationForm,
    TeamView,
    OtherTeamView
  },
  data() {
    return {
      teamID: this.$route.params.teamID
    };
  },
  computed: {
    user() {
      return this.$store.state.user;
    }
  }
};
</script>
