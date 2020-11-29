<template>
  <div id = "app" class = "flexDiv_row3" :style = "{'min-height': '100%'}">
    <div class = "leftSide_bar">
      <el-menu default-active = "1-4-1" class = "el-menu-vertical-demo"
        :collapse = "isCollapse"
        background-color = "#545c64"
        text-color = "#fff"
        active-text-color = "#ffd04b">
        <el-menu-item index = "1" @click = "showChange(1)">
          <i class = "el-icon-s-home"></i>
          <span slot = "title"> 主页</span>
        </el-menu-item>
        <el-submenu index = "2">
          <template slot = "title">
            <i class = "el-icon-menu"></i>
            <span slot = "title"> 基础数据</span>
          </template>
          <el-menu-item-group>
            <template slot = "title">
              <div class = "el-menu-item-group__title_change">
                <i class = "el-icon-s-order"></i>
                <span slot = "title" @click = "showChange(2)"> 文本数据</span>
              </div>
            </template>
            <el-menu-item index = "1-1" @click = "showChange(2)"> 检查文本</el-menu-item>
          </el-menu-item-group>
          <el-menu-item-group>
            <template slot = "title">
              <div class = "el-menu-item-group__title_change">
                <i class = "el-icon-video-play"></i>
                <span slot = "title" @click = "showChange(6)"> 视频数据</span>
              </div>
            </template>
            <el-menu-item index = "1-3" @click = "showChange(6)"> 检查视频</el-menu-item>
          </el-menu-item-group>
        </el-submenu>
        <el-menu-item index = "3" @click = "showChange(3)">
          <i class = "el-icon-s-data"></i>
          <span slot = "title"> 数据分析</span>
        </el-menu-item>
        <el-menu-item index = "4" @click = "showChange(4)">
          <i class = "el-icon-film"></i>
          <span slot = "title"> 结果可视化</span>
        </el-menu-item>
        <el-menu-item index = "5" @click = "showChange(5)">
          <i class = "el-icon-data-analysis"></i>
          <span slot = "title"> 性能分析</span>
        </el-menu-item>
      </el-menu>
    </div>
    <mainBar v-show = "showList[1]"></mainBar>
    <dataShowBar1 v-show = "showList[2]"></dataShowBar1>
    <dataShowBar2 v-show = "showList[6]"></dataShowBar2>
    <dataAnalysisBar v-show = "showList[3]"></dataAnalysisBar>
    <videoBar v-show = "showList[4]"></videoBar>
  </div>
</template>

<script>
import mainBar from './components/mainBar.vue'
import dataShowBar1 from './components/dataShow1.vue'
import dataShowBar2 from './components/dataShow2.vue'
import dataAnalysisBar from './components/dataAnalysisBar.vue'
import videoBar from './components/videoBar.vue'
export default {
  name: 'App',
  components: {
    mainBar, dataAnalysisBar, videoBar, dataShowBar1, dataShowBar2
  },
  data() {
    return {
      isCollapse: true,
      showList: {
        1: true,
        2: false,
        3: false,
        4: false,
        5: false,
        6: false,
      },
    }
  },
  methods: {
    showChange(index) {
      console.log(index);
      for(let i in this.showList)
        if(this.showList[i]) this.showList[i] = false;
      this.showList[index] = true;
      this.$cookies.set("show_value", index, "0");
    }
  },
  created() {
    let show_value = this.$cookies.get("show_value");
    console.log(show_value);
    if(show_value) {
      for(let i in this.showList) this.showList[i] = false;
      this.showList[show_value] = true;
    }
  }
}
</script>

<style>
@import "./assets/base.css";

html, body{
  margin: 0;
  padding: 0;
  height: 100%;
}

.leftSide_bar {
  display: flex;
  min-height: 100%;
}

.el-menu-item-group__title_change {
  padding: 5px 0;
  font-size: 14px;
  color: #bebebe;
  font-weight: bold;
}

.el-menu-item-group .el-menu-item {
  font-size: 12px !important;
  height: 40px !important;
  line-height: 40px !important;
}

.mainBar_div {
  width: 100%;
  min-height: 100%;
}
</style>
