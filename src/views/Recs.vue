<template>
  <v-layout align-center justify-center>
    <v-flex xs8 sm8 md8>
      <v-card class="elevation-12">
        <v-toolbar dark color="primary">
          <v-toolbar-title>Recommendations</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <v-list two-line subheader>
            <v-list-item
              v-for="(item, i) in recProfiles"
              :key="i"
              @click="viewProfile(item.uid)"
            >
              <v-list-item-content>
                <v-list-item-title v-text="item.name"></v-list-item-title>
                <v-list-item-subtitle
                  v-text="item.subtitle"
                ></v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action v-if="teamExists && !item.invited">
                <v-btn icon>
                  <v-icon
                    color="grey lighten-1"
                    @click.stop="inviteUser(item.uid, item.email)"
                    >mdi-check-circle</v-icon
                  >
                </v-btn>
              </v-list-item-action>
              <v-list-item-action v-if="teamExists && item.invited">
                <v-content>Invite Sent!</v-content>
              </v-list-item-action>
              <v-list-item-action v-if="teamExists && !item.invited">
                <v-btn icon>
                  <v-icon
                    color="grey lighten-1"
                    @click.stop="declineRecommendation(item.uid)"
                    >mdi-close-circle</v-icon
                  >
                </v-btn>
              </v-list-item-action>
              <v-list-item-action v-else>
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
    </v-flex>
  </v-layout>
</template>

<script>
import { db, functions } from "../firebase/init";
export default {
  name: "Recs",
  data() {
    return {
      recommendations: [],
      recProfiles: [],
      teamExists: null
    };
  },
  computed: {
    user() {
      return this.$store.state.user;
    }
  },
  async mounted() {
    this.teamExists = this.user.teamID;
    let finduser = await db
      .collection("TTBUsers")
      .doc(this.user.originUID)
      .get();
    finduser.data().recommendations.forEach(element => {
      this.recommendations.push(element.replace(/'/g, ""));
    });
    this.recommendations.forEach(async element => {
      let finduser = await db
        .collection("TTBUsers")
        .doc(element.toString())
        .get();
      let findInvited = await db
        .collection("teamInvites")
        .where("inviteeID", "==", element)
        .where("teamID", "==", this.user.teamID)
        .get();
      if (!findInvited.empty) {
        this.recProfiles.push({
          uid: element,
          name: finduser.data().firstname + " " + finduser.data().lastname,
          email: finduser.data().email,
          subtitle:
            "Focus: " +
            finduser.data().focus +
            ", Interests: " +
            finduser.data().interests,
          invited: true
        });
      } else {
        this.recProfiles.push({
          uid: element,
          name: finduser.data().firstname + " " + finduser.data().lastname,
          email: finduser.data().email,
          subtitle:
            "Focus: " +
            finduser.data().focus +
            ", Interests: " +
            finduser.data().interests,
          invited: false
        });
      }
    });
  },
  methods: {
    async inviteUser(uid, email) {
      let teamInviteData = {
        inviterID: this.user.originUID,
        inviteeID: uid,
        teamID: this.user.teamID
      };

      await functions.httpsCallable("createInvite")({
        teamInviteData: teamInviteData,
        teamID: this.user.teamID,
        email: email
      });
      location.reload();
    },
    async declineRecommendation(uid) {
      await functions.httpsCallable("declineRecommendation")({
        uid: this.user.originUID,
        declinedUID: uid
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
