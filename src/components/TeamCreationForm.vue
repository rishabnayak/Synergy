<template>
  <v-layout align-center justify-center>
    <v-container style="width: 50%;">
      <v-layout text-center wrap>
        <v-flex xs12>
          <v-form v-model="valid" @submit.prevent="createTeam">
            <h2>
              Create your Team
            </h2>
            <v-text-field
              v-model="teamName"
              :rules="nameRules"
              label="Team Name"
              required
            >
            </v-text-field>
            <v-btn type="submit" :disabled="!valid"> Create </v-btn>
          </v-form>
        </v-flex>
      </v-layout>
    </v-container>
  </v-layout>
  <!--
    <h1>Create a Team</h1>
    <input v-model="teamName" type="text" />
    <button @click="createTeam">Create your Team</button>
  -->
</template>

<script>
import { functions } from "../firebase/init";
export default {
  name: "TeamCreationForm",
  data: function() {
    return {
      teamName: "",
      valid: false,
      nameRules: [v => !!v || "Name is required"]
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

      this.$store.dispatch("setUser");
    }
  }
};
</script>
