<template>
  <div>
    <h1>{{ user.name }}</h1>
    <p>{{ user.age }}</p>
  </div>
</template>

<script>
export default {
  props: {
    user: Object
  }
};
</script>
