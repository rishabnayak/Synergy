<template>
  <div v-bind:style="{ background: bg, width: bgWidth, height: bgHeight }">
    <v-layout text-center wrap>
      <v-row>
        <v-col>
          <v-card class="mx-auto" color="white" width="400px">
            <v-card-title class="justify-center">
              <h3>Log in</h3>
            </v-card-title>
            <v-card-text>
              <div id="firebaseui-auth-container"></div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-layout>
  </div>
</template>

<script>
import { authUI, authUIConfig } from "../firebase/init";
export default {
  name: "authUI",
  computed: {
    user() {
      return this.$store.state.user;
    }
  },
  mounted() {
    authUI.start("#firebaseui-auth-container", authUIConfig);
  },
  data() {
    return {
      bg:
        "linear-gradient(180deg, #3DB3EE 13.54%, rgba(255, 255, 255, 0) 99.99%, rgba(64, 159, 227, 0.982353) 100%), #0AA0EA",
      bgWidth: "100%",
      bgHeight: "100%"
    };
  }
};
</script>
