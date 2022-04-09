import { createApp } from './vue'
import navbar from "../vue/navbar.vue"
import map from "../vue/map.vue"
import about from "../vue/about.vue"
import msg from "../vue/msg.vue"

createApp(navbar).mount('#navbar')
createApp(map).mount('#map-frame')
createApp(about).mount('#about')
createApp(msg).mount('#msg')
