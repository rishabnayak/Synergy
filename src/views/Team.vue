<template>
  <div>
    <TeamCreationForm></TeamCreationForm>
    <LeaveTeamButton></LeaveTeamButton>
    <MemberInviteBox></MemberInviteBox>
  </div>
</template>

<script>
import TeamCreationForm from "../components/TeamCreationForm";
import LeaveTeamButton from "../components/LeaveTeamButton";
import MemberInviteBox from "../components/MemberInviteBox";
export default {
  name: "TeamCreation",
  components: {
    TeamCreationForm,
    LeaveTeamButton,
    MemberInviteBox
  }
};
</script>
