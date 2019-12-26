<template>
  <div :style="{ background: bg, width: bgWidth, height: bgHeight }">
    <v-container fill-height text-center>
      <v-layout align-center wrap>
        <v-row>
          <v-container>
            <v-btn x-large text color="white" @click="signIn()">Login</v-btn>
          </v-container>
        </v-row>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      bg:
        "linear-gradient(180deg, #3DB3EE 13.54%, rgba(255, 255, 255, 0) 99.99%, rgba(64, 159, 227, 0.982353) 100%), #0AA0EA",
      bgWidth: "100%",
      bgHeight: "100%"
    };
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
    }
  }
};
</script>
