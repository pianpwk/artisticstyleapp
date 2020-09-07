<template>
  <div class="container">
    <div id="canvas">
      <div id="loading-screen">
        <div id="loading-text">LOADING</div>
        <div id="loading-content"></div>
      </div>
      <div>
        <particles-bg type="lines" num=1000 color="black" :bg="true" />
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
            :z-index=0
          />
        </div>
        <button id="main-picture-submit" type="button" class="btn btn-light" @click="onSubmitMainPicture">
          Select this image
        </button>
        <button id="main-picture-style" type="button" class="btn btn-light" @click="onSelectStyle">
          Use style transfer
        </button>
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
            :z-index=0
          />
        </div>
        <button id="style-picture-submit" type="button" class="btn btn-light" @click="onSubmitStyle">
          Select this style image
        </button>
        <div id="transfer-style-picture">
          <img id="transfer-style-picture-img" ref="pictureInputTransfer" src="" width="400px" height="400px" />
        </div>
        <button id="transfer-style-picture-submit" type="button" class="btn btn-light" @click="onSubmitMainPicture">
          Use this image
        </button>
      </div>
      <div id="main-picture-result">
        <img id="main-picture-result-img" :src="mainImage" width="360px" height="360px" />
      </div>
      <div id="search-results">
        <div class="search-result-image"
          v-for="image in images"
          v-bind:key="image.id"
          style="vertical-align:middle"
        >
          <img class="search-result-image-img"
            id="image.id"
            :src="image.name"
            width="360px"
            height="360px"
            @mouseover="mouseOverResult"
            @mouseleave="mouseLeaveResult"
            @click="mouseClickResult"
            style="margin:auto"
            border="3px ivory"
          />
          <div class="search-result-title" />
          <div class="search-result-artist" />
          <div class="search-result-date" />
        </div>
      </div>
      <div id="click-image">
        <div id="click-image-bg"
          @click="mouseClickBG" 
        />
        <img id="click-image-img" src="" width="480px" height="480px" />
        <div id="click-image-info" width="200px" height="480px">
          <div id="click-image-info-text" />
        </div>
      </div>
    </div>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=News+Cycle&display=swap');
</style>
<script>
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import PictureInput from "vue-picture-input";
import { LoadingScreen } from "./LoadingScreen.vue"
import axios from "axios";
import { ParticlesBg } from "particles-bg-vue";

function fade(element) {
  var op = 1;  // initial opacity
  var timer = setInterval(function () {
      if (op <= 0.1){
          clearInterval(timer);
          element.style.display = 'none';
      }
      element.style.opacity = op;
      element.style.filter = 'alpha(opacity=' + op * 100 + ")";
      op -= op * 0.1;
  }, 50);
  setTimeout(() => {
    element.style.visibility = "hidden";
  }, 3000);
}
function unfade(element) {
    var op = 0.1;  // initial opacity
    element.style.display = 'block';
    element.style.visibility = 'visible';
    var timer = setInterval(function () {
        if (op >= 1){
            clearInterval(timer);
        }
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op += op * 0.1;
    }, 10);
}
function displayMainImage() {
  document.getElementById("main-picture-result-img").style.visibility = 'visible';
}
function displayClickImage() {
  var clickimage = document.getElementById("click-image-img");
  var maxsize = 900;

  var nw = clickimage.naturalWidth;
  var nh = clickimage.naturalHeight;
  if (Math.max(nw, nh) == nw) {
    nh = (nh / nw) * maxsize;
    nw = maxsize;
  } else {
    maxsize = 720;
    nw = (nw / nh) * maxsize;
    nh = maxsize;
  }
  clickimage.style.height = nh + "px";
  clickimage.style.width = nw + "px";

  var parent = document.getElementById("click-image");
  var pw = parent.style.width;
  var ph = parent.style.height;
  clickimage.style.position = "absolute";
  clickimage.style.top = 'calc(50% - ' + (nh/2) + "px)";
  clickimage.style.left = 'calc(50% - ' + (nw+200)/2 + "px)";

  var info = document.getElementById("click-image-info");
  info.style.position = "absolute";
  info.style.top = 'calc(50% - ' + (nh/2) + "px)";
  info.style.left = 'calc(50% - ' + ((320-nw)/2) + "px)";
  info.style.height = nh + "px";
  info.style.width = 320 + "px";

  info.innerHTML = mainImageName + '<p></p>' + mainImageArtist + '<p></p>' + mainImageDate;

  parent.style.visibility = 'visible';
}

var useStyleTransferPicture = false;
var mainImageName = '';
var mainImageArtist = '';
var mainImageDate = '';

export default {
  name: "Home",
  data() {
    return {
      isLoading: true,
      selectedFile: null,
      url: null,
      mainImage: null,
      images: [
        {
          id: 0,
          name:
            "https://fineartreproductionstudio.com/wp-content/uploads/2019/06/cezanne-art.jpg"
        },
        {
          id: 1,
          name: ""
        },
        {
          id: 2,
          name: ""
        },
        {
          id: 3,
          name: ""
        },
        {
          id: 4,
          name: ""
        },
        {
          id: 5,
          name: ""
        }
      ],
      cacheKey: +new Date()
    };
  },
  mounted() {
    setTimeout(() => {
      fade(document.getElementById("loading-screen"));
    }, 3000)
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
    ParticlesBg
  },
  methods: {
    mouseOverResult(event) {
      event.srcElement.style.opacity = 0.8;
      event.srcElement.parentNode.children[1].style.opacity = 0.8;
      event.srcElement.parentNode.children[2].style.opacity = 0.8;
    },
    mouseLeaveResult(event) {
      event.srcElement.style.opacity = 1.0;
      event.srcElement.parentNode.children[1].style.opacity = 1.0;
      event.srcElement.parentNode.children[2].style.opacity = 1.0;
    },
    mouseClickResult(event) {
      console.log(event.srcElement.parentNode);
      mainImageName = event.srcElement.parentNode.children[1].innerHTML;
      mainImageArtist = event.srcElement.parentNode.children[2].innerHTML;
      mainImageDate = event.srcElement.parentNode.children[3].innerHTML;
      document.getElementById("click-image-img").addEventListener(
        "load", displayClickImage
      );
      document.getElementById("click-image-img").src = event.srcElement.src;
    },
    mouseClickBG(event) {
      document.getElementById("click-image").style.visibility = 'hidden';
    },
    onSelectStyle() {
      document.getElementById("style-picture-upload").style.visibility = 'visible';
    },
    onSubmitMainPicture() {
      if (!useStyleTransferPicture) {
        fade(document.getElementById("main-picture-upload"));
        fade(document.getElementById("main-picture-submit"));
        fade(document.getElementById("main-picture-style"));
        unfade(document.getElementById("loading-screen"));
        var mainImage = this.$refs.pictureInput.image;
        var mainImageName = this.$refs.pictureInput.file.name;
      } else {
        fade(document.getElementById("transfer-style-picture"));
        fade(document.getElementById("transfer-style-picture-submit"));
        unfade(document.getElementById("loading-screen"));
        var mainImage = this.$refs.pictureInputTransfer.src;
        var mainImageName = ''
      }
      document.getElementById("main-picture-result").visibility = "visible";
      axios
        .post("http://localhost:5000/image_upload", {
          name: mainImageName,
          data: mainImage
        })
        .then(res => {
          function incrementCounter() {
            counter++;
            if (counter == len) {
              for (var i of Array(6).keys()) {
                var maxsize = 84;
                var nw = elts[i].children[0].naturalWidth;
                var nh = elts[i].children[0].naturalHeight;
                if (Math.max(nw, nh) == nw) {
                  nh = (nh / nw) * maxsize;
                  nw = maxsize;
                } else {
                  nw = (nw / nh) * maxsize;
                  nh = maxsize;
                }
                elts[i].children[0].style.height = nh+"%";
                elts[i].children[0].style.width = nw+"%";

                var top = parseInt(i / 3)*50 + "%";
                var left = parseInt(i % 3)*33 + "%";
                elts[i].style.top = top;
                elts[i].style.left = left;

                var title = document.getElementsByClassName("search-result-title");
                var artist = document.getElementsByClassName("search-result-artist");

                title[i].style.top = (elts[i].children[0].offsetTop - 30) + "px";
                title[i].style.left = (elts[i].children[0].offsetLeft) + "px";
                artist[i].style.top = (elts[i].children[0].offsetTop + elts[i].children[0].height + 6) + "px";
                artist[i].style.left = (elts[i].children[0].offsetLeft) + "px";

                title[i].style.width = nw + "%";
                artist[i].style.width = nw + "%";

              }
              document.getElementById("search-results").style.visibility =
                "visible";
              fade(document.getElementById("loading-screen"));
            }
          }
          document.getElementById("main-picture-result-img").addEventListener(
            "load", displayMainImage
          );
          document.getElementById("main-picture-result-img").src = mainImage;
          var elts = document.getElementsByClassName("search-result-image");
          var len = elts.length;
          var counter = 0;
          res.data.slice(0, 6).forEach(function(item, i) {
            elts[i].children[0].addEventListener(
              "load",
              incrementCounter,
              false
            );
            elts[i].children[0].src = item['url'];
            document.getElementsByClassName("search-result-title")[i].innerHTML = item['title'].toUpperCase();
            var artist_name = item['artist']
            if (artist_name == '') {
              artist_name = 'Unknown artist'
            }
            var artdate = item['date']
            if (artdate == '') {
              artdate = 'Unknown date'
            }
            document.getElementsByClassName("search-result-artist")[i].innerHTML = artist_name;
            document.getElementsByClassName("search-result-date")[i].innerHTML = artdate;
          });
        });
    },
    onUploadMainPicture(image) {
      document.getElementById("main-picture-submit").style.visibility = "visible";
      document.getElementById("main-picture-style").style.visibility = "visible";
      // document.getElementById("main-picture-submit").addEventListener("click", onSubmitMainPicture);
    },
    onUploadStylePicture(image) {
      document.getElementById("style-picture-submit").style.visibility = "visible";
    },
    onSubmitStyle() {
      useStyleTransferPicture = true;
      unfade(document.getElementById('loading-screen'));
      fade(document.getElementById("main-picture-upload"));
      fade(document.getElementById("main-picture-submit"));
      fade(document.getElementById("main-picture-style"));
      fade(document.getElementById("style-picture-upload"));
      fade(document.getElementById("style-picture-submit"));
      axios
        .post("http://localhost:5000/upload_style_transfer", {
          data: [
            this.$refs.pictureInput.image,
            this.$refs.pictureInputStyle.image
          ]
        })
        .then(res => {
          document.getElementById("transfer-style-picture").style.visibility = 'visible';
          document.getElementById("transfer-style-picture-submit").style.visibility = 'visible';
          document.getElementById("transfer-style-picture-img").src =
            "data:image/png;base64," + res.data;
          fade(document.getElementById('loading-screen'));
        });
    }
  }
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
  font-family: 'PT Sans Narrow', sans-serif;
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
  border: 3px solid #F00;
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

#main-picture-upload {
  width: 400px;
  height: 400px;
  position: absolute;
  left: calc(50% - 200px);
  top: calc(50% - 200px);
  background-color: white;
  opacity: 1;
  position: absolute;
  z-index: 10000;
}

#main-picture-submit {
  width: 160px;
  height: 36px;
  position: absolute;
  left: calc(50% - 80px - 90px);
  top: calc(50% + 200px + 10px);
  background-color: white;
  visibility: hidden;
  display: inline-block;
  text-align: center;
  font-family: sans-serif;
  font-size: 16px;
}

#main-picture-style {
  width: 160px;
  height: 36px;
  position: absolute;
  left: calc(50% - 80px + 90px);
  top: calc(50% + 200px + 10px);
  background-color: white;
  visibility: hidden;
  display: inline-block;
  text-align: center;
  font-family: sans-serif;
  font-size: 16px;
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
  background-color: white;
  visibility: hidden;
  display: inline-block;
  text-align: center;
  font-family: sans-serif;
  font-size: 16px;
}

#style-picture-upload {
  width: 400px;
  height: 400px;
  position: absolute;
  left: calc(50% - 200px + 420px);
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
  left: calc(50% + 420px - 100px);
  top: calc(50% - 200px + 400px + 10px);
  background-color: white;
  visibility: hidden;
  display: inline-block;
  text-align: center;
  font-family: sans-serif;
  font-size: 16px;
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
  left: 30%;
  top: 6%;
  width: 66%;
  height: 92%;
  visibility: hidden;
}

.search-result-title {
  position: absolute;
  background-color: ivory;
  color: #2e3636;
  font-family: 'News Cycle', sans-serif;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  padding-top: 2px;
  padding-left: 6px;
  padding-right: 6px;
  text-align: left;
  font-size: 19px;
  width: 92%;
  height: 32px;
}

.search-result-artist {
  position: absolute;
  background-color: ivory;
  color: #2e3636;
  font-family: 'News Cycle', sans-serif;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  padding-left: 6px;
  padding-right: 6px;
  vertical-align: top;
  text-align: left;
  font-size: 14px;
  width: 92%;
  height: 16px;
  line-height: 100%;
}

.search-result-date {
  visibility: hidden;
}

.search-result-image {
  width: 33%;
  height: 50%;
  position: absolute;
  vertical-align: middle;
  display: flex;
}

.search-result-image-img {
  border: solid white 3px;
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
  position: absolute;
  left: calc(50% - 400px);
  top: calc(50% - 400px);
  z-index: 10001;
}

#click-image-info {
  position: absolute;
  z-index: 10001;
  background-color: ivory;
  color: #2e3636;
  font-family: 'News Cycle', sans-serif;
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

