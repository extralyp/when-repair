<template>

    <!-- <label class="slidername"><slot name="header"></slot></label> -->
    <div class="slider_container">
      <table style="width: 100%;">
        <tr >

          <td>
            <label class="label_range_start" id="label_start"><slot name="left_label"></slot></label>

          </td>
          <td style="width: 100%; " >
            <span id='slider' class="slider">
              <output :id="idEl"  :class="idEl" for="distance" :value="sliderValue" class="range-slider-tooltip"></output>
              <input class="range-slider"  type="range" :max="maxValue" :min="minValue" :step="stepValue" v-model="sliderValue" :disabled="disabled">
    
            </span>
          </td>
          <td>
            <label class="label_range_end" id="label_end"><slot name="right_label"></slot></label>

          </td>
            
        </tr>
      </table>
    </div>
    
  

</template>

<script>
  export default {
    name:'my-rangeslider',
    props: {
            idEl: {
                type: String,
                required: true
            },
            disabled:{
              type: Boolean,
              required: false
            },
            minValue: {
                type: String,
                required: true
            },
            stepValue:{
              type: String,
              required: true
            },
            maxValue: {
                type: String,
                required: true
            },
            defaultValue: {
                type: [Number, String],
                required: true
            }
        },

    emits:['slider_value'],

    data(){
      
      return{
        
        sliderValue: this.defaultValue,
      }
    },
    watch: {
      'sliderValue': function() {
        let width_number = document.getElementById(this.idEl).offsetWidth
        let width_div_slider = document.getElementById('slider').offsetWidth
        let normalized = (Number(this.sliderValue) - Number(this.minValue)) / (Number(this.minValue) - Number(this.maxValue))
        let new_pos =  (width_div_slider) * normalized *(-1) - Number(width_number/2);
        const element = document.getElementById(this.idEl);
        element.style.left=new_pos + 'px'
        // эмитим значение слайдера чтобы передать в родителя
        this.$emit('slider_value', this.sliderValue)
      },
      'defaultValue': function() {
        this.sliderValue = this.defaultValue
      }
    },
    mounted() {

      {
        let width_number = document.getElementById(this.idEl).offsetWidth
        let width_div_slider = document.getElementById('slider').offsetWidth
        let normalized = (Number(this.sliderValue) - Number(this.minValue)) / (Number(this.minValue) - Number(this.maxValue))
        let new_pos =  (width_div_slider) * normalized * (-1) - Number(width_number/2);
        const element = document.getElementById(this.idEl);
        element.style.left=new_pos + 'px'
      }

    }  
    
  }

  
</script>

<style scoped>
.range-slider-tooltip {
  position: absolute;
  bottom: 15px;
  color: white;
  font-weight: 500;
  font-size: 18px;
}

.range-slider{
  width: 100% !important;
}

.slider{
  position: relative;
  width: 100%;
}

.slider_container{
  width: 100%;
  display: flex;
  justify-content: space-between;
}

.label_range_end{
  font-weight: 500;
  font-size: 18px;
  padding-left: 10px;
  color: white;
}
.label_range_start{
  font-weight: 500;
  font-size: 18px;
  padding-right: 10px;
  /* width: 70px; */
  color: white;

}

/*********** Baseline, reset styles ***********/
input[type="range"] {
  -webkit-appearance: none;
  appearance: none;
  background: transparent;
  cursor: pointer;
  width: 250px;

}

/* Removes default focus */
input[type="range"]:focus {
  outline: none;

}

/******** Chrome, Safari, Opera and Edge Chromium styles ********/
/* slider track */
input[type="range"]::-webkit-slider-runnable-track {
  background-color: #62636C;
  border-radius: 0.5rem;
  height: 0.5rem;
  filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));
  /* margin-left: 10px; */
  /* margin-right: 10px; */


}

/* slider thumb */
input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none; /* Override default look */
  appearance: none;
  margin-top: -4px; /* Centers thumb on the track */
  background-color: var(--primary-color);
  border-radius: 60px;
  height: 1rem;
  width: 1rem;
}

/* input[type="range"]:focus::-webkit-slider-thumb {
  outline: 3px solid #1cba68;
  outline-offset: 0.125rem;
} */

/*********** Firefox styles ***********/
/* slider track */
input[type="range"]::-moz-range-track {
  background-color: #62636C;
  border-radius: 60px;
  height: 0.5rem;
  filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));
}

/* slider thumb */
input[type="range"]::-moz-range-thumb {
  background-color: var(--primary-color);
  border: none; /*Removes extra border that FF applies*/
  border-radius: 60px;
  height: 385px;
  width: 7.39px;
}

input[type="range"]:focus::-moz-range-thumb{
  outline: 3px solid var(--primary-color);
  outline-offset: 0.125rem;
}


input[type=range]:disabled::-webkit-slider-thumb {
    /* Disabled slider-thumb */
    -webkit-appearance: none; /* Override default look */
  appearance: none;
  margin-top: -4px; /* Centers thumb on the track */
  background-color: gray;
  border-radius: 60px;
  height: 1rem;
  width: 1rem;
}

input[type=range]:disabled::-moz-range-thumb {
    /* Disabled slider-thumb */
  outline: 3px solid gray;
  outline-offset: 0.125rem;

}
</style>