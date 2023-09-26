<template>
    <div class="footer">
        <MySelect
            class="selector"
            style="background-color: var(--primary-color); font-size: 12px; height: 24px;"
            id="solo_select2"
        >
            <option selected="selected" value="mean_liq_exp">Беггз и Брилл</option>
            <option value="mean_oil_exp">Мукерджи и Брилл</option>
        </MySelect>

        <MySelect
            @change="selectedOption=$event.target.value"
            class="selector"
            style="background-color: var(--primary-color); font-size: 12px; height: 24px;"
            id="solo_select"
        >
            <option selected="selected" value="mean_liq_exp">Загрузка Qж, м3/сут</option>
            <option value="mean_oil_exp">Загрузка Qн, т/сут</option>
            <option value="mean_gas_exp">Загрузка Qг, м3/сут</option>
            <option value="mean_wat_exp">Загрузка Qв, м3/сут</option>
            <option value="mean_p">Давление, атм</option>
            <option value="mean_temp_exp">Температура, град.С</option>
            <option value="mode">Режим течения, 1-4</option>
            <option value="mean_speed">Скорость, м/сек</option>
            <option value="v_crit">Критическая скорость, м/сек</option>
            <option value="wear_perc">Износ, %</option>
            <option value="res_year">Ресурс, лет</option>
            <option value="stop_year">Пронозный год отказа (ML)</option>

        </MySelect>
        <MyRangeslider idEl="1"  @mouseup="changeOptSens(liqSliderValue)" @slider_value="(value) => liqSliderValue = value" :defaultValue="liqSliderValue" minValue="2014" stepValue="1" maxValue="2023" >
            <template v-slot:left_label>
                2014
            </template>  
            <template v-slot:right_label>
                2023
            </template>      
        </MyRangeslider>
        <div style="display: flex; column-gap: 5px;">
            <span class='legend-value'>
                <slot name="min_legend">
                </slot>
            </span>
            <hr  :class="{'gradient-legend-mode': (selectedOption=='mode'), 'gradient-legend': (selectedOption!=='mode')}">
            <span class='legend-value'>
                <slot name="max_legend">
                </slot>
            </span>
        </div>
        
    </div>
</template>
<script setup>
import { onMounted, ref, watch } from 'vue'
import MyRangeslider from '@/components/UI/MyRangeSlider.vue'
import MySelect from '@/components/UI/MySelect.vue'
import axios from 'axios'

const liqSliderValue = ref(2015)
const selectedOption = ref('mean_liq_exp')
const data = ref(null)

const emit = defineEmits(['colorsArray'])



function selectName(){
    emit('colorsArray',{data: data.value[selectedOption.value], option: selectedOption.value})
}

watch(()=>data.value, (oldValue, newValue) =>{
    selectName()
})

watch(()=>selectedOption.value, (oldValue, newValue) =>{
    selectName()
})

function changeOptSens(year){
    axios.post('/pipe_info/all_info_year', {'year': year})
    .then((response)=>{
        console.log(response)
        data.value = response.data

    })
}







onMounted(()=>{
    changeOptSens(liqSliderValue.value)
})


</script>
<style scoped>
.footer{
    display: flex;
    justify-content: space-between;
    background-color: transparent;
    column-gap: 20px;
    /* background: none; */
    background: #42424Af7;
    border-radius: 10px;
    padding: 15px;

}
.gradient-legend{
    width: 100px;
    height: 10px;
    background: linear-gradient(to left,red, green);
    border-radius: 10px;
    border: 0;
    margin-top: 9px;
}

.legend-value{
    margin-top: 3px;
    color: white;
    font-weight: 500;
    font-size: 18px;
}
.gradient-legend-mode{
    width: 100px;
    height: 10px;
    background: linear-gradient(to left,green, red);
    border-radius: 10px;
    border: 0;
    margin-top: 9px;
}
</style>

