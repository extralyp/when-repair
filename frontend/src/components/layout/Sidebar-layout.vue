<template>
    <div class="folders_container"  :class="{'folders_container_open': (isOpenMenu), 'folders_container_close': (!isOpenMenu)}">
        <div class="folders">
            <div v-if="selectOption !== 'mode'">
                <h4>Информация по тр-ду: {{ selectedTube }}</h4>
                <div style="width: 400px; height: 300px">
                    <LineChart
                        :data="data"
                    >
                    </LineChart>
                </div>
            </div>
            <div v-if="selectOption==='mode'">
                <img src="@/assets/img/mode.png" style="width: 400px; height: 450px">
            </div>
        </div>
        <div class="icon_container" >
            <img v-if="isOpenMenu" @click="toggleMenu" class='hamburger' id='arrow' src="@/assets/img/down-green.svg" style="transform: rotate(90deg);" title = "Скрыть">
            <img v-if="!isOpenMenu" @click="toggleMenu" class='hamburger' id='arrow' src="@/assets/img/down-green.svg" style="transform: rotate(270deg);" title = "Открыть">
        </div>
        
    </div>

</template>
 
<script setup>
import { ref, watch } from "vue"
import LineChart from '@/components/charts/LineChart.vue'

const isOpenMenu = ref(false)
const toggleMenu = () => {
  isOpenMenu.value = !isOpenMenu.value
}
const data = ref(null)

const props = defineProps({
    selectedTube: {
        type: String,
        required: false
        },
    chartData: {
        type: Object,
        required: false
        }, 
    selectOption:{
            type:String,
            required:false
        }
})

watch(()=>props.selectedTube, (oldValue, newValue) =>{
    isOpenMenu.value=true
    data.value = props.chartData[props.selectedTube]
})




</script>
 

 
<style scoped>
.folders{
    /* padding-top: 20px; */
    /* box-sizing: border-box; */
    display: flex;
    flex-direction: column;
    font-weight: 400;
    font-size: 22px;
    max-width: 500px;
    /* margin-right: 20px; */
    height: 100vh;
    /* max-height:800px; */
    overflow-y:auto;
    overflow-x: auto;
    background: #42424Af7;
    padding-right: 10px;
    padding-top: 10px;
    box-shadow:  0px 6px 15px rgba(0, 0, 0, 0.32);
  
}
.folders_container_open{
    transform: translateX(0px);
    transition: all 0.3s ease-out;
    display: flex;
    flex-direction: row;

}
.folders_container_close{
    transform: translateX(-400px);
    transition: all 0.3s ease-out;
    display: flex;
    flex-direction: row;

}
.hamburger {
    position: relative;
    z-index: 1;
    /* height: 50px; */
    height: 35px;
    width: 30px;
    top: 45vh;
    
    /* margin: 100px auto; */
    padding-top: 5px;
    box-sizing: border-box;
    cursor: pointer;
}
.icon_container{
    height: 100vh;
    background: #42424Af7;
}

</style>