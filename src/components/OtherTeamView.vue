<template>
  <v-layout justify-center>
    <v-container>
      <v-layout text-center wrap>
        <v-flex v-if="loaded" xs12>
          <h2>{{ teamObject.teamName }}</h2>
          <p>{{ teamObject.teamDescription }}</p>
        </v-flex>
      </v-layout>
      <v-container v-if="loaded && members.length > 0" class="pb-4">
        <v-card class="elevation-12">
          <v-toolbar dark color="primary">
            <v-toolbar-title>Team Members</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-list two-line subheader>
              <v-list-item
                v-for="(item, i) in members"
                :key="i"
                @click="viewProfile(item.uid)"
              >
                <v-list-item-content>
                  <v-list-item-title v-text="item.name"></v-list-item-title>
                  <v-list-item-subtitle
                    v-text="item.subtitle"
                  ></v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-action>
                  <v-btn icon>
                    <v-icon
                      color="grey lighten-1"
                      @click.stop="removeFromTeam(item.uid)"
                      >mdi-close-circle</v-icon
                    >
                  </v-btn>
                </v-list-item-action>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-container>
    </v-container>
  </v-layout>
</template>

<script>
import { db } from "../firebase/init";

export default {
  name: "OtherTeamView",
  props: {
    teamID: {
      type: String,
      required: true
    }
  },
  data: function() {
    return {
      teamObject: null,
      loaded: false,
      members: []
    };
  },
  computed: {
    user() {
      return this.$store.state.user;
    }
  },
  created: function() {
    let teamID = this.teamID;
    db.collection("teams")
      .doc(teamID)
      .get()
      .then(doc => {
        this.teamObject = doc.data();
        this.loaded = true;
        this.teamObject.teamMembers.forEach(async element => {
          if (element != this.user.originUID) {
            let finduser = await db
              .collection("TTBUsers")
              .doc(element.toString())
              .get();
            this.members.push({
              uid: element,
              name: finduser.data().firstname + " " + finduser.data().lastname,
              subtitle:
                "Focus: " +
                finduser.data().focus +
                ", Interests: " +
                finduser.data().interests
            });
          }
        });
      });
  },
  methods: {
    async viewProfile(uid) {
      this.$router.push("/profile/" + uid);
    }
  }
};
</script>
