# Synergy

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
firebase.functions().httpsCallable("name-of-function")(<input_data>).then(data => {callback})
```
