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
                <v-select
                  v-if="role == null"
                  v-model="role"
                  :items="roles"
                  label="User Role"
                  :rules="roleRules"
                ></v-select>
                <v-text-field
                  v-else
                  v-model="role"
                  label="User Role"
                  :disabled="true"
                ></v-text-field>
              </v-flex>
            </v-layout>
            <v-layout v-if="role == 'Admin' || role == 'Inmate'" row>
              <v-flex xs12>
                <v-combobox
                  v-if="location == null"
                  v-model="location"
                  :items="prisons"
                  :rules="locationRules"
                  label="Prison Location"
                />
                <v-text-field
                  v-else
                  v-model="location"
                  label="Prison Location"
                  :disabled="true"
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
import { db } from "../firebase/init.js";
import store from "../store";
export default {
  name: "ProfileUI",
  data() {
    return {
      name: null,
      role: null,
      email: null,
      calEvents: null,
      contacts: null,
      valid: false,
      location: null,
      prisons: [],
      roleRules: [val => !!val || "Role Required"],
      locationRules: [val => !!val || "Location Required"],
      roles: ["Friends and Family", "Inmate"]
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
    this.role = this.user.role;
    this.email = this.user.email;
    this.calEvents = this.user.calEvents;
    this.contacts = this.user.contacts;
    this.location = this.user.location;
    this.getPrison();
  },
  methods: {
    async updateProfile() {
      if (this.$refs.form.validate()) {
        const ref = db.collection("users").doc(this.user.uid);
        if (this.location) {
          await ref
            .update({
              role: this.role,
              location: this.location
            })
            .then(() => {
              this.$store.dispatch("setUser").then(() => {
                this.$router.push("/user");
              });
            });
        } else {
          await ref
            .update({
              role: this.role
            })
            .then(() => {
              this.$store.dispatch("setUser").then(() => {
                this.$router.push("/user");
              });
            });
        }
      }
    },
    async getPrison() {
      let snapshot = await db.collection("users").get();
      snapshot.forEach(doc => {
        if (doc.data().location) {
          this.prisons.push(doc.data().location);
        }
      });
    }
  }
};
</script>
