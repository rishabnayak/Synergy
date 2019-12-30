import firebase from "firebase/app";
const firebaseui = require("firebaseui");
import "firebase/auth";
import "firebase/firestore";
import "firebase/functions";

const config = {
  apiKey: "AIzaSyAKyPPIPB-oTWbSHnP90w28ICM8txxxms0",
  authDomain: "team-synergy-bu.firebaseapp.com",
  databaseURL: "https://team-synergy-bu.firebaseio.com",
  projectId: "team-synergy-bu",
  storageBucket: "team-synergy-bu.appspot.com",
  messagingSenderId: "499195778927",
  appId: "1:499195778927:web:7b2035c6bb59fcd2443a9a",
  measurementId: "G-CP7L6RZ1NT"
};

const app = firebase.initializeApp(config);
const auth = firebase.auth();
const db = app.firestore();
const functions = firebase.functions();

const authUI = new firebaseui.auth.AuthUI(auth);

const authUIConfig = {
  signInSuccessUrl: "/",
  signInOptions: [
    {
      provider: firebase.auth.EmailAuthProvider.PROVIDER_ID
    },
    {
      provider: firebase.auth.GoogleAuthProvider.PROVIDER_ID,
      customParameters: {
        prompt: "select_account"
      }
    }
  ]
};

export default app;
export { auth, db, authUI, authUIConfig, functions };
