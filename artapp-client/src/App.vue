<template>
  <div id="app">
    <Home2 />
  </div>
</template>

<script>
import Home2 from './components/Home2.vue';

document.firstElementChild.style.zoom = 'reset';

export default {
  components: {
    Home2,
  },
};
</script>

<style>
html, body {
  height: 100%;
  width: 100%;
  overflow: hidden;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;

  width: 100%;
  height: 100%;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
