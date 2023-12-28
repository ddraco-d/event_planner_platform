import Vue from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';
import store from './store';


Vue.prototype.$http = axios.create({
  baseURL: 'http://localhost:8000',
});



// console.log(axios.defaults)
// console.log(Vue.prototype.$http.defaults)


new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app');