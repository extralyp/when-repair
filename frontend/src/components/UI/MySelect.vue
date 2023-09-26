<template>
    <select class="select" id="select_object">
        <!-- <option class="options" disabled selected="selected" >Выберите объект</option> -->
        <slot></slot>
        
    </select>
</template>

<script>
    export default {
        name: "SoloSelect",
    }
</script>

<style scoped>
select {
    -webkit-appearance: none;
    -moz-appearance: none;
    -ms-appearance: none;
    appearance: none;
    outline: 0;
    box-shadow: none;
/* border: 1px dashed var(--primary-color); */

}
/* Remove IE arrow */
select::-ms-expand {
    display: none;
}
/* Custom Select */
.select {
    width: auto;
    height: 40px;
    padding: 5px;
    background-color:  #68696B;
    /* background:  #68696B; */
    color: var(--text-color-second);
    border-width: 0px;
    overflow: hidden;
    border-radius: 60px;
}
select {
    padding-left: 20px;
    justify-content: center;
    text-align: center;
    align-items: center;
    color: var(--text-color-second);
    cursor: pointer;
    font-family: 'Montserrat';
    font-style: normal;
    font-weight: 500;
    font-size: 18px;
}

</style>