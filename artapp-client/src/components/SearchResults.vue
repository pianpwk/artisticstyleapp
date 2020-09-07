<template>
    <div>
        <div id="main-picture">
            <img id="main-picture-img" :src="mainImage" width="360px" height="360px" @load="mainPictureLoaded"/>
        </div>
        <div id="search-results-container">
            <SearchResult v-for="result in results" v-bind:result="result" v-bind:key="result.id" @click-image-result="clickImageResult" @image-loaded="incrementCounter" />
        </div>
    </div>
</template>

<script>
import SearchResult from './SearchResult.vue';

var counter = 0;

export default {
    name: "SearchResults",
    props: [
        "mainImage",
        "results"
    ],
    components: {
        SearchResult
    },
    methods: {
        mainPictureLoaded(event) {
            var img = document.getElementById("main-picture-img");
            var maxsize = 360;
            var nw = img.naturalWidth;
            var nh = img.naturalHeight;
            if (Math.max(nw, nh) == nw) {
                nh = (nh / nw) * maxsize;
                nw = maxsize;
            } else {
                nw = (nw / nh) * maxsize;
                nh = maxsize;
            }
            img.style.height = nh + "px";
            img.style.width = nw + "px";
            document.getElementById("main-picture").style.top = "calc(50% - " + parseInt(nh/2) + "px)"
            document.getElementById("main-picture").style.left = "calc(6% + " + parseInt((maxsize-nw)/2) + "px)"
        },
        clickImageResult(result) {
            this.$emit('click-image-result', result)
        },
        incrementCounter(event) {

            var elts = document.getElementsByClassName("search-result-image");
            var len = elts.length;

            counter++;
            if (counter == len) {
                this.results.forEach(function(result, i) {
                    var maxsize = 80;
                    var nw = elts[i].getElementsByClassName("search-result-image-img")[0].naturalWidth;
                    var nh = elts[i].getElementsByClassName("search-result-image-img")[0].naturalHeight;

                    if (Math.max(nw, nh) == nw) {
                        nh = (nh / nw) * maxsize;
                        nw = maxsize;
                    } else {
                        nw = (nw / nh) * maxsize;
                        nh = maxsize;
                    }
                    elts[i].children[0].style.width = nw + "%";

                    var ch = elts[i].clientHeight;
                    var cw = elts[i].clientWidth;
                    elts[i].getElementsByClassName("search-result-image-img")[0].style.height = nh / 100 * ch + "px"
                    elts[i].getElementsByClassName("search-result-image-img")[0].style.width = nw / 100 * cw + "px"
                    elts[i].getElementsByClassName("search-result-image-img")[0].style.top = "32px";
                    elts[i].getElementsByClassName("search-result-image-img")[0].style.left = "0px";

                    var top = parseInt(i / 3) * 48 + "%";
                    var left = parseInt(i % 3) * 32 + "%";
                    elts[i].style.top = top;
                    elts[i].style.left = left;

                    elts[i].getElementsByClassName("search-result-artist")[0].style.top = (32 + nh / 100 * ch) + "px"
                    elts[i].children[0].style.height = (32 + nh / 100 * ch + 24) + "px"

                    var dw = (100 - nw) / 2
                    var dh = (100 - nh) / 2
                    elts[i].children[0].style.top = dh + "%"
                    elts[i].children[0].style.left = dw + "%"
                })
                this.$emit('search-results-done')
            }
        },
        updateResults() {
            counter = 0;
        }
    }
}
</script>

<style lang="scss" scoped>
#main-picture {
    position: absolute;
    left: 8%;
    top: calc(50% - 180px);
    width: 360px;
    height: 360px; // visibility: hidden;
}

#main-picture-img {
    border: solid white 3px;
}

#search-results-container {
    position: absolute;
    left: 30%;
    top: 2%;
    width: 64%;
    height: 96%;
}
</style>