import Vue from "vue";
import VueRouter from "vue-router";
import store from "@/store/index.js";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: () => import("@/views/Home.vue")
  },
  {
    path: "/profile",
    name: "profile",
    component: () => import("@/views/Profile.vue"),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: "/profile/:uid",
    name: "otherprofile",
    component: () => import("@/views/Profile.vue"),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/Login.vue"),
    meta: {
      requiresAuth: false
    }
  },
  {
    path: "/recommendations",
    name: "recommendations",
    component: () => import("@/views/Recs.vue"),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: "/invites",
    name: "invites",
    component: () => import("@/views/Invites.vue"),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: "/team",
    name: "team",
    component: () => import("@/views/Team.vue"),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: "/team/:teamID",
    name: "otherteam",
    component: () => import("@/views/Team.vue"),
    meta: {
      requiresAuth: true
    }
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
      if (to.name == "profile") {
        next();
      } else {
        if (user.originUID) {
          next();
        } else {
          next({
            name: "profile"
          });
        }
      }
    } else {
      next({ name: "login" });
    }
  } else {
    next();
  }
});

export default router;
