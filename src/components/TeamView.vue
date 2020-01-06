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
      <v-container v-if="loaded && invites.length > 0" class="pb-4">
        <v-card class="elevation-12">
          <v-toolbar dark color="primary">
            <v-toolbar-title>Invites</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-list two-line subheader>
              <v-list-item
                v-for="(item, i) in invites"
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
                      @click.stop="deleteInvite(item.uid)"
                      >mdi-close-circle</v-icon
                    >
                  </v-btn>
                </v-list-item-action>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-container>
      <v-layout text-center wrap>
        <v-flex v-if="loaded" xs12>
          <LeaveTeamButton />
          <MemberInviteBox />
        </v-flex>
      </v-layout>
    </v-container>
  </v-layout>
</template>

<script>
import { db, functions } from "../firebase/init";

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
      loaded: false,
      members: [],
      invites: []
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
        this.teamObject.teamInvites.forEach(async element => {
          let findInvite = await db
            .collection("teamInvites")
            .doc(element.toString())
            .get();
          let findInviter = await db
            .collection("TTBUsers")
            .doc(findInvite.data().inviterID.toString())
            .get();
          let findInvitee = await db
            .collection("TTBUsers")
            .doc(findInvite.data().inviteeID.toString())
            .get();
          this.invites.push({
            uid: findInvitee.data().id,
            name:
              findInvitee.data().firstname + " " + findInvitee.data().lastname,
            subtitle:
              "Invited By: " +
              findInviter.data().firstname +
              " " +
              findInviter.data().lastname
          });
        });
      });
  },
  methods: {
    async removeFromTeam(uid) {
      await functions.httpsCallable("removeFromTeam")({
        uid: uid,
        teamID: this.user.teamID
      });
      location.reload();
    },
    async deleteInvite(uid) {
      await functions.httpsCallable("deleteInvite")({
        teamID: this.user.teamID,
        deletedUID: uid
      });
      location.reload();
    },
    async viewProfile(uid) {
      this.$router.push("/profile/" + uid);
    }
  }
};
</script>
