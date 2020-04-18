import Vue from 'vue';
import AsyncComputed from 'vue-async-computed';
import VTooltip from 'v-tooltip';
import { BootstrapVue } from 'bootstrap-vue';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

require('typeface-rubik');

Vue.config.productionTip = false;
Vue.use(VTooltip);
Vue.use(AsyncComputed);
Vue.use(BootstrapVue);

Vue.prototype.$hostname = 'http://192.168.1.142:5000';

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
