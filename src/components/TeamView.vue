<template>
  <v-layout justify-center>
    <v-container>
      <v-layout text-center wrap>
        <v-flex v-if="loaded" xs12>
          <h2>{{ teamObject.teamName }}</h2>
          <p>Insert members info here</p>
          <LeaveTeamButton />
          <MemberInviteBox />
        </v-flex>
      </v-layout>
    </v-container>
  </v-layout>
</template>

<script>
import { db } from "../firebase/init";

import MemberInviteBox from "./MemberInviteBox";
import LeaveTeamButton from "./LeaveTeamButton";

export default {
  name: "TeamView",
  components: {
    MemberInviteBox,
    LeaveTeamButton
  },
  props: {
    teamID: {
      type: String,
      required: true
    }
  },
  data: function() {
    return {
      teamObject: null,
      loaded: false
    };
  },
  created: function() {
    let teamID = this.teamID;
    db.collection("teams")
      .doc(teamID)
      .get()
      .then(doc => {
        this.teamObject = doc.data();
        this.loaded = true;
      });
  }
};
</script>
