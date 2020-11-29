<template>
  <div class = "videoBar_div">
    <div class = "background">
      <img :src = "imgSrc" width = "100%" height = "100%" alt = "" />
    </div>
    <div class = "flexDiv_col_withoutHeight left_botton_list">
      <el-button style = "display: none"></el-button>
      <el-tooltip content = "上传视频文件" effect = "light" placement = "right">
        <el-button circle icon = "el-icon-upload2" @click = "clickLoad"></el-button>
      </el-tooltip>
      <el-tooltip content = "查看视频集" effect = "light" placement = "right">
        <el-button circle icon = "el-icon-plus" @click = "drawer = !drawer"></el-button>
      </el-tooltip>
      <el-tooltip content = "提交数据" effect = "light" placement = "right">
        <el-button circle icon = "el-icon-plus" @click = "drawer2 = !drawer2"></el-button>
      </el-tooltip>
    </div>
    <div class = "selectDiv flexDiv_row">
      <el-select v-model = "value" placeholder = "请选择模型">
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
    <input type = "file" id = "files" :style = "{'display': 'none'}" ref = "refFile" v-on:change = "fileLoad">
    <div class = "flexDiv_row" :style = "{'width': '100%'}">
      <div class = "flexDiv_col" :style = "{'width': '50%'}">
          <video-player class = "video-player vjs-custom-skin"
            ref = "videoPlayer"
            :playsinline = "true"
            :options = "playerOptions">
          </video-player>
          <div :style = "{'padding-top': '3px'}" v-show = "this.return_list.length == 0">
            <el-alert
              title = "这里还没有任何结果 :("
              type = "error"
              effect = "dark"
              :closable = "false">
            </el-alert>
          </div>
          <el-collapse>
            <el-collapse-item v-for = "(i, index) in return_list" :key = "index">
              <template slot = "title">
                <div class = "collapse_title_text">
                  <i class="header-icon el-icon-info"></i> Top {{index}}
                </div>
              </template>
              <div class = "flexDiv_col">
                <el-alert
                  title = "预测区间"
                  type = "info"
                  :description = "Math.round(i[0]/30*10)/10 + ' s - ' + Math.round(i[1]/30*10)/10 + ' s'"
                  show-icon>
                </el-alert>
                <div class = "flexDiv_row">
                  <div :style = "{'height': '15px', 'width': (i[0]/total/30*100) + '%', 'background-color': 'rgb(229, 233, 242)'}"></div>
                  <div :style = "{'height': '15px', 'width': (i[1]-i[0])/total/30*100 + '%', 'background-color': '#e6a23c'}"></div>
                  <div :style = "{'height': '15px', 'width': ((total*30-i[1])/total/30*100) + '%', 'background-color': 'rgb(229, 233, 242)'}"></div>
                </div>
              </div>
            </el-collapse-item>
          </el-collapse>
      </div>
    </div>
    
    <el-drawer
      title = "我是标题"
      :visible.sync = "drawer"
      :with-header = "false">
      <div class = "drawer_mainDiv">
        <div class = "drawer_title"> 选择视频 </div>
        <div class = "drawer_button" v-for = "(i, index) in file_list" :key = "index" @click = "selectVideo(i)">
          <el-button>{{i}}</el-button>
        </div>
        <div class = "drawer_title"> 确认选择 </div>
        <div :style = "{'padding': '5px'}">
          <el-alert
            title = "已选择的视频:"
            type = "success"
            :description = "select_video"
            :closable = "false">
          </el-alert>
        </div>
        <div class = "drawer_button">
          <el-button @click = "submitVideo">读取视频</el-button>
        </div>
      </div>
    </el-drawer>

    <el-drawer
      title = "我是标题"
      :visible.sync = "drawer2"
      :with-header = "false">
      <div class = "drawer_mainDiv">
        <div class = "drawer_title"> 预测文本 </div>
        <div :style = "{'padding': '5px'}">
          <el-input
            type = "text"
            placeholder = "输入预测文本"
            v-model = "select_text"
            maxlength = "50"
            show-word-limit
          ></el-input>
        </div>
        <div class = "drawer_title"> 确认选择 </div>
        <div :style = "{'padding': '5px'}">
          <el-alert
            title = "已选择的视频:"
            type = "success"
            :description = "select_video"
            :closable = "false">
          </el-alert>
          <div :style = "{'padding-top': '5px'}">
            <el-alert
              title = "已输入的文本:"
              type = "info"
              :description = "select_text"
              :closable = "false">
            </el-alert>
          </div>
        </div>
        <div class = "drawer_button">
          <el-button @click = "submitText">提交结果</el-button>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script>
export default {
  name: 'videoPage',
  data() {
    return {
      options: [
        {
          value: 1,
          label: 'TALL'
        }, {
          value: 2,
          label: 'MAC'
        }, {
          value: 3,
          label: 'A2C'
        }
      ],
      value: '',
      now_model: this.$cookies.get('now_model'),
      return_list: [],
      total: 7,
      select_video: this.$cookies.get("select_video"),
      imgSrc: require('../assets/1.jpg'),
      select_text: "",
      drawer: false,
      drawer2: false,
      file_list: [],
      video_length: 0,
      playerOptions: {
        playbackRates: [0.5, 1.0, 1.5, 2.0, 2.5, 3.0],        // 可选的播放速度
        autoplay: false,                                      // 如果为true,浏览器准备好时开始回放。
        muted: false,                                         // 默认情况下将会消除任何音频。
        loop: false,                                          // 是否视频一结束就重新开始。
        preload: 'auto',                                      // 建议浏览器在<video>加载元素后是否应该开始下载视频数据。auto浏览器选择最佳行为,立即开始加载视频（如果浏览器支持）
        language: 'zh-CN',
        aspectRatio: '16:9',                                  // 将播放器置于流畅模式，并在计算播放器的动态大小时使用该值。值应该代表一个比例 - 用冒号分隔的两个数字（例如"16:9"或"4:3"）
        fluid: true,                                          // 当true时，Video.js player将拥有流体大小。换句话说，它将按比例缩放以适应其容器。
        sources: [{
          type: "video/mp4",                                  // 类型
          src: this.$cookies.get('src')                       // url地址
        }],
        poster: '',                                           // 封面地址
        notSupportedMessage: '此视频暂无法播放，请稍后再试',    // 允许覆盖 Video.js 无法播放媒体源时显示的默认信息。
        controlBar: {
          timeDivider: true,                    // 当前时间和持续时间的分隔符
          durationDisplay: true,                // 显示持续时间
          remainingTimeDisplay: false,          // 是否显示剩余时间功能
          fullscreenToggle: true                // 是否显示全屏按钮
        }
      }
    }
  },
  methods: {
    returnTitle() {
      if(this.value == -1 || this.value == '' || this.value == null) return "别忘记选择模型啊！";
      else {
        this.now_model = this.options[this.value - 1].label;
        this.$cookies.set('now_model', this.now_model);
        this.$cookies.set('now_model_value', this.value);
        return "你正在使用 " + this.now_model;
      }
    },
    submitVideo() {
      this.$cookies.set("select_video", this.select_video);
      this.$cookies.set("src", this.$main_url + '/api/getMovieData?name=' + this.select_video, "0");
      window.location.reload();
      document.getElementById("source").src =  this.src;
    },
    selectVideo(value) {
      this.select_video = value;
    },
    fileLoad() {
      let _this = this;
      try {
        var selectedFile = _this.$refs.refFile.files[0];
        var fileurl = URL.createObjectURL(selectedFile);
        var audioElement = new Audio(fileurl);

        audioElement.addEventListener("loadedmetadata",  (_event) => {
          _this.video_length = audioElement.duration;
        });

        var name = selectedFile.name;
        var size = selectedFile.size;
        var reader = new FileReader();
        reader.readAsDataURL(selectedFile);
        reader.onload = function() {
          _this.playerOptions.sources[0].src = this.result;
        }
      }
      catch(e) {
        console.log(e);
      }
    },
    clickLoad() {
      this.$refs.refFile.dispatchEvent(new MouseEvent('click'));
    },
    submitText() {
      this.$axios.get(this.$main_url + '/api/getVideoCut', {
        params: {
          model: this.$cookies.get("now_model"),
          video_name: this.select_video.replace('.mp4', ''),
          sentence: this.select_text
        }
      }).then(response => {
        let bet_list = [];
        let data = response.data['list']
        for(let i in data) {
          if(i >= 3) break;
          bet_list.push(data[i]);
        }
        this.return_list = bet_list;
        this.total = document.getElementsByClassName('vjs-duration-display')[0].innerHTML;
        this.total = parseInt(this.total.replace('0:', ''), 10);
      }).catch(error => {
        console.log(error);
      })
    }
  },
  created() {
    this.$axios({
      url: this.$main_url + '/api/getMovieList',
      method: 'get',
    }).then(response => {
      this.file_list = response.data['list'];
      console.log(this.file_list);
    }).catch(error => {
      console.log(error);
    })
  },
  mounted() { 
  },
}
</script>

<style>
.videoBar_div {
  width: 100%;
}

.background{
  width: 100%;  
  height: 100%;       /*  宽高100%是为了图片铺满屏幕  */
  z-index:-1;
  position: fixed;
}

.left_botton_list{
  height: 200px;
  position: fixed;
  right: 10px;
  top: 150px;
  padding: 10px;
  z-index: 2;
}

.selectDiv {
  margin: 15px;
}

.drawer_mainDiv {
  padding: 20px;
}

.drawer_button {
  margin: 7px;
  margin-top: 10px;
  display: inline-block;
}

.drawer_title {
  margin: 5px;
  padding: 5px;
  padding-left: 10px;
  font-size: 20px;
  border-left: 3px solid #4F8699;
  border-bottom: 1px solid #4F8699;
  border-bottom-left-radius: 5px;
}

.drawer_button .el-button {
  max-width: 120px;
  min-width: 120px;
}

.collapse_title_text {
  padding-left: 10px !important;
}

.video-player {
  width: 100%;
}

.collapse_title_text {
  font-size: 16px;
  color: #4F8699;
}

.video-js {
  background-color: rgb(0, 0, 0, 0.3) !important;
}
</style>