<template>
  <LandingPage />
</template>

<script>
import LandingPage from "../components/LandingPage";
export default {
  name: "Home",
  computed: {
    user() {
      return this.$store.state.user;
    }
  },
  components: {
    LandingPage
  }
};
</script>
