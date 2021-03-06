# Synergy
[![Actions Status](https://github.com/rishabnayak/synergy/workflows/Build/badge.svg)](https://github.com/rishabnayak/synergy/actions)
[![License](http://img.shields.io/badge/License-MIT-brightgreen.svg)](./LICENSE)

Synergy is a Team Building Platform For Hackathons. Built with Vue.js, Firebase and Python.

## Project setup

```bash
npm install
```

### Compiles and hot-reloads for development

```bash
npm run serve
```

### Compiles and minifies for production

```bash
npm run build
```

### Lints and fixes files

```bash
npm run lint
```

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).

## Calling Firebase functions

With an authenticated @firebase/app object,

```javascript
firebase.functions().httpsCallable("name-of-function")(input_data).then(data => {...})
```

For more info on the types of functions, visit the official [Firebase Documentation](https://firebase.google.com/docs/functions).

## Making a Firestore transaction

With an authenticated @firebase/app object,

```javascript
import { db } from "../firebase/init";
db.collection("name-of-collection").doc("doc-identifier").action().then(data => {...})
```

For more info on actions that can be performed, visit the official [Firebase Documentation](https://firebase.google.com/docs/firestore).

## Deployment

After running the buildscript, run the following command after installing the [Firebase CLI](https://firebase.google.com/docs/cli) to deploy the website as well as the functions.

```bash
firebase deploy
```

To deploy only functions,

```bash
firebase deploy --only functions
```

## Update recommendations

To run the server locally, fill in input database credentials in RecsUpdate/dadtabase.ini and run

```bash
cd RecsUpdate
export FLASK_APP=main.py
python -m flask run
```

To make an update run, send a GET http server to /update.

To deploy,

```bash
cd RecsUpdate
gcloud app deploy
```

## Contributing

To contribute to Synergy, view our [contribution guide](https://github.com/rishabnayak/Synergy/blob/master/CONTRIBUTING.md).
