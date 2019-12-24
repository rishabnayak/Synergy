import Vue from "vue";
import App from "./App";
import router from "@/router/index.js";
import store from "@/store/index.js";
import firebase from "firebase";

Vue.config.productionTip = false;

var app = null;
firebase.auth().onAuthStateChanged(async () => {
  if (!app) {
    await store.dispatch("setUser");
    new Vue({
      el: "#app",
      router,
      components: { App },
      template: "<App/>"
    });
  }
});
