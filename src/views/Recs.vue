<template>
  <div>
    <h1>Hello World!!!</h1>
    <p>{{ user.uid }}</p>
    <UserProfile
      v-for="profile in recProfiles"
      :key="profile.id"
      :user="profile"
    ></UserProfile>
  </div>
</template>

<script>
import UserProfile from "../components/UserProfile";
export default {
  name: "Recs",
  components: {
    UserProfile
  },
  data: function() {
    // Recs dummy data -> should be replaced with real data from database
    return {
      recProfiles: [
        {
          id: 1,
          name: "User1",
          age: 17
        },
        {
          id: 2,
          name: "User2",
          age: 18
        }
      ]
    };
  },
  computed: {
    // get authenticated user from firebase authentication
    user: function() {
      return this.$store.getters.getUser;
    }
  }
};
</script>
