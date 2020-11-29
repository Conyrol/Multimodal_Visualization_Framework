<template>
  <div class = "mainBar_div">
    <div class = "background">
      <img :src = "imgSrc" width = "100%" height = "100%" alt = "" />
    </div>
    <div class = "mainBar_stepBar">
      <el-steps direction = "vertical" :active = "step_now">
        <el-step title = "检查环境">
          <template slot = "description">
            <div class = "mainBar_stepBar_description">
              <el-alert
                title = "请检查环境..."
                type = "warning"
                effect = "dark"
                v-show = "environment_show">
              </el-alert>
              <div class = "environmentTable">
                <el-table :data = "table_data_environment" stripe v-show = "!environment_show">
                  <el-table-column
                    prop = "name"
                    label = "环境名"
                    width = "250">
                  </el-table-column>
                  <el-table-column
                    prop = "value"
                    label = "版本号"
                    width = "250">
                  </el-table-column>
                  <el-table-column
                    prop = "situation"
                    label = "环境情况"
                    width = "250">
                  </el-table-column>
                </el-table>
              </div>
              <el-button @click = "environmentCheck">开始检查</el-button>
            </div>
          </template>
        </el-step>
        <el-step title = "检查数据集">
          <template slot = "description">
            <div class = "mainBar_stepBar_description">  
              <el-alert
                title = "请检查环境..."
                type = "warning"
                effect = "dark"
                v-show = "dataset_show">
              </el-alert>
              <div class = "datasetTable">
                <el-table :data = "table_data_dataset" stripe v-show = "!dataset_show">
                  <el-table-column
                    prop = "name"
                    label = "数据集类型"
                    width = "300">
                  </el-table-column>
                  <el-table-column
                    prop = "value"
                    label = "数据集预存个数"
                    width = "300">
                  </el-table-column>
                </el-table>
              </div>
              <el-button @click = "dataCheck">开始检查</el-button>
            </div>
          </template>
        </el-step>
        <el-step title = "检查模型" description = "这是一段很长很长很长的描述性文字">
          <template slot = "description">
            <div class = "mainBar_stepBar_description">  
              <el-alert
                title = "请检查模型 (此过程会在后端加载预处理模型，需要花费一段时间)"
                type = "warning"
                effect = "dark"
                v-show = "model_show">
              </el-alert>
              <div class = "modelTable">
                <el-table :data = "table_data_model" stripe v-show = "!model_show">
                  <el-table-column
                    prop = "name"
                    label = "模型名称"
                    width = "300">
                  </el-table-column>
                  <el-table-column
                    prop = "value"
                    label = "模型状态"
                    width = "300">
                  </el-table-column>
                </el-table>
              </div>
              <el-button @click = "modelCheck">开始检查</el-button>
            </div>
          </template>
        </el-step>
      </el-steps>
    </div>
  </div>
</template>

<script>
export default {
  name: 'mainPage',
  data() {
    return {
      step_now: 0,
      environment_show: true,
      dataset_show: true,
      model_show: true,
      table_data_environment: [],
      table_data_dataset: [],
      table_data_model: [],
      imgSrc: require('../assets/1.jpg'),
    }
  },
  methods: {
    environmentCheck() {
      this.$axios({
        url: this.$main_url + '/api/checkEnvironment',
        method: 'get',
      }).then(response => {
        this.table_data_environment = [];
        for(let i in response.data) {
          this.table_data_environment.push({
            name: i,
            value: response.data[i][0],
            situation: response.data[i][1],
          })
        }
        this.environment_show = false;
        this.$cookies.set("environment_show", false, "0");
        this.step_now = 1;
      }).catch(error => {
        console.log(error);
      })
    },
    dataCheck() {
      this.$axios({
        url: this.$main_url + '/api/checkDataSet',
        method: 'get',
      }).then(response => {
        this.table_data_dataset = [];
        for(let i in response.data) {
          this.table_data_dataset.push({
            name: i,
            value: response.data[i],
          })
        }
        this.dataset_show = false;
        this.$cookies.set("dataset_show", false, "0");
        this.step_now = 2;
      }).catch(error => {
        console.log(error);
      })
    },
    modelCheck() {
      this.$axios({
        url: this.$main_url + '/api/checkModel',
        method: 'get',
      }).then(response => {
        this.table_data_model = [];
        for(let i in response.data) {
          this.table_data_model.push({
            name: i,
            value: response.data[i],
          })
        }
        this.model_show = false;
        this.$cookies.set("model_show", false, "0");
        this.step_now = 3;
      }).catch(error => {
        console.log(error);
      })
    }
  },
  created() {
    if(this.$cookies.get("environment_show")) this.environmentCheck();
    if(this.$cookies.get("dataset_show")) this.dataCheck();
    if(this.$cookies.get("model_show")) this.modelCheck();
  }
}
</script>

<style>
.background {
  width: 100%;  
  height: 100%;       /*  宽高100%是为了图片铺满屏幕  */
  z-index:-1;
  position: fixed;
}

.mainBar_stepBar {
  min-height: 90%;
  margin-top: 10px;
  margin-bottom: 10px;
  padding-left: 20px;
}

.mainBar_stepBar_description {
  margin: 10px;
}

.environmentTable {
  margin-top: 10px;
  margin-bottom: 10px;
  width: 750px;
}
.datasetTable, .modelTable{
  margin-top: 10px;
  margin-bottom: 10px;
  width: 600px;
}

.el-step__line {
  background-color: red !important;
}

.el-step__head.is-wait {
  color: #7c7c7c !important;
  border-color: #7c7c7c !important;
}

.is-wait {
  color: #585858 !important;
}
</style>