<template>
  <main class="container">
    <div class="jumbotron">
      <h1 align="center">{{ displayname }}</h1>
      <h4 class="section-head">Bio</h4>
      <p class="content">{{ bio }}</p>
      <h4 class="section-head">City</h4>
      <p class="content">{{ city }}</p>
      <h4 class="section-head">State</h4>
      <p class="content">{{ stt }}</p>
      <h4 class="section-head">Country</h4>
      <p class="content">{{ country }}</p>
      <h4 class="section-head">Phone Number</h4>
      <p class="content">{{ number }}</p>
      <h4 class="section-head">Current Affiliation</h4>
      <p class="content">{{ affiliation }}</p>
      <router-link to="/editprofile">
        <button
          v-if="userCheck"
          class="btn btn-primary btn-lg btn-block col-md-3"
        >
          Update
        </button>
      </router-link>
    </div>
  </main>
</template>

<script>
import db from "@/firebase/init.js";
export default {
  name: "profile",
  computed: {
    user() {
      return this.$store.state.user;
    }
  },
  data() {
    return {
      uname: this.$route.params.uname,
      displayname: null,
      bio: null,
      city: null,
      stt: null,
      country: null,
      number: null,
      affiliation: null,
      userCheck: null
    };
  },
  async created() {
    let finduser = await db
      .collection("users")
      .where("uname", "==", this.uname)
      .get();
    this.bio = finduser.docs[0].data().bio;
    this.city = finduser.docs[0].data().city;
    this.stt = finduser.docs[0].data().stt;
    this.country = finduser.docs[0].data().country;
    this.number = finduser.docs[0].data().number;
    this.affiliation = finduser.docs[0].data().affiliation;
    this.displayname = finduser.docs[0].data().displayName;
    if (this.$route.params.uname == this.user.uname) {
      this.userCheck = true;
    } else {
      this.userCheck = false;
    }
  }
};
</script>

<style>
h1 {
  color: #444;
}

.section-head {
  padding-left: 8px;
}

.content {
  padding-left: 12px;
}
</style>
