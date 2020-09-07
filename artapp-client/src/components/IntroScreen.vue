<template>
  <div id="intro-screen">
    <div id="intro-images">
      <img id="intro-img-0" src="../assets/images/header0.jpg" />

      <img class="intro-img-border" src="../assets/images/border.png" />

      <img id="intro-img-1" src="../assets/images/header1.jpg" />

      <img class="intro-img-border" src="../assets/images/border.png" />

      <img id="intro-img-2" src="../assets/images/header2.jpg" />

      <img class="intro-img-border" src="../assets/images/border.png" />

      <img id="intro-img-3" src="../assets/images/header3.jpg" />

      <img class="intro-img-border" src="../assets/images/border.png" />

      <img id="intro-img-4" src="../assets/images/header4.jpg" />
    </div>

    <div id="intro-text">
      This app allows you to search similar artworks and images from over 100,000 Open Access Images,
      <br />indexed from the Metropolitan Museum of Art, the Rijksmuseum, and the Europeana art collections.
      <p></p>You can search using an artwork of your own, or of a prominent artist,
      <br />or using an artwork generated with our style transfer feature,
      <br />to be analyzed by our deep learning backend for similarity search.
      <p></p>
    </div>

    <div id="intro-instruction">
      <img id="intro-instr-img-1" src="../assets/images/instruction_1.png" />

      <img
        src="../assets/images/border.png"
        width="24px"
        height="100%"
        style="border-right: solid 2px ivory;"
      />

      <img src="../assets/images/border.png" width="24px" height="100%" />

      <img id="intro-instr-img-2" src="../assets/images/instruction_2.png" />
    </div>
    <button id="button-continue" type="button" class="btn btn-light" @click="continueIntro">CONTINUE</button>
    <div id="end-text">
      * Best in full screen mode *
    </div>
  </div>
</template>

<script>
export default {
  name: "IntroScreen",
  methods: {
      continueIntro() {
          this.$emit('continue-intro')
      }
  }
};
</script>

<style lang="scss" scoped>
@import url("https://fonts.googleapis.com/css2?family=News+Cycle&display=swap");
#intro-screen {
  width: 100%;
  height: 100%;
  background-color: black;
  z-index: 30000;
  position: relative;
}

#intro-images {
  width: 100%;
  height: 30%;
  top: 10%;
  position: relative;
}

#intro-img-0,
#intro-img-1,
#intro-img-2,
#intro-img-3,
#intro-img-4 {
  height: 100%;
  border: solid 1px ivory;
  border-radius: 2px;
}

.intro-img-border {
  height: 100%;
  width: 20px;
}

#intro-text {
  color: ivory;
  top: 14%;
  width: 60%;
  position: relative;
  text-align: center;
  font-family: "News Cycle", sans-serif;
  font-size: 18px;
  left: 20%;
}

#intro-instruction {
  width: 100%;
  height: 150px;
  top: 16%;
  position: relative;
}

#intro-instr-img-1,
#intro-instr-img-2 {
  height: 100%;
  position: relative;
}

#intro-instr-img-1 {
    padding-left: 20px;
}

#button-continue {
  background-color: black;
  border: solid 1.5px ivory;
  color: ivory;
  display: inline-block;
  text-align: center;
  font-family: "News Cycle", sans-serif;
  font-size: 16px;
  line-height: 100%;
  border-radius: 2px;
  position: absolute;
  bottom: 4%;
  width: 100px;
  left: calc(50% - 50px);
}

#end-text {
  position: absolute;
  bottom: 1%;
  text-align: center;
  font-family: 'News Cycle';
  font-size: 12px;
  color: #aa8;
  width: 240px;
  left: calc(50% - 120px);
}
</style>