<template>
  <div class = "dataAnalysisBar_div">
    <div class = "selectDiv flexDiv_row">
      <el-select v-model = "value" placeholder = "请选择模型" @change = "selectChange">
        <el-option
          v-for = "item in options"
          :key = "item.value"
          :label = "item.label"
          :value = "item.value">
        </el-option>
      </el-select>
      <el-alert
        :title = "returnTitle()"
        type = "warning"
        effect = "dark"
        :closable = "false">
      </el-alert>
    </div>
    <div v-show = "value == 1">
      <div id = "chartLineBox1_1" style = "width: 800px; height: 70vh;"> </div>
      <div id = "chartLineBox1_2" style = "width: 800px; height: 70vh;"> </div>
      <div id = "chartLineBox1_3" style = "width: 800px; height: 70vh;"> </div>
    </div>
    <div v-show = "value == 2">
      <div id = "chartLineBox2_1" style = "width: 800px; height: 70vh;"> </div>
      <div id = "chartLineBox2_2" style = "width: 800px; height: 70vh;"> </div>
      <div id = "chartLineBox2_3" style = "width: 800px; height: 70vh;"> </div>
    </div>
    <div v-show = "value == 3">
      <div id = "chartLineBox3_1" style = "width: 800px; height: 70vh;"> </div>
      <div id = "chartLineBox3_2" style = "width: 800px; height: 70vh;"> </div>
      <div id = "chartLineBox3_3" style = "width: 800px; height: 70vh;"> </div>
    </div>
    <div v-show = "value == 4">
      <div id = "chartLineBox4_1" style = "width: 800px; height: 70vh;"> </div>
      <div id = "chartLineBox4_2" style = "width: 800px; height: 70vh;"> </div>
      <div id = "chartLineBox4_3" style = "width: 800px; height: 70vh;"> </div>
    </div>
    <div v-show = "value == 5">
      <div id = "chartLineBox5_1" style = "width: 800px; height: 70vh;"> </div>
      <div id = "chartLineBox5_2" style = "width: 800px; height: 70vh;"> </div>
      <div id = "chartLineBox5_3" style = "width: 800px; height: 70vh;"> </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'dataAnalysisPage',
  components: { },
  data() {
    return {
      options: [
        {
          value: 1,
          label: 'TALL_C3D'
        }, {
          value: 2,
          label: 'MAC_C3D'
        }, {
          value: 3,
          label: 'A2C'
        }, {
          value: 4,
          label: 'TALL_I3D'
        }, {
          value: 5,
          label: 'MAC_I3D'
        }
      ],
      value: 1,
      data: '',
      data_5: '',
      data_7: '',
      now_model: '',
      over_list: [],
    }
  },
  methods: {
    returnTitle() {
      if(this.value == -1 || this.value == '') return "别忘记选择模型啊！";
      else {
        this.now_model = this.options[this.value - 1].label;
        return "你正在可视化 " + this.now_model;
      }
    },
    createGroup(id_name, data, start, end) {
      // 'chartLineBox1'
      let series = [];
      console.log(data['name']);
      for(let i in data['name']) {
        let data_y = [];
        for(let j in data['data_y']) {
          data_y.push(data['data_y'][j][data['name'][i]])
        }
        series.push({
          name: data['name'][i],
          data: data_y,
          type: 'line',
          lineStyle: {
            normal: {
              color: data['color'][i],
            }
          },
          markPoint: {
            symbolSize: 40,
            itemStyle:{
              color: '#4587E7',
              borderColor: '#000',
              borderWidth: 0,
              borderType: 'solid'
            },
            data: [{type: 'max', name: '最大值'}]
          },
          markLine: {
            data: [
              {type: 'average', name: '平均值'}
            ]
          }
        })
      }
      this.chartLine = this.$echarts.init(document.getElementById(id_name));
      var option = {
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: data['name'],
        },
        color: data['color'],
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: data['data_x'],
          name: data['name_x'],
          nameTextStyle: {
            color: '#FA6F53',
            fontSize: 16,
            padding: [0, 0, 0, 20]
          },
          axisLine: {
            lineStyle: {
              color: '#FA6F53',
            }
          }
        },
        yAxis: {
          name: data['name_y'],
          nameTextStyle: {
            color: '#FA6F53',
            fontSize: 16,
            padding: [0, 0, 10, 0]
          },
          axisLine: {
            lineStyle: {
              color: '#FA6F53',
            }
          },
          type: 'value'
        },
        series: series,
        dataZoom: {
          show: true,         // 为true 滚动条出现
          realtime: true,  
          type: 'slider',     // 有type这个属性，滚动条在最下面，也可以不行，写y：36，这表示距离顶端36px，一般就是在图上面。
          height: 30,         // 表示滚动条的高度，也就是粗细
          start: start,          // 表示默认展示20%～80%这一段。
          end: end
        }
      };
      this.chartLine.setOption(option);
    },
    selectChange() {
      for(let i in this.over_list) {
        if(this.over_list[i] == this.value) return;
      }
      this.$axios.get(this.$main_url + '/api/getAnalysisData', {
        params: {
          name: this.options[this.value - 1].label
        }
      }).then(response => {
        this.data = response.data['data'];
        this.data_5 = response.data['data_5'];
        this.data_7 = response.data['data_7'];
        if(this.value == 1) {
          this.createGroup('chartLineBox1_1', this.data, 20, 80);
          this.createGroup('chartLineBox1_2', this.data_5, 20, 80);
          this.createGroup('chartLineBox1_3', this.data_7, 20, 80);
        }
        if(this.value == 2) {
          this.createGroup('chartLineBox2_1', this.data, 20, 80);
          this.createGroup('chartLineBox2_2', this.data_5, 20, 80);
          this.createGroup('chartLineBox2_3', this.data_7, 20, 80);
        }
        if(this.value == 3) {
          this.createGroup('chartLineBox3_1', this.data, 20, 80);
          this.createGroup('chartLineBox3_2', this.data_5, 20, 80);
          this.createGroup('chartLineBox3_3', this.data_7, 20, 80);
        }
        if(this.value == 4) {
          this.createGroup('chartLineBox4_1', this.data, 20, 80);
          this.createGroup('chartLineBox4_2', this.data_5, 20, 80);
          this.createGroup('chartLineBox4_3', this.data_7, 20, 80);
        }
        if(this.value == 5) {
          this.createGroup('chartLineBox5_1', this.data, 20, 80);
          this.createGroup('chartLineBox5_2', this.data_5, 20, 80);
          this.createGroup('chartLineBox5_3', this.data_7, 20, 80);
        }
        this.over_list.push(this.value);
      }).catch(error => {
        console.log(error);
      })
    },
  },
  mounted() {
    this.$axios.get(this.$main_url + '/api/getAnalysisData', {
      params: {
        name: this.options[this.value - 1].label
      }
    }).then(response => {
      this.data = response.data['data'];
      this.data_5 = response.data['data_5'];
      this.data_7 = response.data['data_7'];
      if(this.value == 1) {
        this.createGroup('chartLineBox1_1', this.data, 20, 80);
        this.createGroup('chartLineBox1_2', this.data_5, 20, 80);
        this.createGroup('chartLineBox1_3', this.data_7, 20, 80);
      }
    }).catch(error => {
      console.log(error);
    })
  },
  created() {
    this.returnTitle()
  }
}
</script>

<style>
.dataAnalysisBar_div {
  width: 100%;
}
.selectDiv {
  margin: 20px;
  width: 100%;
}
</style>