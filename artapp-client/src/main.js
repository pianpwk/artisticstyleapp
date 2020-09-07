import Vue from 'vue';
import App from './App.vue';
import router from './router';
Vue.config.productionTip = false;
import VueEllipseProgress from 'vue-ellipse-progress';

Vue.use(VueEllipseProgress);

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
