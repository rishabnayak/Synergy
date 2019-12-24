<template>
  <div id="app">
    <navigation />
    <router-view />
  </div>
</template>

<script>
import navigation from "@/components/navigation.vue";
import store from "@/store/index.js";
export default {
  name: "App",
  store,
  components: {
    navigation
  },
  data() {
    return {};
  }
};
</script>

<style></style>
