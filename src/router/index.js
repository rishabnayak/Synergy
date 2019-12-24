import Vue from "vue";
import VueRouter from "vue-router";
import store from "@/store/index.js";
import login from "@/components/login";
import editprofile from "@/components/edit-profile";
import profile from "@/components/profile";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "login",
    component: login
  },
  {
    path: "/editprofile",
    name: "editprofile",
    component: editprofile,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: "/profile/:uname",
    name: "profile",
    component: profile
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

router.beforeEach((to, from, next) => {
  if (to.matched.some(rec => rec.meta.requiresAuth)) {
    let user = store.state.user;
    if (user) {
      next();
    } else {
      next({ name: "login" });
    }
  } else {
    next();
  }
});

export default router;
