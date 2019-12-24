import Vue from "vue";
import App from "./App";
import router from "@/router/index.js";
import store from "@/store/index.js";
import firebase from "firebase/app";
import "firebaseui/dist/firebaseui.css";
import vuetify from "./plugins/vuetify";

Vue.config.productionTip = false;

var app = null;
firebase.auth().onAuthStateChanged(async () => {
  if (!app) {
    await store.dispatch("setUser");
    new Vue({
      router,
      store,
      vuetify,
      render: h => h(App)
    }).$mount("#app");
  }
});
export const db = firebase.firestore();
