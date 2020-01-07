<template>
  <v-layout align-center justify-center>
    <v-flex xs8 sm8 md8>
      <v-card class="elevation-12">
        <v-toolbar dark color="primary">
          <v-toolbar-title>Invites</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <v-list two-line subheader>
            <v-list-item
              v-for="(item, i) in invites"
              :key="i"
              @click="viewTeam(item.uid)"
            >
              <v-list-item-content>
                <v-list-item-title v-text="item.name"></v-list-item-title>
                <v-list-item-subtitle
                  v-text="item.subtitle"
                ></v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action v-if="!teamExists">
                <v-btn icon>
                  <v-icon color="grey lighten-1" @click.stop="accept(i)"
                    >mdi-check-circle</v-icon
                  >
                </v-btn>
              </v-list-item-action>
              <v-list-item-action v-else>
                <v-content
                  >Leave your current team to accept another invite.</v-content
                >
              </v-list-item-action>
              <v-list-item-action>
                <v-btn icon>
                  <v-icon color="grey lighten-1" @click.stop="decline(i)"
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
  name: "Invites",
  data() {
    return {
      invites: [],
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
    let findInvited = await db
      .collection("teamInvites")
      .where("inviteeID", "==", this.user.originUID)
      .get();
    findInvited.docs.forEach(async element => {
      let findTeam = await db
        .collection("teams")
        .doc(element.data().teamID)
        .get();
      let findInviter = await db
        .collection("TTBUsers")
        .doc(element.data().inviterID.toString())
        .get();
      if (!element.data().rejected) {
        this.invites.push({
          uid: element.data().teamID,
          name: findTeam.data().teamName,
          inviteID: element.id,
          subtitle:
            "Invited By: " +
            findInviter.data().firstname +
            " " +
            findInviter.data().lastname
        });
      }
    });
  },
  methods: {
    async accept(i) {
      await functions.httpsCallable("acceptInvite")({
        userID: this.user.uid,
        inviteeID: this.user.originUID,
        teamID: this.invites[i].uid,
        inviteID: this.invites[i].inviteID
      });
      location.reload();
    },
    async decline(i) {
      await functions.httpsCallable("rejectInvite")({
        inviteID: this.invites[i].inviteID
      });
      location.reload();
    },
    async viewTeam(uid) {
      this.$router.push("/team/" + uid);
    }
  }
};
</script>
