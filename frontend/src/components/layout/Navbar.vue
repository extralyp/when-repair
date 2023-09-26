<template>
   <div class="navbar">
    <div class="tools">
        <router-link
                class="navbar__link"
                :class="{navbar__link__active: '/nestroplan' + link.href ==  activeEl}"
                v-for="link in links"
                :key="link.name"
                :to="link.href"
        >   
                {{ link.name }}
        </router-link>
    </div>
        
        <div class="underBar">
            <div class="path">
                <span class="label_verticalLine" v-if="selectDo"></span>
                <span class="label" v-if="selectDo"> {{selectDo}}/</span>
                <span class="label" v-if="selectField">{{selectField}}/</span>
                <span class="label" v-if="selectDo">{{selectUser}}/</span>
                <span class="label" v-if="selectPra">{{selectPra}}/</span>
                <span class="label" v-if="selectDo">{{selectScenario}}</span>
            </div>
        </div>
   </div>
   
</template>



<script setup>
import { mapGetters } from 'vuex';
import { ref } from 'vue'
const links = ref([
    {name:'Сценарии', href:"/scenario"},
    {name:'Добыча', href:"/debits"},
    {name:'Ограничения', href:"/limits"},
    {name:'Экономика', href:"/economic"},
    {name:'Сводка', href:"/svodka"},
]);

</script>

<script>
    export default {
        data(){
            return {
                activeEl:window.location.pathname,
            }
               
        },
        
        // изменяем activeEl при переходе по ссылке
        watch:{
            $route (to, from){
                this.activeEl = window.location.pathname;
                
            }
        },
        computed: {
            ...mapGetters({
                selectDo: "scenarioPath/stateDo",
                selectField: "scenarioPath/stateField",
                selectPra: "scenarioPath/statePra",
                selectUser: "scenarioPath/stateUser",
                selectScenario: "scenarioPath/stateScenario"

            })
        }, 
        

        
    }
</script>

<style scoped>
.navbar{
    margin: 0;
    
    padding: 0;
    height: 100px;
}
.label {
  font-size: 18px;
}
.tools{
    margin-left: 25px;
}
.label_verticalLine{
    /* border-left: 1px solid var(--primary-color); */
    height: 100%;
    margin-right: 8px;
}
.path{
    margin-left: 10px;
}
.folders{
    width: 15%;
    /* left: 30px; */
    display: flex;
    /* position: absolute; */
}
.navbar__link{
    position: relative;
    top: 11px;
    float:left;
    color: #B3B3B3;
    text-align: center;
    padding: 14px 16px;
    font-weight: 500;
    font-size: 18px;
    border-radius: 5px 15px 0 0;
    margin-left: 5px;
    background: linear-gradient(180deg, #46464A 0%, #68696B 100%);
    z-index: 0;
    /* transition: .3s ease all, z-index .00000000001s, background .00000000001s, top .00000000001s; */

}
/* .navbar__link:hover {
   
    border-top: solid 1px  var(--primary-color);
    border-left: solid 1px  var(--primary-color);
    border-right: solid 1px  var(--primary-color);
    border-radius: 5px 15px 0 0;
    padding-top: 16px;

} */

.navbar__link__active{
    position: relative;
    top:1px;
    font-size: 22px;
    font-weight: 600;
    border-top: solid 2px  var(--primary-color);
    border-left: solid 2px  var(--primary-color);
    border-right: solid 2px  var(--primary-color);
    border-radius: 5px 15px 0 0;
    color:var(--text-color-main);
    background: #42424A;
    z-index: 2;
    /* высота 62px фиксит скачки экрана при переключении */
    height: 55px;
    /* transition: .3s ease all, border-top .00000000001s,border-left .00000000001s,border-right .00000000001s, z-index .00000000001s, background .00000000001s ; */
}

.underBar{
    /* text-align: start; */
    font-weight: 500;
    font-size: 18px;
    padding-top: 5px;
    /* padding-bottom: 5px;  */
    height: 35px;
    padding-left: 20px;
    float:left;
    width: 100%;
    position: relative;
    bottom: 0.6px;
    z-index: 1;
    border-top: solid 2px  var(--primary-color);
    background: #42424A;
    box-shadow:  0px 6px 15px rgba(0, 0, 0, 0.32);
}

</style>