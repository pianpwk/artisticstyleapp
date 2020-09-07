<template>
  <div id="loading-screen">
    <vue-ellipse-progress
      id="progress-circle"
      :progress=progress
      color="ivory"
      empty-color="black"
      :size="240"
      :thickness="6"
      :empty-thickness="3"
      animation="bounce 700 1000"
      fontSize="1.5rem"
      font-color="white"
      dot="7"
    >
      <span slot="legend-caption" id="loading-legend"> {{ loadingText }} </span>
    </vue-ellipse-progress>
  </div>
</template>

<script>
export default {
  name: "LoadingScreen",
  props: ["progress","loadingText"]
};
</script>

<style lang="scss" scoped>
#progress-circle {
  width: 240px;
  height: 240px;
  left: 50%;
  top: 50%;
  left: calc(50% - 120px);
  top: calc(50% - 120px);
  position: absolute;
}

#loading-legend {
  font-family: "News Cycle", "sans-serif";
  font-size: 24px;
  color: ivory;
}

#loading-screen {
  left: -25%;
  width: 150%;
  height: 100%;
  background-color: black;
  bottom: 0;
  display: block;
  font-size: 32px;
  overflow: hidden;
  position: relative;
  z-index: 20000;
  opacity: 100%;
}

#loading-wrapper {
  position: absolute;
  width: 100%;
  height: 100%;
}

#loading-text {
  display: block;
  position: absolute;
  top: 50%;
  left: 50%;
  color: white;
  width: 100px;
  height: 30px;
  margin: -7px 0 0 -45px;
  text-align: center;
  font-family: "PT Sans Narrow", sans-serif;
  font-size: 20px;
}

#loading-content {
  display: block;
  position: absolute;
  left: 50%;
  top: 50%;
  width: 170px;
  height: 170px;
  margin: -85px 0 0 -85px;
  border: 3px solid #f00;
}

#loading-content {
  border: 3px solid transparent;
  border-top-color: white;
  border-bottom-color: white;
  border-radius: 50%;
  -webkit-animation: loader 2s linear infinite;
  -moz-animation: loader 2s linear infinite;
  -o-animation: loader 2s linear infinite;
  animation: loader 2s linear infinite;
}

@keyframes loader {
  0% {
    -webkit-transform: rotate(0deg);
    -ms-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
    -ms-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}

.fadeout {
  animation: fadeout 2s forwards;
}

@keyframes fadeout {
  to {
    opacity: 0;
    visibility: hidden;
  }
}
</style>