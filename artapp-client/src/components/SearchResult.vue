<template>
    <div class="search-result-image">
        <div class="search-result-image-container">
            <img class="search-result-image-img"
                :src="result.url"
                width="360px"
                height="360px"
                @mouseover="mouseOverResult"
                @mouseleave="mouseLeaveResult"
                @click="mouseClickResult"
                @load="imageLoaded"
                style="margin:auto"
                border="3px ivory"
            />
            <div class="search-result-title">
                {{ result.title }}
            </div>
            <div class="search-result-artist">
                {{ result.artist }}
            </div>
            <div class="search-result-date">
                {{ result.date }}
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'SearchResult',
        props: ['result'],
        methods: {
            mouseOverResult(event) {
                event.srcElement.parentNode.style.opacity = 0.8;
            },
            mouseLeaveResult(event) {
                event.srcElement.parentNode.style.opacity = 1.0;
            },
            mouseClickResult(event) {
                this.$emit('click-image-result', this.result);
            },
            imageLoaded(event) {
                this.$emit('image-loaded', event);
            }
        }
    }
</script>

<style lang="scss" scoped>

.search-result-image {
    width: 33%;
    height: 48%;
    vertical-align: middle;
    display: flex;
    position: absolute;
}

.search-result-image-img {
    position: absolute;
    top: 10%;
    cursor: pointer;
}

.search-result-image-container {
    position: relative;
    background-color: ivory;
    color: #2e3636;
}

.search-result-title {
    position: absolute;
    padding-top: 2px;
    padding-left: 6px;
    padding-right: 6px;
    text-align: left;
    font-size: 19px;
    width: 92%;
    height: 12%;
    top: 0px;

    font-family: 'News Cycle', sans-serif;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
}

.search-result-artist {
    position: absolute;
    padding-left: 6px;
    padding-right: 6px;
    // vertical-align: top;
    text-align: left;
    font-size: 14px;
    width: 92%;
    height: 24px;
    line-height: 200%;
    // bottom: 0px;

    font-family: 'News Cycle', sans-serif;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
}

.search-result-date {
    visibility: hidden;
}

</style>