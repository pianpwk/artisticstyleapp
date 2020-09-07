<template>
  <div class="container">
    <img :src="previewImage" class="uploading-image" />
    <input
      type="file"
      accept="image/jpeg"
      @change="uploadImage"
    />
  </div>
</template>

<script>
export default {
  name: "imageUpload",
  data() {
    return {
      previewImage: null,
    };
  },
  methods: {
    uploadImage(e) {
      const image = e.target.files[0];
      const reader = new FileReader();
      reader.readAsDataURL(image);
      reader.onload = (e) => {
        this.previewImage = e.target.result;
        console.log(this.previewImage);
      };
    },
  },
};
</script>

<style lang="scss" scoped>
.container {
  width: 100%;
  height: 100%;
  background-color: white;
  opacity: 1;
  position: absolute;
  z-index: 10000;
}
.uploading-image {
  display: flex;
}
</style>