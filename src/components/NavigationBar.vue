<template>
  <div>
    <v-toolbar>
      <v-toolbar-title>Synergy</v-toolbar-title>
      <v-spacer></v-spacer>
      <!-- <v-toolbar-items class="hidden-sm-and-down"> -->
      <v-toolbar-items>
        <v-btn text @click="home()">Home</v-btn>
        <v-btn v-if="user" text @click="team()">Team</v-btn>
        <v-btn v-if="user" text @click="recommendations()"
          >Recommendations</v-btn
        >
        <v-btn v-if="user" text @click="profile()">My Profile</v-btn>
        <v-btn icon>
          <v-icon v-if="user" @click="signOut()">mdi-export-variant</v-icon>
          <v-icon v-else @click="signIn()">mdi-arrow-right</v-icon>
        </v-btn>
      </v-toolbar-items>
      <!-- <v-menu class="hidden-md-and-up">
        <v-app-bar-nav-icon></v-app-bar-nav-icon>
        <v-list>
          <v-list-tile>
            <v-list-tile-content>
              <v-list-tile-title @click="home()">Home</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile v-if="user">
            <v-list-tile-content>
              <v-list-tile-title @click="team()">Team</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile v-if="user">
            <v-list-tile-content>
              <v-list-tile-title @click="profile()"
                >My Profile</v-list-tile-title
              >
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
        <v-btn icon>
          <v-icon v-if="user" @click="signOut()">mdi-export-variant</v-icon>
          <v-icon v-else @click="signIn()">mdi-arrow-right</v-icon>
        </v-btn>
      </v-menu>-->
    </v-toolbar>
  </div>
</template>

<script>
export default {
  name: "NavigationBar",
  data() {
    return {};
  },
  computed: {
    user() {
      return this.$store.state.user;
    }
  },
  methods: {
    async signOut() {
      await this.$store.dispatch("logOut");
      this.$router.push("/");
    },
    signIn() {
      this.$router.push("/login");
    },
    home() {
      this.$router.push("/");
    },
    profile() {
      this.$router.push("/profile");
    },
    team() {
      this.$router.push("/team");
    },
    recommendations() {
      this.$router.push("/recommendations");
    }
  }
};
</script>
