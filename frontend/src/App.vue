<template>
  <div class="app">
    <LayoutSidebar 
    class="sidebar"
    :selectedTube="selectedTube"
    :chartData="chartData"
    :selectOption="selectOption"
    >

    </LayoutSidebar>
    <div class="content" >
      <v-network-graph
        ref="graph"
        :nodes="data.nodes"
        :edges="edges"
        :layouts="data.layouts"
        :configs="configs"
        :layers="layers"
        :event-handlers="eventHandlers"        
      >
        <template #edge-label="{edge, ...slotProps}" >
          <VEdgeLabel 
            :text="edge.label" 
            align="center" 
            vertical-align="below" 
            v-bind="slotProps"
          />
          <VEdgeLabel 
            :text="edge.mean" 
            align="center" 
            vertical-align="center" 
            v-bind="slotProps"
            fill="#ffffff"
          />
          <v-edge-label
            :text="edge.min"
            align="source"
            vertical-align="center"
            v-bind="slotProps"
            fill="#ffffff"
          />
          <v-edge-label
            :text="edge.max"
            align="target"
            vertical-align="center"
            v-bind="slotProps"
            fill="#ffffff"
          />
        </template>
        <!-- Additional layer -->
        <template #worldmap>
          <image
            href='@/assets/img/World_location_map2.svg'
            x="0"
            y="0"
            width="1000px"
            @load="onLoadImage"
          />
        </template>
    

    <!-- Replace the node component -->
    <template #override-node="{ nodeId, scale, config, ...slotProps }">
      <!-- circle for filling background -->
      <circle
        class="face-circle"
        :r="config.radius * scale * 1.5"
        fill="#ffffff"
        stroke='#15923D'
        stroke-width='0.05'
        v-bind="slotProps"
      />
      <!--
        The base position of the <image /> is top left. The node's
        center should be (0,0), so slide it by specifying x and y.
      -->
      <image
        class="face-picture"
        :x="-config.radius * scale"
        :y="-config.radius * scale"
        :width="config.radius * scale * 2"
        :height="config.radius * scale * 2"
        href='@/assets/img/oil-platform.svg'
        clip-path="url(#faceCircle)"
      />
    </template>
        
      </v-network-graph>
      <!-- Tooltip -->
      <div
        ref="tooltip"
        class="tooltip"
        :style="{ ...tooltipPos, opacity: tooltipOpacity }"
      >
        <div>{{ data.nodes[targetNodeId]?.name ?? "" }}</div>

      </div>
    </div>
    <div style="position: absolute; top: 1000px; left: 30%; width: 45%;">
      <LayoutFooter
        @colorsArray="addGradient"
      >
      <template v-slot:min_legend>
        {{leftLabel}}
      </template>
      <template v-slot:max_legend>
        {{rightLabel}}
      </template>
      </LayoutFooter>
    </div>
  </div>
  
</template>

<script setup>
import { VEdgeLabel, VNetworkGraph } from 'v-network-graph';
import { defineConfigs } from "v-network-graph"
import LayoutFooter from '@/components/layout/Footer-layout.vue'
import LayoutSidebar from '@/components/layout/Sidebar-layout.vue'
import { ref, computed, watch, nextTick  } from "vue"
import data from "@/assets/data/data.js"
import axios from 'axios'


// additional layers definition
const layers = {
  // {layername}: {position}
  worldmap: "base",
}

// ref="graph"
const graph = ref(null)
const edges = ref({
  'D8-D4': { source: "D8", target: "D4", label: 'D8-D4', color:'black' , min:null, mean:null, max:null },
  'D4-C3/E': { source: "D4", target: "C3/E", label: 'D4-C3/E', color:'black', min:null, mean:null, max:null },
  'C3/E-X4': { source: "C3/E", target: "X4", label: 'C3/E-X4' , color:'black', min:null, mean:null, max:null },
  'C3/E-C2/E': { source: "C3/E", target: "C2/E", label: 'C3/E-C2/E' , color:'black', min:null, mean:null, max:null },
  'H7/D14-C3/E': { source: "C3/E", target: "H7/D14", label: 'H7/D14-C3/E' , color:'black', min:null, mean:null, max:null },
  'H7/D14-D9': { source: "H7/D14", target: "D9", label: 'H7/D14-D9' , color:'black', min:null, mean:null, max:null },
  'D9-C3': { source: "D9", target: "C3", label: 'D9-C3' , color:'black', min:null, mean:null, max:null },
  'D20-C3': { source: "C3", target: "D20" , label: 'D20-C3', color:'black', min:null, mean:null, max:null },
  'D6-C3': { source: "C3", target: "D6" , label: 'D6-C3', color:'black', min:null, mean:null, max:null },
  'D6-C2/D2': { source: "D6", target: "C2/D2", label: 'D6-C2/D2', color:'black', min:null, mean:null, max:null },
  'D1/10-C2/D2': { source: "C2/D2", target: "D1/10", label: 'D1/10-C2/D2', color:'black', min:null, mean:null, max:null },
  'D5-C2/D2': { source: "C2/D2", target: "D5", label: 'D5-C2/D2', color:'black', min:null, mean:null, max:null },
  'C2/D2-I3/E': { source: "C2/D2", target: "I3/E", label: 'C2/D2-I3/E', color:'black', min:null, mean:null, max:null },
  'G1-C2/D2': { source: "C2/D2", target: "G1", label: 'G1-C2/D2', color:'black', min:null, mean:null, max:null },
  'C2/D2-G1': { source: "G1", target: "C2D2" , color:'black', min:null, mean:null, max:null },
  'D3-D2': { source: "D3", target: "D2", label: 'D3-D2', color:'black', min:null, mean:null, max:null },
  'D3-G1': { source: "D3", target: "G1", label: 'D3-G1', color:'black', min:null, mean:null, max:null },
  'D2-D3': { source: "D2", target: "D3", color:'black', min:null, mean:null, max:null },
  'G9-D3': { source: "D3", target: "G9", label: 'G9-D3', color:'black', min:null, mean:null, max:null },
  'G8-G9': { source: "G9", target: "G8", label: 'G8-G9', color:'black', min:null, mean:null, max:null },
  'G8-G1': { source: "G8", target: "G1", label: 'G8-G1', color:'black', min:null, mean:null, max:null },
  'G1-G8': { source: "G1", target: "G8", color:'black', min:null, mean:null, max:null },
  'Y2-G8': { source: "G8", target: "Y2", label: 'Y2-G8', color:'black', min:null, mean:null, max:null },
  'G10-G9': { source: "G9", target: "G10", label: 'G10-G9', color:'black', min:null, mean:null, max:null },
  'G10-G5': { source: "G10", target: "G5", label: 'G10-G5', color:'black', min:null, mean:null, max:null },
  'G4-G8': { source: "G4", target: "G8", label: 'G4-G8', color:'black', min:null, mean:null, max:null },
  'D15-G10': { source: "G10", target: "D15", label: 'D15-G10', color:'black', min:null, mean:null, max:null },
  'G7-G5': { source: "G5", target: "G7", label: 'G7-G5', color:'black', min:null, mean:null, max:null },
  'G5-G3': { source: "G5", target: "G3", label: 'G5-G3', color:'black', min:null, mean:null, max:null },
  'G3-G4': { source: "G3", target: "G4", label: 'G3-G4', color:'black', min:null, mean:null, max:null },
  'G4-G9': { source: "G4", target: "G9", label: 'G4-G9', color:'black', min:null, mean:null, max:null },
  'G6-G4': { source: "G4", target: "G6", label: 'G6-G4', color:'black', min:null, mean:null, max:null },
  'Y1-G6': { source: "G6", target: "Y1", label: 'Y1-G6', color:'black', min:null, mean:null, max:null },
  'K-G-6': { source: "G6", target: "K", label: 'K-G6', color:'black', min:null, mean:null, max:null },
  'D19-K': { source: "K", target: "D19", label: 'D19-K', color:'black', min:null, mean:null, max:null },
  'D21-K': { source: "K", target: "D21", label: 'D21-K', color:'black', min:null, mean:null, max:null },
  'F1-D14': { source: "F1", target: "D14", label: 'F1-D14', color:'black', min:null, mean:null, max:null },
  'D16-D14': { source: "D14", target: "D16", label: 'D16-D14', color:'black', min:null, mean:null, max:null },
  'A-B4': { source: "A", target: "B4", label: 'A-B4', color:'black', min:null, mean:null, max:null },
  'B4-B5': { source: "B4", target: "B5", label: 'B4-B5', color:'black', min:null, mean:null, max:null },
  'B5-J1': { source: "B5", target: "J1", label: 'B5-J1', color:'black', min:null, mean:null, max:null },
  'B6-J1': { source: "J1", target: "B6", label: 'B6-J1', color:'black', min:null, mean:null, max:null },
  'J1-KX6': { source: "J1", target: "KX6", label: 'J1-KX6', color:'black', min:null, mean:null, max:null },
  'J1-KX3': { source: "J1", target: "KX3", label: 'J1-KX3', color:'black', min:null, mean:null, max:null },
  'Z1-J2': { source: "Z1", target: "J2", label: 'Z1-J2', color:'black', min:null, mean:null, max:null },
  'J2-KX3/X6': { source: "J2", target: "KX3/X6", label: 'J2-KX3/X6', color:'black', min:null, mean:null, max:null },
  'B3-J2': { source: "J2", target: "B3", label: 'B3-J2', color:'black', min:null, mean:null, max:null },
  'J3-J2': { source: "J3", target: "J2", label: 'J3-J2', color:'black', min:null, mean:null, max:null },
})

const edgesDefault = {
  'D8-D4': { source: "D8", target: "D4", label: 'D8-D4', color:'black' , min:null, mean:null, max:null },
  'D4-C3/E': { source: "D4", target: "C3/E", label: 'D4-C3/E', color:'black', min:null, mean:null, max:null },
  'C3/E-X4': { source: "C3/E", target: "X4", label: 'C3/E-X4' , color:'black', min:null, mean:null, max:null },
  'C3/E-C2/E': { source: "C3/E", target: "C2/E", label: 'C3/E-C2/E' , color:'black', min:null, mean:null, max:null },
  'H7/D14-C3/E': { source: "C3/E", target: "H7/D14", label: 'H7/D14-C3/E' , color:'black', min:null, mean:null, max:null },
  'H7/D14-D9': { source: "H7/D14", target: "D9", label: 'H7/D14-D9' , color:'black', min:null, mean:null, max:null },
  'D9-C3': { source: "D9", target: "C3", label: 'D9-C3' , color:'black', min:null, mean:null, max:null },
  'D20-C3': { source: "C3", target: "D20" , label: 'D20-C3', color:'black', min:null, mean:null, max:null },
  'D6-C3': { source: "C3", target: "D6" , label: 'D6-C3', color:'black', min:null, mean:null, max:null },
  'D6-C2/D2': { source: "D6", target: "C2/D2", label: 'D6-C2/D2', color:'black', min:null, mean:null, max:null },
  'D1/10-C2/D2': { source: "C2/D2", target: "D1/10", label: 'D1/10-C2/D2', color:'black', min:null, mean:null, max:null },
  'D5-C2/D2': { source: "C2/D2", target: "D5", label: 'D5-C2/D2', color:'black', min:null, mean:null, max:null },
  'C2/D2-I3/E': { source: "C2/D2", target: "I3/E", label: 'C2/D2-I3/E', color:'black', min:null, mean:null, max:null },
  'G1-C2/D2': { source: "C2/D2", target: "G1", label: 'G1-C2/D2', color:'black', min:null, mean:null, max:null },
  'C2/D2-G1': { source: "G1", target: "C2D2" , color:'black', min:null, mean:null, max:null },
  'D3-D2': { source: "D3", target: "D2", label: 'D3-D2', color:'black', min:null, mean:null, max:null },
  'D3-G1': { source: "D3", target: "G1", label: 'D3-G1', color:'black', min:null, mean:null, max:null },
  'D2-D3': { source: "D2", target: "D3", color:'black', min:null, mean:null, max:null },
  'G9-D3': { source: "D3", target: "G9", label: 'G9-D3', color:'black', min:null, mean:null, max:null },
  'G8-G9': { source: "G9", target: "G8", label: 'G8-G9', color:'black', min:null, mean:null, max:null },
  'G8-G1': { source: "G8", target: "G1", label: 'G8-G1', color:'black', min:null, mean:null, max:null },
  'G1-G8': { source: "G1", target: "G8", color:'black', min:null, mean:null, max:null },
  'Y2-G8': { source: "G8", target: "Y2", label: 'Y2-G8', color:'black', min:null, mean:null, max:null },
  'G10-G9': { source: "G9", target: "G10", label: 'G10-G9', color:'black', min:null, mean:null, max:null },
  'G10-G5': { source: "G10", target: "G5", label: 'G10-G5', color:'black', min:null, mean:null, max:null },
  'G4-G8': { source: "G4", target: "G8", label: 'G4-G8', color:'black', min:null, mean:null, max:null },
  'D15-G10': { source: "G10", target: "D15", label: 'D15-G10', color:'black', min:null, mean:null, max:null },
  'G7-G5': { source: "G5", target: "G7", label: 'G7-G5', color:'black', min:null, mean:null, max:null },
  'G5-G3': { source: "G5", target: "G3", label: 'G5-G3', color:'black', min:null, mean:null, max:null },
  'G3-G4': { source: "G3", target: "G4", label: 'G3-G4', color:'black', min:null, mean:null, max:null },
  'G4-G9': { source: "G4", target: "G9", label: 'G4-G9', color:'black', min:null, mean:null, max:null },
  'G6-G4': { source: "G4", target: "G6", label: 'G6-G4', color:'black', min:null, mean:null, max:null },
  'Y1-G6': { source: "G6", target: "Y1", label: 'Y1-G6', color:'black', min:null, mean:null, max:null },
  'K-G-6': { source: "G6", target: "K", label: 'K-G6', color:'black', min:null, mean:null, max:null },
  'D19-K': { source: "K", target: "D19", label: 'D19-K', color:'black', min:null, mean:null, max:null },
  'D21-K': { source: "K", target: "D21", label: 'D21-K', color:'black', min:null, mean:null, max:null },
  'F1-D14': { source: "F1", target: "D14", label: 'F1-D14', color:'black', min:null, mean:null, max:null },
  'D16-D14': { source: "D14", target: "D16", label: 'D16-D14', color:'black', min:null, mean:null, max:null },
  'A-B4': { source: "A", target: "B4", label: 'A-B4', color:'black', min:null, mean:null, max:null },
  'B4-B5': { source: "B4", target: "B5", label: 'B4-B5', color:'black', min:null, mean:null, max:null },
  'B5-J1': { source: "B5", target: "J1", label: 'B5-J1', color:'black', min:null, mean:null, max:null },
  'B6-J1': { source: "J1", target: "B6", label: 'B6-J1', color:'black', min:null, mean:null, max:null },
  'J1-KX6': { source: "J1", target: "KX6", label: 'J1-KX6', color:'black', min:null, mean:null, max:null },
  'J1-KX3': { source: "J1", target: "KX3", label: 'J1-KX3', color:'black', min:null, mean:null, max:null },
  'Z1-J2': { source: "Z1", target: "J2", label: 'Z1-J2', color:'black', min:null, mean:null, max:null },
  'J2-KX3/X6': { source: "J2", target: "KX3/X6", label: 'J2-KX3/X6', color:'black', min:null, mean:null, max:null },
  'B3-J2': { source: "J2", target: "B3", label: 'B3-J2', color:'black', min:null, mean:null, max:null },
  'J3-J2': { source: "J3", target: "J2", label: 'J3-J2', color:'black', min:null, mean:null, max:null },
}
const leftLabel = ref(0)
const rightLabel = ref(100)
const chartData = ref(null)
const selectOption = ref(null)
const renderComponent = ref(true)
const dataGlobal = ref(null)



const configs = defineConfigs({
  view:{
    minZoomLevel: 3,
    maxZoomLevel: 45,
    autoPanAndZoomOnLoad:  "fit-content"

  },
  node: {
    normal: {
      type: "rect",
      radius: 12,
      color: "#15923D",
    },
    hover:{
      color: "#15923D",
    },
    label: {
      visible: true,
      direction: "south",
      directionAutoAdjustment: true,
    },
  },
  edge:{
    selectable: true,
    normal:{
      color: e => e.color,
      width: 13
    },
    hover:{
      color: e => e.color
    },
    label:{
      fontSize: 12,
      background:{
        visible: false
      }
    }
  }
})

const forceRerender = async () => {
   // Remove MyComponent from the DOM
   renderComponent.value = false;
  // Wait for the change to get flushed to the DOM
  await nextTick();
  // Add the component back in
  renderComponent.value = true;
}



function addGradient({ data, option }) {
  dataGlobal.value = data
  selectOption.value = option
  // if (option=='res_year'){
  //     axios.post('/pipe_info/life_pipe')
  //     .then((response)=>{
  //       dataGlobal.value = response.data.year_life
  //       console.log('dddddd', dataGlobal.value)
  //     })
  // }
  // console.log('dddddd', dataGlobal.value)
  const tubeKeys = Object.keys(dataGlobal.value.gradient)
  const allKeys = Object.keys(edges.value)
  chartData.value = dataGlobal.value.chart
  leftLabel.value=(dataGlobal.value.min_grad)?.toFixed(0)
  rightLabel.value=(dataGlobal.value.max_grad)?.toFixed(0)
  let round 
  if (option=='v_crit' || option=='mean_speed'){
    round = 1
  }else{
    round = 0
  }

  Object.values(allKeys).forEach(tube => {
    edges.value[`${tube.split(" ").join("")}`].color = 'black'
    edges.value[`${tube.split(" ").join("")}`].mean = null
    edges.value[`${tube.split(" ").join("")}`].min = null
    edges.value[`${tube.split(" ").join("")}`].max = null
    edges.value[`${tube.split(" ").join("")}`].chart = null

  })

  Object.values(tubeKeys).forEach(tube => {
    edges.value[`${tube.split(" ").join("")}`].color = dataGlobal.value?.gradient[`${tube.split(" ").join("")}`]
    edges.value[`${tube.split(" ").join("")}`].mean = (dataGlobal.value?.mean_stats[`${tube.split(" ").join("")}`])?.toFixed(round)
    if (option=='mode' || option=='v_crit'){
      edges.value[`${tube.split(" ").join("")}`].min = null
      edges.value[`${tube.split(" ").join("")}`].max = null
      edges.value[`${tube.split(" ").join("")}`].chart = null
    }else{
      edges.value[`${tube.split(" ").join("")}`].min = (dataGlobal.value?.min_stats[`${tube.split(" ").join("")}`])?.toFixed(round)
      edges.value[`${tube.split(" ").join("")}`].max = (dataGlobal.value?.max_stats[`${tube.split(" ").join("")}`])?.toFixed(round)
    }
  })
  
}

function onLoadImage() {
  graph.value?.fitToContents()
}

// ref="tooltip"
const tooltip = ref()

// positions of the center of nodes
const layouts = ref(data.layouts)
const NODE_RADIUS = 16
const targetNodeId = ref("")
const selectedTube = ref("")
const tooltipOpacity = ref(0) // 0 or 1
const tooltipPos = ref({ left: "0px", top: "0px" })

const targetNodePos = computed(() => {
  const nodePos = layouts.value.nodes[targetNodeId.value]
  return nodePos || { x: 0, y: 0 }
})

// Update `tooltipPos`
watch(
  () => [targetNodePos.value, tooltipOpacity.value],
  () => {
    if (!graph.value || !tooltip.value) return

    // translate coordinates: SVG -> DOM
    const domPoint = graph.value.translateFromSvgToDomCoordinates(targetNodePos.value)
    // calculates top-left position of the tooltip.
    tooltipPos.value = {
      left: domPoint.x - tooltip.value.offsetWidth / 2 + "px",
      top: domPoint.y - NODE_RADIUS - tooltip.value.offsetHeight - 10 + "px",
    }
  },
  { deep: true }
)

const eventHandlers = {
  "node:pointerover": ({ node }) => {
    targetNodeId.value = node
    tooltipOpacity.value = 1 // show
  },
  "node:pointerout": _ => {
    tooltipOpacity.value = 0 // hide
  },
  "edge:click": ({ edge }) => {
    if (selectOption.value!=='mode' && selectOption.value!=='v_crit' && selectOption.value!=='v_crit'){
      selectedTube.value = edge
    }
  },
}



</script>

<style scoped>
.app {
  font-family: "Montserrat";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--text-color-main);
  background: linear-gradient(180deg, #53565A 0%, #4C525A 100%);
  /* zoom: 80%; */
  /* min-height: 99vh; */
  overflow-x: hidden;
  overflow-y: hidden;

}

.content{
  width: 100%;
  height: 100vh;
  overflow-x: hidden;
  overflow-y: hidden;

  /* position: relative; */
}
.sidebar{
  position: absolute;
  z-index: 1;

}

.tooltip {
  top: 0;
  left: 0;
  opacity: 0;
  position: absolute;
  padding: 5px;
  width: auto;
  height: 20px;
  display: grid;
  place-content: center;
  text-align: center;
  font-size: 10px;
  background-color: var(--primary-color);
  /* border: 1px solid #09e709; */
  border-radius: 10px;
  transition: opacity 0.2s linear;
  pointer-events: none;
}
</style>