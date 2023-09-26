<template>
    <!-- <my-dialog v-model:show="dialogVisible" >
        <apexchart type="line" height="700px" width="1200px" :options="chartOptions" :series="chartData"></apexchart>
    </my-dialog> -->
    <apexchart  @dblclick="showZoomChart" type="line" height="100%" width="100%" :options="chartOptions" :series="chartData"></apexchart>  

</template>

<script setup>
import {ref, onBeforeUpdate, onBeforeMount, watch} from "vue"

const chartOptions = ref({
                    chart: {
                        animations: {
                            enabled: true,
                        },
                        id: 'fb1',
                        group: 'social',
                        zoom:{
                            autoScaleYaxis: true,
                        },
                        type: 'line',
                        background: 'rgba(66, 66, 66, 0.27)',
                        fontFamily: 'Montserrat',
                        locales: [{
                        "name": "ru",
                        "options": {
                            "months": ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июнь", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
                            "shortMonths": ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июнь", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
                            "days": ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Субота"],
                            "shortDays": ["Вс.", "Пн.", "Вт.", "Ср.", "Чт.", "Пт.", "Сб."],
                            "toolbar": {
                                "exportToSVG": "Скачать SVG",
                                "exportToPNG": "Скачать PNG",
                                "exportToCSV": "Скачать CSV",
                                "menu": "Меню",
                                "selection": "Выбрать",
                                "selectionZoom": "Выбрать Zoom",
                                "zoomIn": "Приблизить",
                                "zoomOut": "Отдалить",
                                "pan": "Перетащить",
                                "reset": "Сбросить масштаб"
                            }
                        }
                        }],
                        defaultLocale: "ru",
                        dropShadow: {
                            enabled: true,
                            enabledOnSeries: undefined,
                            top: 2,
                            left: 2,
                            blur: 3,
                            color: 'black',
                            opacity: 0.35
                        }
                    },
                    stroke: {
                        show: true,
                        curve: 'smooth',
                        colors: undefined,
                        width: 3,
                    },
                    legend: {
                        show: true,
                        fontSize: '14px',
                        labels: {
                            colors: 'var(--text-color-second)',
                            useSeriesColors: false
                        }
                    },
                    grid: {
                        show: true,
                        borderColor: 'red',
                        strokeDashArray: 2,
                        position: 'back',
                        xaxis: {
                            lines: {
                                show: false
                            }
                        },   
                        yaxis: {
                            lines: {
                                show: false
                            },
            
                    }
                    },   
                    yaxis: {
                        
                        axisTicks: {
                            show: true,
                            borderType: 'solid',
                            color: 'var(--text-color-second)',
                            height: 6,
                            offsetX: 1,
                            offsetY: 0
                        },
                        // округляем ось Y
                        labels: {
                            formatter: function (val) {
                                return (val)?.toFixed(1)
                            },
                            style:{
                                colors: 'var(--text-color-second)',
                                fontSize:'14px',
                                fontWeight: 400,
                            }
                        },
                        // делаем черту по оси Y
                        crosshairs: {
                            show: false,
                            stroke: {
                                color: 'var(--text-color-second)',
                                width: 1,
                                dashArray: 6,
                            },
                        },
                        tooltip: {
                            enabled: false
                        },
                        // название оси
                        title:{
                            text: "Параметр",
                            offsetY: 0,
                            style:{
                                color: 'var(--text-color-second)',
                                fontSize:'14px',
                                fontWeight: 600,
                            }
                        },
                        axisBorder: {
                            show: true,
                            color: 'var(--text-color-second)',
                            height: 0,
                            width: '1px',
                            offsetX: -1,
                            offsetY: 0
                        },
                    }, 
                    xaxis: {     
                        min:150,                   
                        type: 'numeric',
                        axisTicks: {
                            show: true,
                            borderType: 'solid',
                            color: 'var(--text-color-second)',
                            height: 6,
                            offsetX: 0,
                            offsetY: 0
                        },
                        labels: {
                            style:{
                                colors: 'var(--text-color-second)',
                                fontSize:'14px',
                                fontWeight: 400,
                            }
                        },
                        crosshairs: {
                            show: true,
                            stroke: {
                                color: 'var(--text-color-second)',
                                width: 1,
                                dashArray: 6,
                            },
                            
                        },
                        labels: {
                            style:{
                                colors: 'var(--text-color-second)',
                                fontSize:'14px',
                                fontWeight: 400,
                            }
                        },
                        // название оси
                        title:{
                            style:{
                                color: 'var(--text-color-second)'
                            }
                        },
                        axisBorder: {
                            show: true,
                            color: 'var(--text-color-second)',
                            offsetX: 0,
                            offsetY: 0
                        },
                    },
                    // вывод аннотации 
                    tooltip: {
                        theme: 'dark',
                        // измененние формата вывода в аннотации по оси Х 
             
                    },
                    colors: ['var(--chart-oil-color)']
                })
const dialogVisible = ref(false)
const props = defineProps({

            data: {
                type: Object,
                required: true
                }
            })
const chartData = ref(
                        [
                            {
                                name: 'Параметр',
                                data: []
                            },
                        ]
                    )
const showZoomChart = () => {
    dialogVisible.value=true
    chartOptions.value.chart.group = ''
    chartOptions.value.chart.id = ''
}

watch(()=>{
    console.log(chartData.value)
    console.log(props.data)
    chartData.value[0].data=[]
    chartData.value[0].data=props.data
})

onBeforeMount(()=>{
    console.log(chartData.value)
    console.log(props.data)
    chartData.value[0].data=[]
    chartData.value[0].data=props.data
})


</script>

<style scoped>

</style>