<template>
  <div>
    <audio
      ref="audio"
      @timeupdate="updateCurrentTime"
      @loadedmetadata="setDuration"
      :src="src"
      @ended="handleAudioEnd"
      :volume="volume"
    />
    <div class="controls">
      <v-btn @click="togglePlay" icon>
        <v-icon>{{ isPlaying ? 'mdi-pause' : 'mdi-play' }}</v-icon>
      </v-btn>
      <div class="audio-player" :class="{ visible: true }">
        <span class="audio-name">{{ audioName }}</span>
        <div class="track" @click="seekTrack">
          <div class="progress" :style="{ width: progressWidth }"></div>
          <span>{{ formatTime(currentTime) }} / {{ formatTime(duration) }}</span>
        </div>
        <v-slider v-model="volume" @input="setVolume" min="0" max="1" step="0.01" />
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, defineProps, defineEmits, watch } from 'vue';

const props = defineProps<{
  src: string; // 接收音频源
  audioName: string; // 音频名称
  isPlaying: boolean; // 接收播放状态
}>();

const emit = defineEmits<{
  (e: 'togglePlay'): void; // 定义 togglePlay 事件
  (e: 'ended'): void; // 定义 ended 事件
}>();

const audio = ref<HTMLAudioElement | null>(null);
const volume = ref(1); // 音量控制
const currentTime = ref(0);
const duration = ref(0);

// 监控 isPlaying 状态变化
watch(() => props.isPlaying, (newValue) => {
  if (audio.value) {
    if (newValue) {
      audio.value.play();
    } else {
      audio.value.pause();
    }
  }
});

// 切换播放状态
const togglePlay = () => {
  emit('togglePlay'); // 通知外部切换播放状态
};

// 更新当前时间
const updateCurrentTime = () => {
  if (audio.value) {
    currentTime.value = audio.value.currentTime;
  }
};

// 设置音频持续时间
const setDuration = () => {
  if (audio.value) {
    duration.value = audio.value.duration;
  }
};

// 音频结束处理
const handleAudioEnd = () => {
  emit('ended'); // 通知外部音频结束
};

// 格式化时间
const formatTime = (time: number) => {
  const minutes = Math.floor(time / 60);
  const seconds = Math.floor(time % 60);
  return `${minutes}:${seconds < 10 ? '0' + seconds : seconds}`;
};

// 寻找音轨
const seekTrack = (event: MouseEvent) => {
  const track = event.currentTarget as HTMLElement;
  const rect = track.getBoundingClientRect();
  const offsetX = event.clientX - rect.left;
  const percentage = offsetX / track.clientWidth;
  if (audio.value) {
    audio.value.currentTime = percentage * duration.value;
  }
};

// 设置音量
const setVolume = (value: number) => {
  volume.value = value; // 更新音量状态
  if (audio.value) {
    audio.value.volume = value; // 设置音频元素的音量
  }
};

// 计算进度条宽度
const progressWidth = computed(() => {
  return duration.value > 0 ? (currentTime.value / duration.value) * 100 + '%' : '0%';
});

</script>

<style scoped>
.audio-player {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0; /* 确保在页面底部 */
  height: 60px; /* 设置高度 */
  z-index: 1000; /* 提高 z-index 确保在其他元素之上 */
  background: rgba(255, 255, 255, 0.9);
  padding: 10px;
  box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.controls {
  display: flex;
  align-items: center;
}

.track {
  width: 300px;
  height: 5px;
  background: #ccc;
  position: relative;
  cursor: pointer;
  margin: 0 10px;
}

.progress {
  height: 100%;
  background: #76c7c0;
}

.audio-name {
  margin-bottom: 5px;
  font-weight: bold;
}
</style>