import Vue from 'vue'
import App from './App.vue'

import VueNumber from 'vue-number-animation';
Vue.use(VueNumber)

import '@/assets/styles/tailwind.css';
import '@/assets/styles/index.css';

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
