import Vue from 'vue'
import App from './App.vue'

import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
Vue.use(ElementUI)

import axios from 'axios'
Vue.prototype.$axios = axios

import VueCookies from 'vue-cookies'
Vue.use(VueCookies)

import VideoPlayer from 'vue-video-player'
import 'vue-video-player/src/custom-theme.css'
import 'video.js/dist/video-js.css'

Vue.use(VideoPlayer)
Vue.config.productionTip = false

import echarts from 'echarts'
Vue.prototype.$echarts = echarts

Vue.prototype.$main_url = "http://127.0.0.1:8000"

new Vue({
  render: h => h(App),
}).$mount('#app')