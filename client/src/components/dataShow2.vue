<template>
  <div class = "dataShowBar2_div">
    <div id = "main2_1" style = "width:800px; height:400px"></div>
		<div id = "main2_2" style = "width:800px; height:400px"></div>
		<div :style = "{'padding-left': '20px'}">
			<el-alert
				title = "如果需要更多可视化可以编写插件 :)"
				type = "info"
				effect = "dark">
			</el-alert>
		</div>
  </div>
</template>

<script>
export default {
  name: 'dataShowPage2',
  data() {
    return {
			data1: '',
			data2: '',
    }
  },
  methods: {
    createGroup(name_id, data) {
      var myChart = this.$echarts.init(document.getElementById(name_id));
			var option = {
				tooltip: {
					show: true
				},
				legend: {
					data: data['name']
				},
				xAxis: [{
					type: 'category',
					name: data['name'],
					data: data['data_x'],
					nameTextStyle: {
            color: '#FA6F53',
            fontSize: 16,
            padding: [0, 0, 0, 20]
          },
				}],
				yAxis: [{
					type: 'value',
					name: '数量',
					nameTextStyle: {
            color: '#FA6F53',
            fontSize: 16,
            padding: [0, 0, 0, 20]
          },
				}],
				series: [{
					"name": data['name'],
					"type": "bar",
					"data": data['data'],
					itemStyle: {
						normal: {
							label: {
								show: true,
								position: 'top',
								textStyle: {
									color: 'black',
									fontSize: 16
								}
							}
            }
					},
				}]
			};
			myChart.setOption(option);
    }
  },
  mounted() {
		this.$axios.get(this.$main_url + '/api/getVideoShowData')
		.then(response => {
			this.data1 = response.data['data1'];
			this.data2 = response.data['data2'];
			this.createGroup('main2_1', this.data1);
			this.createGroup('main2_2', this.data2);
    }).catch(error => {
      console.log(error);
    })
  },
  created() {
  }
}
</script>

<style>

</style>