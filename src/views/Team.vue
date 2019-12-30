<template>
  <div>
    <TeamCreationForm></TeamCreationForm>
    <LeaveTeamButton></LeaveTeamButton>
    <MemberInviteBox></MemberInviteBox>
    <TeamInviteHandler v-if="loaded" :teamInvite="teamInvite" inviteID="0IGRSzKSvP7m91CM9edd"> </TeamInviteHandler>
    </div>
  </div>
</template>

<script>
import { db } from "../firebase/init";

import TeamCreationForm from "../components/TeamCreationForm";
import LeaveTeamButton from "../components/LeaveTeamButton";
import MemberInviteBox from "../components/MemberInviteBox";
import TeamInviteHandler from "../components/TeamInviteHandler";

export default {
  name: "TeamCreation",
  components: {
    TeamCreationForm,
    LeaveTeamButton,
    MemberInviteBox,
    TeamInviteHandler
  },
  data: function () {
    return {
      teamInvite: null,
      loaded: false
    };
  },
  beforeCreate: function () {
    let teamInviteRef = db.collection('teamInvites').doc("0IGRSzKSvP7m91CM9edd");
    let getTeamInvite = teamInviteRef.get()
      .then(doc => {
        console.log(doc.data());
        this.teamInvite = doc.data();
        this.loaded = true;
      })
  }
};
</script>
