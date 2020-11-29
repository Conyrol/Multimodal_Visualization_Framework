<template>
  <div class = "dataShowBar1_div">
    <div id = "main1_1" style = "width:800px; height:400px"></div>
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
  name: 'dataShowPage1',
  data() {
    return {
			data1: '',
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
            padding: [0, 0, 0, 10]
          },
				}],
				yAxis: [{
					type: 'value',
					name: '数量',
					nameTextStyle: {
            color: '#FA6F53',
            fontSize: 16,
            padding: [0, 0, 0, 10]
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
		this.$axios.get(this.$main_url + '/api/getTextShowData')
		.then(response => {
			this.data1 = response.data['data1'];
			this.createGroup('main1_1', this.data1);
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