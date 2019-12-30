<template>
  <v-layout align-center justify-center>
    <v-flex xs12 sm8 md4>
      <v-card class="elevation-12">
        <v-toolbar dark color="primary">
          <v-toolbar-title>Profile</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-layout row>
              <v-flex xs12>
                <v-text-field
                  v-model="name"
                  label="Name"
                  name="name"
                  readonly
                ></v-text-field>
              </v-flex>
            </v-layout>
            <v-layout row>
              <v-flex xs12>
                <v-text-field
                  v-model="email"
                  label="Email"
                  name="email"
                  readonly
                ></v-text-field>
              </v-flex>
            </v-layout>
            <v-layout row>
              <v-flex xs12>
                <v-text-field
                  v-model="originUID"
                  label="Hackathon UID"
                  :rules="originUIDRules"
                  name="uid"
                ></v-text-field>
              </v-flex>
            </v-layout>
            <v-btn color="primary" @click="updateProfile">Update</v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import store from "../store";
import { functions } from "../firebase/init";
export default {
  name: "ProfileUI",
  data() {
    return {
      name: null,
      email: null,
      originUID: null,
      originUIDRules: [val => !!val || "Origin UID Required"],
      valid: false
    };
  },
  computed: {
    user() {
      return this.$store.state.user;
    }
  },
  async mounted() {
    await store.dispatch("getUser");
    this.name = this.user.displayName;
    this.email = this.user.email;
    this.originUID = this.user.originUID;
  },
  methods: {
    async updateProfile() {
      if (this.$refs.form.validate()) {
        await functions.httpsCallable("updateOriginUID")({
          uid: this.user.uid,
          originUID: this.originUID
        });
        this.$store.dispatch("setUser").then(() => {
          this.$router.push("/team");
        });
      }
    }
  }
};
</script>
