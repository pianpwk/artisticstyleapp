<template>
  <div class="container">
    <div id="canvas">
      <IntroScreen id="intro-screen" @continue-intro="continueIntro" />

      <LoadingScreen
        ref="loadingScreen"
        v-bind:progress="loadingProgress"
        v-bind:loadingText="loadingText"
        id="loading-screen"
        style="visibility: hidden;"
      ></LoadingScreen>

      <div>
        <particles-bg type="lines" num="1000" color="black" :bg="true" />

        <div id="main-picture-text">
          Upload an image or artwork
        </div>

        <div id="main-picture-upload">
          <picture-input
            ref="pictureInput"
            @change="onUploadMainPicture"
            button-class="btn"
            :customStrings="{
    
                  drag: ''
    
                }"
            :hideChangeButton="true"
            :crop="false"
            :toggleAspectRatio="true"
            :autoToggleAspectRatio="true"
          />
        </div>

        <button
          id="main-picture-submit"
          type="button"
          class="btn btn-light"
          @click="onSubmitMainPicture"
        >SEARCH</button>

        <button
          id="main-picture-style"
          type="button"
          class="btn btn-light"
          @click="onSelectStyle"
        >APPLY STYLE</button>

        <div id="style-picture-text">
          Upload an artwork for styling
        </div>

        <div id="style-picture-upload">
          <picture-input
            ref="pictureInputStyle"
            @change="onUploadStylePicture"
            button-class="btn"
            :customStrings="{
    
                  drag: ''
    
                }"
            :hideChangeButton="true"
            :crop="false"
            :z-index="0"
          />
        </div>

        <button
          id="style-picture-submit"
          type="button"
          class="btn btn-light"
          @click="onSubmitStyle"
        >USE THIS STYLE</button>

        <div id="transfer-style-picture">
          <img
            id="transfer-style-picture-img"
            ref="pictureInputTransfer"
            src
            width="400px"
            height="400px"
          />
        </div>

        <button
          id="transfer-style-picture-submit"
          type="button"
          class="btn btn-light"
          @click="onSubmitMainPicture"
        >SUBMIT</button>
      </div>

      <SearchResults
        v-bind:mainImage="mainImage"
        v-bind:results="results"
        id="search-results"
        ref="searchResults"
        @search-results-done="displaySearchResults"
        @click-image-result="clickImageResult"
      />

      <div id="click-image">
        <div id="click-image-bg" @click="mouseClickBG" />

        <img id="click-image-img" width="460px" height="460px" />

        <div id="click-image-info" width="200px" height="460px">
          <div id="click-image-info-text" />
        </div>
      </div>
    </div>
  </div>
</template>

<style>
@import url("https://fonts.googleapis.com/css2?family=News+Cycle&display=swap");
</style>
<script>
import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import PictureInput from "vue-picture-input";
import SearchResults from "./SearchResults";
import LoadingScreen from "./LoadingScreen.vue";
import IntroScreen from "./IntroScreen.vue";
import ImageUpload from "./ImageUpload";
import axios from "axios";
import { ParticlesBg } from "particles-bg-vue";

function fade(element, duration = 1000) {
  var op = 1; // initial opacity
  var timer = setInterval(function () {
    if (op <= 0.1) {
      clearInterval(timer);
      element.style.display = "none";
    }
    element.style.opacity = op;
    element.style.filter = "alpha(opacity=" + op * 100 + ")";
    op -= op * 0.1;
  }, 50);
  setTimeout(() => {
    element.style.visibility = "hidden";
  }, duration);
}

function unfade(element) {
  var op = 0.1; // initial opacity
  element.style.display = "block";
  element.style.visibility = "visible";
  var timer = setInterval(function () {
    if (op >= 1) {
      clearInterval(timer);
    }
    element.style.opacity = op;
    element.style.filter = "alpha(opacity=" + op * 100 + ")";
    op += op * 0.1;
  }, 10);
}

function displayMainImage() {
  document.getElementById("main-picture-result-img").style.visibility =
    "visible";
}

function displayClickImage(result) {
  mainImageName = result.title;
  mainImageArtist = result.artist;
  mainImageDate = result.date;

  var clickimage = document.getElementById("click-image-img");
  var maxsize = 880;

  var nw = clickimage.naturalWidth;
  var nh = clickimage.naturalHeight;
  if (Math.max(nw, nh) == nw) {
    nh = (nh / nw) * maxsize;
    nw = maxsize;
  } else {
    maxsize = 700;
    nw = (nw / nh) * maxsize;
    nh = maxsize;
  }
  clickimage.style.height = nh + "px";
  clickimage.style.width = nw + "px";
  clickimage.src = result.url;

  var parent = document.getElementById("click-image");
  var pw = parent.style.width;
  var ph = parent.style.height;
  clickimage.style.position = "absolute";
  clickimage.style.top = "calc(50% - " + nh / 2 + "px)";
  clickimage.style.left = "calc(50% - " + (nw + 200) / 2 + "px)";

  var info = document.getElementById("click-image-info");
  info.style.position = "absolute";
  info.style.top = "calc(50% - " + nh / 2 + "px)";
  info.style.left = "calc(50% - " + (320 - nw) / 2 + "px)";
  info.style.height = nh + "px";
  info.style.width = 320 + "px";

  info.innerHTML =
    mainImageName + "<p></p>" + mainImageArtist + "<p></p>" + mainImageDate;

  clickimage.addEventListener("load", () => {
    parent.style.visibility = "visible";
  });
}

var useStyleTransferPicture = false;
var mainImageName = "";
var mainImageArtist = "";
var mainImageDate = "";

export default {
  name: "Home2",
  data() {
    return {
      loadingText: "Initializing App",
      loadingProgress: 0,
      selectedFile: null,
      url: null,
      token: null,
      mainImage: null,
      results: [
        {
          id: 0,
          name: "",
        },
        {
          id: 1,
          name: "",
        },
        {
          id: 2,
          name: "",
        },
        {
          id: 3,
          name: "",
        },
        {
          id: 4,
          name: "",
        },
        {
          id: 5,
          name: "",
        },
      ],
      cacheKey: +new Date(),
    };
  },
  mounted() {
    this.$data.loadingText = "Initializing App";
    setTimeout(() => {
      this.$data.loadingProgress = 100;
    }, 2000);
  },
  created() {
    this.interval = setInterval(() => {
      this.cacheKey = +new Date();
    }, 60 * 1000);
  },
  destroyed() {
    clearInterval(this.interval);
  },
  components: {
    PictureInput,
    ParticlesBg,
    LoadingScreen,
    IntroScreen,
    SearchResults,
    ImageUpload,
  },
  methods: {
    continueIntro() {
      fade(document.getElementById("intro-screen"), 5000);
    },
    mouseClickBG(event) {
      document.getElementById("click-image").style.visibility = "hidden";
    },
    onSelectStyle() {
      document.getElementById("style-picture-text").style.visibility = 
        "visible";
      document.getElementById("style-picture-upload").style.visibility =
        "visible";
      document.getElementById("main-picture-text").style.left = 
        "calc(50% - 400px - 20px)"
      document.getElementById("main-picture-upload").style.left =
        "calc(50% - 400px - 20px)";
      document.getElementById("main-picture-submit").style.left =
        "calc(50% - 400px + 10px)";
      document.getElementById("main-picture-style").style.left =
        "calc(50% - 400px + 190px)";
    },
    clickImageResult(result) {
      displayClickImage(result);
      displayClickImage(result);
    },
    displaySearchResults() {
      this.$data.loadingText = "Artworks retrieved";
      this.$data.loadingProgress = 100;
      setTimeout(() => {
        document.getElementById("search-results").style.visibility = "visible";
        fade(document.getElementById("loading-screen"));
      }, 1000);
    },
    onSubmitMainPicture() {
      this.$data.loadingText = "Sending image to server";
      this.$data.loadingProgress = 0;
      setTimeout(() => {
        if (!useStyleTransferPicture) {
          fade(document.getElementById("main-picture-text"));
          fade(document.getElementById("main-picture-upload"));
          fade(document.getElementById("main-picture-submit"));
          fade(document.getElementById("main-picture-style"));
          fade(document.getElementById("style-picture-text"));
          fade(document.getElementById("style-picture-upload"));
          fade(document.getElementById("style-picture-submit"));
          unfade(document.getElementById("loading-screen"));
          var mainImage = this.$refs.pictureInput.image;
          var mainImageName = this.$refs.pictureInput.file.name;
        } else {
          fade(document.getElementById("transfer-style-picture"));
          fade(document.getElementById("transfer-style-picture-submit"));
          unfade(document.getElementById("loading-screen"));
          var mainImage = this.$refs.pictureInputTransfer.src;
          var mainImageName = "";
        }
        axios
          .post("http://localhost:5000/request_image_upload", {})
          .then((res) => {
            this.$data.token = res.data.token;
            axios
              .post("http://localhost:5000/image_upload", {
                name: mainImageName,
                data: mainImage,
                token: this.$data.token,
              })
              .then((res) => {
                clearInterval(prInt);
                this.$data.loadingText = "Loading artworks";
                this.$data.loadingProgress = 75;
                var results = [];
                res.data.forEach(function (item, i) {
                  var url = item.url;
                  var title = item.title.toUpperCase();
                  var artist = item.artist.toUpperCase();
                  if (artist == "") {
                    artist = "Unknown Artist";
                  }
                  var artdate = item.date;
                  if (artdate == "") {
                    artdate = "Unknown Date";
                  }
                  results.push({
                    url: url,
                    title: title,
                    artist: artist,
                    date: artdate,
                  });
                });
                this.mainImage = mainImage;
                this.results = results;
                this.$refs.searchResults.updateResults();
              });
          });
        var prInt = setInterval(() => {
          if (this.$data.token) {
            axios
              .post("http://localhost:5000//progress_image_upload", {
                token: this.$data.token,
              })
              .then((res) => {
                var pr_msg = null;
                var pr_val = null;
                if (res.data == "processing") {
                  pr_msg = "Image received by server";
                  pr_val = 15;
                } else if (res.data == "analyzed") {
                  pr_msg = "Analysis done";
                  pr_val = 30;
                } else if (res.data == "done1") {
                  pr_msg = "Found 1/6 artworks";
                  pr_val = 35;
                } else if (res.data == "done2") {
                  pr_msg = "Found 2/6 artworks";
                  pr_val = 40;
                } else if (res.data == "done3") {
                  pr_msg = "Found 3/6 artworks";
                  pr_val = 45;
                } else if (res.data == "done4") {
                  pr_msg = "Found 4/6 artworks";
                  pr_val = 50;
                } else if (res.data == "done5") {
                  pr_msg = "Found 5/6 artworks";
                  pr_val = 55;
                } else if (res.data == "done6") {
                  pr_msg = "Found 6/6 artworks";
                  pr_val = 60;
                }
                if (pr_msg) {
                  this.$data.loadingText = pr_msg;
                  this.$data.loadingProgress = pr_val;
                }
              });
          }
        }, 500);
      }, 500);
    },
    onUploadMainPicture(image) {
      document.getElementById("main-picture-upload").style.backgroundColor =
        "transparent";
      document.getElementById("main-picture-submit").style.visibility =
        "visible";
      document.getElementById("main-picture-style").style.visibility =
        "visible";
    },
    onUploadStylePicture(image) {
      document.getElementById("style-picture-submit").style.visibility =
        "visible";
      document.getElementById("style-picture-upload").style.backgroundColor =
        "transparent";
      document.getElementById("style-picture-text").style.visibility = 
        "visible";
    },
    onSubmitStyle() {
      this.$data.loadingText = "Sending images to server";
      this.$data.loadingProgress = 0;
      useStyleTransferPicture = true;
      unfade(document.getElementById("loading-screen"));
      fade(document.getElementById("main-picture-text"));
      fade(document.getElementById("main-picture-upload"));
      fade(document.getElementById("main-picture-submit"));
      fade(document.getElementById("main-picture-style"));
      fade(document.getElementById("style-picture-text"));
      fade(document.getElementById("style-picture-upload"));
      fade(document.getElementById("style-picture-submit"));
      axios
        .post("http://localhost:5000/request_style_transfer", {})
        .then((res) => {
          this.$data.token = res.data.token;
          axios
            .post("http://localhost:5000/upload_style_transfer", {
              data: [
                this.$refs.pictureInput.image,
                this.$refs.pictureInputStyle.image,
              ],
              token: this.$data.token
            })
            .then((res) => {
              clearInterval(prInt);
              this.$data.loadingText = "Style transfer done";
              this.$data.loadingProgress = 100;
              document.getElementById(
                "transfer-style-picture"
              ).style.visibility = "visible";
              document.getElementById(
                "transfer-style-picture-submit"
              ).style.visibility = "visible";
              document.getElementById("transfer-style-picture-img").src =
                "data:image/png;base64," + res.data;
              fade(document.getElementById("loading-screen"));
            });
        });
      var prInt = setInterval(() => {
        if (this.$data.token) {
          axios
            .post("http://localhost:5000/progress_style_transfer", {
              token: this.$data.token,
            })
            .then((res) => {
              var pr_msg = null;
              var pr_val = null;
              if (res.data == "received") {
                pr_msg = "Image received";
                pr_val = 15;
              } else if (res.data == "content feature") {
                pr_msg = "Content analyzed";
                pr_val = 30;
              } else if (res.data == "style feature") {
                pr_msg = "Style analyzed";
                pr_val = 45;
              } else if (res.data == "finalizing") {
                pr_msg = "Decoding completed";
                pr_val = 80;
              } else if (res.data == "preparing") {
                pr_msg = "Waiting for result";
                pr_val = 90;
              }
              if (pr_msg) {
                this.$data.loadingText = pr_msg;
                this.$data.loadingProgress = pr_val;
              }
            });
        }
      }, 500);
    },
  },
};
</script>

<style lang="scss" scoped>
.container {
  width: 100%;
  height: 100%;
}

#canvas {
  width: 150%;
  height: 100%;
  left: -25%;
  position: relative;
}

#main-picture-text {
  width: 400px;
  position: absolute;
  left: calc(50% - 200px);
  top: calc(50% - 200px - 36px);
  color: ivory;
  font-family: "News Cycle";
  font-size: 20px;
  z-index: 10000;
}

#main-picture-upload {
  width: 400px;
  height: 400px;
  position: absolute;
  left: calc(50% - 200px);
  top: calc(50% - 200px);
  background-color: ivory;
  opacity: 1;
  position: absolute;
  z-index: 10000;
}

#main-picture-submit,
#main-picture-style,
#transfer-style-picture-submit,
#style-picture-submit {
  background-color: black;
  border: solid 1.5px ivory;
  color: ivory;
  visibility: hidden;
  display: inline-block;
  text-align: center;
  font-family: "News Cycle", sans-serif; // font-weight: bold;
  font-size: 16px;
  line-height: 100%;
  border-radius: 2px;
}

#main-picture-submit {
  width: 160px;
  height: 36px;
  position: absolute;
  left: calc(50% - 80px - 90px);
  top: calc(50% + 200px + 10px);
}

#main-picture-style {
  width: 160px;
  height: 36px;
  position: absolute;
  left: calc(50% - 80px + 90px);
  top: calc(50% + 200px + 10px);
}

#transfer-style-picture {
  width: 400px;
  height: 400px;
  position: absolute;
  left: calc(50% - 200px);
  top: calc(50% - 200px);
  background-color: white;
  opacity: 1;
  position: absolute;
  visibility: hidden;
}

#transfer-style-picture-submit {
  width: 200px;
  height: 36px;
  position: absolute;
  left: calc(50% - 100px);
  top: calc(50% + 200px + 10px);
}

#style-picture-text {
  width: 400px;
  position: absolute;
  left: calc(50% + 20px);
  top: calc(50% - 200px - 36px);
  color: ivory;
  font-family: "News Cycle";
  font-size: 20px;
  z-index: 10000;
  visibility: hidden;
}

#style-picture-upload {
  width: 400px;
  height: 400px;
  position: absolute;
  left: calc(50% + 20px);
  top: calc(50% - 200px);
  background-color: white;
  opacity: 1;
  position: absolute;
  visibility: hidden;
}

#style-picture-submit {
  width: 200px;
  height: 36px;
  position: absolute;
  left: calc(50% + 20px + 200px - 100px);
  top: calc(50% - 200px + 400px + 10px);
}

#main-picture-result {
  position: absolute;
  left: 5%;
  top: calc(50% - 180px);
  width: 360px;
  height: 360px;
  visibility: hidden;
}

#main-picture-result-img {
  border: solid white 3px;
}

#search-results {
  position: absolute;
  width: 100%;
  height: 100%;
  visibility: hidden;
}

#click-image {
  position: relative;
  left: -25%;
  top: 0px;
  width: 150%;
  height: 100%;
  visibility: hidden;
}

#click-image-bg {
  position: absolute;
  background-color: blanchedalmond;
  width: 100%;
  height: 100%;
  z-index: 10000;
  opacity: 0.2;
}

#click-image-img {
  width: 460px;
  height: 460px;
  position: absolute;
  left: calc(50% - 400px);
  top: calc(50% - 400px);
  z-index: 10001;
}

#click-image-info {
  width: 200px;
  height: 460px;
  position: absolute;
  z-index: 10001;
  background-color: ivory;
  color: #2e3636;
  font-family: "News Cycle", sans-serif;
  padding-left: 32px;
  padding-right: 32px;
  padding-top: 36px;
}

.image {
  width: 200px;
  height: 200px;
}

.upload {
  width: 200px;
  height: 200px;
  background-color: blanchedalmond;
  position: absolute;
  left: 100px;
  top: 20px;
}

.upload-style {
  width: 200px;
  height: 200px;
  background-color: blanchedalmond;
  position: absolute;
  left: 100px;
  top: 240px;
}

.image-style {
  width: 200px;
  height: 200px;
  position: absolute;
  left: 100px;
  top: 460px;
}

.particles-bg {
  position: relative;
  width: 100%;
  height: 100%;
}
</style>

