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
  },
  beforeMount() {
    if (this.user) {
      this.$router.push("/team");
    }
  }
};
</script>
