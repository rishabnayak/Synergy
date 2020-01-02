<template>
  <v-layout align-center justify-center>
    <v-flex xs12 sm8 md4>
      <v-card class="elevation-12">
        <v-toolbar dark color="primary">
          <v-toolbar-title>Recommendations</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <v-list>
            <v-list-item-group v-model="recProfile" color="primary">
              <v-list-item
                v-for="(item, i) in recProfiles"
                :key="i"
                :to="{ name: 'profile', params: { uid: item.uid } }"
              >
                <v-list-item-content>
                  <v-list-item-title v-text="item.name"></v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: "Recs",
  data() {
    return {
      recProfile: null,
      recProfiles: [
        {
          uid: 1,
          name: "John"
        },
        {
          uid: 2,
          name: "Jack"
        }
      ]
    };
  },
  computed: {
    user() {
      return this.$store.state.user;
    }
  }
};
</script>
