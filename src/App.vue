<template>
  <v-app>
    <router-view />
  </v-app>
</template>

<script>
import store from "@/store/index.js";
export default {
  name: "App",
  store,
  components: {},
  data() {
    return {};
  }
};
</script>
