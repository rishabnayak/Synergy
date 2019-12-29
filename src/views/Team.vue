<template>
  <div>
    <TeamCreationForm></TeamCreationForm>
    <LeaveTeamButton></LeaveTeamButton>
  </div>
</template>

<script>
import TeamCreationForm from "../components/TeamCreationForm";
import LeaveTeamButton from "../components/LeaveTeamButton";
export default {
  name: "TeamCreation",
  components: {
    TeamCreationForm,
    LeaveTeamButton
  }
};
</script>
