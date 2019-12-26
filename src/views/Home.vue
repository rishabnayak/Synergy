<template>
  <LandingPage />
</template>

<script>
import LandingPage from "../components/LandingPage";
export default {
  name: "Home",
  components: {
    LandingPage
  },
  computed: {
    user() {
      return this.$store.state.user;
    }
  }
};
</script>
