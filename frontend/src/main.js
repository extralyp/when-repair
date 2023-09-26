import { VNetworkGraph } from 'v-network-graph'
import { createApp } from 'vue'
import "v-network-graph/lib/style.css"
import App from './App.vue'
import router from './router'
import store from './store'
import "@/styles/global.css"
import components from '@/components/UI'
import axios from 'axios'
import VueApexCharts from "vue3-apexcharts"



axios.defaults.baseURL="http://192.168.56.81:55002/"



const app = createApp(App)




components.forEach(component => {
    app.component(component.name, component)
})

app.use(VNetworkGraph)
.use(VueApexCharts)
.use(router)
.use(store)
.mount('#app')