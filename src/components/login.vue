<template>
  <div id="firebaseui-auth-container"></div>
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
  }
};
</script>
