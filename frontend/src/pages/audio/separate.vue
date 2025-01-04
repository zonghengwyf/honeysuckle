<template>
  <v-container>
    <v-row class="mt-16">
      <v-col cols="12">
        <v-card flat>
          <v-btn @click="uploadFile" color="primary">上传文件</v-btn>
          <v-divider></v-divider>

          <v-data-table
            :items="audioFiles"
            :headers="headers"
            :expanded.sync="expanded"
            :show-expand="canExpand"
            hide-default-header
            hide-default-footer
          >
            <template #item.status="{ item }">
              <v-icon :color="getStatusColor(item.status)">
                {{ getStatusIcon(item.status) }}
              </v-icon>
            </template>
            <template #item.audioSrc="{ item }">
              <div class="text-center">
                <v-btn @click="() => togglePlay(item)">
                  <v-icon>{{ isAudioPlaying[item.audioSrc] ? 'mdi-pause' : 'mdi-play' }}</v-icon>
                </v-btn>
                <v-snackbar v-model="audioSnackbar[item.audioSrc]" vertical timeout="-1">
                  <AudioPlayer
                    ref="audioPlayerRefs[item.audioSrc]"
                    :src="item.audioSrc"
                    :audioName="item.fileName"
                    :isPlaying="isAudioPlaying[item.audioSrc]"
                    @togglePlay="handleTogglePlay(item.audioSrc)"
                    @ended="handleAudioEnd(item.audioSrc)"
                  />
                  <template v-slot:actions>
                    <v-btn color="indigo" variant="text" @click="closeSnackbar(item.audioSrc)">Close</v-btn>
                  </template>
                </v-snackbar>
              </div>
            </template>
            <template #item.fileName="{ item }">
              <v-icon>mdi-music</v-icon> {{ item.fileName }}
            </template>
            <template #item.createdAt="{ item }">
              <span v-if="isLgAndUp">{{ item.createdAt }}</span>
            </template>
            <template #item.separateType="{ item }">
              <v-select
                clearable
                chips
                height="20"
                width="150"
                label="分离方式"
                active="true"
                :items="separateTypeItems"
                item-title="title"
                item-value="value"
                variant="underlined"
                v-model="item.separateType"
              ></v-select>
            </template>
            <template #item.download="{ item }">
              <v-icon @click="downloadFile(item.audioSrc)">mdi-download</v-icon>
            </template>
            <template #item.actions="{ item }">
              <v-btn
                prepend-icon="mdi-arrow-right"
                @click="separateAudio(item)"
                v-if="item.separateType"
              >
                <template v-slot:prepend>
                  <v-icon color="success" size="30"></v-icon>
                </template>
                开始分离
              </v-btn>
            </template>
            <template #expanded-row="{ columns, item }">
              <tr>
                <td :colspan="columns.length">{{ item.fileName }}</td>
              </tr>
            </template>
            <template #item.delete="{ index }">
              <v-btn
                icon="$close"
                size="small"
                variant="text"
                @click="removeFile(index)"
              ></v-btn>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue';
import AudioPlayer from '@/components/audio/AudioPlayer.vue';
import { useBreakpoint } from '@/composables/useBreakpoint';
import { useSeparateStore } from '@/stores/index';

const { isLgAndUp } = useBreakpoint();

interface AudioFile {
  status: number;
  audioSrc: string;
  fileName: string;
  createdAt: string;
  separateType?: string; // 分离方式
  audio?: File; // 添加音频文件属性
}

interface SelectItem {
  title: string;
  value: string;
}

const headers = ref([
  { text: '状态', value: 'status' },
  { text: '音频源', value: 'audioSrc' },
  { text: '文件名', value: 'fileName' },
  { text: '创建时间', value: 'createdAt' },
  { text: '分离方式', value: 'separateType' },
  { text: '下载', value: 'download' },
  { text: '操作', value: 'actions' },
  { text: '拓展', value: 'expanded' },
  { text: '删除', value: 'delete' },
]);

const expanded = ref([]);
const audioFiles = ref<AudioFile[]>([]);
const audioSnackbar = ref<{ [key: string]: boolean }>({});
const isAudioPlaying = ref<{ [key: string]: boolean }>({});
const audioPlayerRefs = ref<{ [key: string]: InstanceType<typeof AudioPlayer> | null }>({});
const separateTypeItems = ref<SelectItem[]>([
  { title: '人声分离', value: '2stems' },
  { title: '4轨分离', value: '4stems' },
  { title: '5轨分离', value: '5stems' },
]);

// 上传音频文件
const uploadFile = async () => {
  const fileInput = document.createElement('input');
  fileInput.type = 'file';
  fileInput.accept = 'audio/*';
  fileInput.onchange = (event) => {
    const files = event.target.files;
    if (files && files.length > 0) {
      const file = files[0];
      const audioSrc = URL.createObjectURL(file);
      const createdAt = new Date().toLocaleString();
      audioFiles.value.push({
        status: 1,
        audioSrc,
        fileName: file.name,
        createdAt,
        separateType: separateTypeItems.value[0].value, // 初始化为第一个选项
        audio: file, // 存储音频文件
      });
      audioPlayerRefs.value[audioSrc] = null;
    }
  };
  fileInput.click();
};

// 分离音频
const separateAudio = async (item: AudioFile) => {
  console.log("当前分离方式:", item.separateType); // 获取 select 的值

  const separateStore = useSeparateStore(); // 实例化 store

  try {
    console.log('22222222222222222222222')
    console.log(item.audio)
    console.log(typeof item.audio)
    const response = await separateStore.separateAudio({
      audio: item.audio, // 确保这里是 File 类型
      separate_type: item.separateType,
    });

    if (response.data) {
      console.log('分离结果:', response.data);
      // 继续处理分离结果
    } else {
      console.error('分离失败:', response.message);
    }
  } catch (error) {
    console.error('执行分离时发生错误:', error);
  }
};

// 下载音频文件
const downloadFile = (audioSrc: string) => {
  const link = document.createElement('a');
  link.href = audioSrc;
  link.download = audioSrc.split('/').pop() || 'download.mp3';
  link.click();
};

// 移除音频文件
const removeFile = (index: number) => {
  const audioFile = audioFiles.value[index];
  if (audioFile) {
    URL.revokeObjectURL(audioFile.audioSrc);
    audioFiles.value.splice(index, 1);
    delete isAudioPlaying.value[audioFile.audioSrc];
    delete audioSnackbar.value[audioFile.audioSrc];
    delete audioPlayerRefs.value[audioFile.audioSrc];
  }
};

// 关闭 Snackbar
const closeSnackbar = (src: string) => {
  audioSnackbar.value[src] = false;
  isAudioPlaying.value[src] = false;
};

// 播放或暂停音频
const togglePlay = (item: AudioFile) => {
  if (audioSnackbar.value[item.audioSrc]) {
    isAudioPlaying.value[item.audioSrc] = !isAudioPlaying.value[item.audioSrc];
  } else {
    audioSnackbar.value[item.audioSrc] = true;
    isAudioPlaying.value[item.audioSrc] = true;
  }
};

// 处理音频结束事件
const handleAudioEnd = (src: string) => {
  isAudioPlaying.value[src] = false;
  audioSnackbar.value[src] = false;
};

// 处理播放状态切换
const handleTogglePlay = (src: string) => {
  isAudioPlaying.value[src] = !isAudioPlaying.value[src];
};

// 获取状态图标
const getStatusIcon = (status: number) => {
  switch (status) {
    case 1: return 'mdi-check-circle';
    case 0: return 'mdi-clock';
    default: return 'mdi-help-circle';
  }
};

// 获取状态颜色
const getStatusColor = (status: number) => {
  switch (status) {
    case 1: return '#28a745'; // 绿色
    case 0: return '#6C757D'; // 灰色
    default: return ''; // 默认
  }
};

// 计算属性，确定是否显示展开功能
const canExpand = computed(() => {
  return audioFiles.value.some(item => item.status === 1);
});
</script>

<style scoped>
/* 你的样式 */
</style>
