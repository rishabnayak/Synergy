<template>
  <div class="container">
    <h4 class="mb-3">User Profile</h4>
    <form v-if="user">
      <div class="row">
        <div class="col-md-auto mb-3">
          <label for="username">Username</label>
          <div class="input-group">
            <div class="input-group-prepend">
              <span class="input-group-text">@</span>
            </div>
            <input
              type="text"
              class="form-control"
              id="username"
              v-model="uname"
              @input="checkAvailability()"
            />
            <div class="availability">
              <i v-if="unameempty" class="material-icons red">close</i>
              <i v-else-if="available" class="material-icons green">check</i>
              <i v-else-if="unavailable" class="material-icons red">close</i>
            </div>
          </div>
          <p v-if="unameempty" class="red availability">Enter a Username</p>
          <p v-else-if="available" class="green availability">
            Username available!
          </p>
          <p v-else-if="unavailable" class="red availability">
            Username unavailable!
          </p>
        </div>
      </div>
      <div class="mb-3">
        <label for="bio">Short Introduction</label>
        <textarea
          class="form-control"
          rows="5"
          id="bio"
          v-model="bio"
        ></textarea>
      </div>
      <div class="row">
        <div class="col-md-4 mb-3">
          <label for="city">City</label>
          <input type="text" class="form-control" id="city" v-model="city" />
        </div>
        <div class="col-md-4 mb-3">
          <label for="state">State</label>
          <input type="text" class="form-control" id="state" v-model="stt" />
        </div>
        <div class="col-md-4 mb-3">
          <label for="country">Country</label>
          <input
            type="text"
            class="form-control"
            id="country"
            v-model="country"
          />
        </div>
      </div>
      <div class="row">
        <div class="col-md-4 mb-3">
          <label for="number">Phone Number</label>
          <input
            type="text"
            class="form-control"
            id="number"
            v-model="number"
          />
        </div>
        <div class="col-md-4 mb-3">
          <label for="affiliation">Current Affiliation</label>
          <input
            type="text"
            class="form-control"
            id="affiliation"
            placeholder="University/College/Company"
            v-model="affiliation"
          />
        </div>
      </div>
      <hr class="mb-4" />
    </form>
    <button
      :disabled="unavailable || unameempty"
      class="btn btn-primary btn-lg btn-block col-md-3"
      type="submit"
      @click="updateProfile()"
    >
      Update
    </button>
  </div>
</template>

<script>
import db from "@/firebase/init.js";
export default {
  name: "editprofile",
  computed: {
    user() {
      return this.$store.state.user;
    }
  },
  methods: {
    async updateProfile() {
      const ref = db.collection("users").doc(this.user.uid);
      await ref.update({
        bio: this.bio,
        city: this.city,
        stt: this.stt,
        country: this.country,
        number: this.number,
        affiliation: this.affiliation,
        uname: this.uname
      });
      this.$router.push({ name: "profile", params: { uname: this.uname } });
    },
    async checkAvailability() {
      let checkname = await db
        .collection("users")
        .where("uname", "==", this.uname)
        .get();
      if (this.uname == null || this.uname == "") {
        this.unameempty = true;
      } else if (
        checkname.empty ||
        checkname.docs[0].data().uname == this.user.uname
      ) {
        this.available = true;
        this.unameempty = false;
        this.unavailable = false;
      } else {
        this.available = false;
        this.unameempty = false;
        this.unavailable = true;
      }
    }
  },
  data() {
    return {
      bio: null,
      city: null,
      stt: null,
      country: null,
      number: null,
      affiliation: null,
      uname: null,
      available: null,
      unavailable: null,
      unameempty: null
    };
  },
  mounted: function() {
    this.checkAvailability();
  },
  async created() {
    this.bio = this.user.bio;
    this.city = this.user.city;
    this.stt = this.user.stt;
    this.country = this.user.country;
    this.number = this.user.number;
    this.affiliation = this.user.affiliation;
    this.uname = this.user.uname;
  }
};
</script>

<style>
.container {
  padding-top: 40px;
  padding-bottom: 40px;
}
.material-icons.green {
  color: green;
}

.material-icons.red {
  color: red;
}

.availability {
  padding-top: 6px;
  padding-left: 3px;
}

.green {
  color: green;
}

.red {
  color: red;
}
</style>
