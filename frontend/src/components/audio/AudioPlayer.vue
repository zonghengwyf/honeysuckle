<script setup>
import { ref, watch, onUnmounted, computed } from 'vue'
import { Howl } from 'howler'

const props = defineProps({
  src: {
    type: String,
    required: true
  },
  loop: {
    type: Boolean,
    default: false
  },
  playbackRate: {
    type: Number,
    default: 1.0,
    validator: v => v >= 0.5 && v <= 4.0
  },
  initialVolume: {
    type: Number,
    default: 1.0,
    validator: v => v >= 0 && v <= 1
  },
  autoplay: {
    type: Boolean,
    default: false
  },
  showControls: {
    type: Boolean,
    default: true
  },
  color: {
    type: String,
    default: 'primary'
  }
})

const emit = defineEmits([
  'end',
  'play',
  'pause',
  'volume-change',
  'rate-change',
  'update:loop',
  'update:playbackRate'
])

// 播放器状态
const isPlaying = ref(false)
const duration = ref(0)
const currentTime = ref(0)
const volume = ref(props.initialVolume)
const isMuted = ref(false)
const progress = ref(0)

let howl = null
let animationFrameId = null

// 初始化播放器
const initPlayer = () => {
  if (howl) {
    howl.unload()
    cancelAnimationFrame(animationFrameId)
  }

  howl = new Howl({
    src: [props.src],
    html5: true,
    loop: props.loop,
    rate: props.playbackRate,
    volume: volume.value,
    autoplay: props.autoplay,
    onend: () => emit('end'),
    onplay: () => {
      isPlaying.value = true
      emit('play')
      updateProgress()
    },
    onpause: () => {
      isPlaying.value = false
      emit('pause')
    },
    onstop: () => {
      isPlaying.value = false
    },
    onload: () => {
      duration.value = howl.duration()
    },
    onloaderror: (_, msg) => console.error('加载失败:', msg)
  })
}

// 进度条更新
const updateProgress = () => {
  if (howl && howl.playing()) {
    currentTime.value = howl.seek()
    progress.value = (currentTime.value / duration.value) * 100
    animationFrameId = requestAnimationFrame(updateProgress)
  }
}

// 播放控制
const togglePlay = () => {
  if (!howl) return
  howl.playing() ? howl.pause() : howl.play()
}

// 进度跳转
const seek = (value) => {
  if (howl) {
    howl.seek((value / 100) * duration.value)
  }
}

// 音量控制
const setVolume = (value) => {
  volume.value = value
  isMuted.value = value === 0
  if (howl) {
    howl.volume(value)
    emit('volume-change', value)
  }
}

// 静音切换
const toggleMute = () => {
  isMuted.value = !isMuted.value
  setVolume(isMuted.value ? 0 : volume.value || 0.5)
}

// 时间格式化
const formatTime = (seconds) => {
  const minutes = Math.floor(seconds / 60)
  seconds = Math.floor(seconds % 60)
  return `${minutes}:${seconds.toString().padStart(2, '0')}`
}

// 监听属性变化
watch(() => props.src, initPlayer)
watch(() => props.loop, (val) => {
  if (howl) howl.loop(val)
})
watch(() => props.playbackRate, (val) => {
  if (howl) {
    howl.rate(val)
    emit('rate-change', val)
  }
})
watch(() => props.autoplay, (val) => {
  if (val && howl && !howl.playing()) howl.play()
})

// 暴露组件方法
defineExpose({
  play: () => howl?.play(),
  pause: () => howl?.pause(),
  stop: () => howl?.stop(),
  seekTo: (seconds) => {
    if (howl) howl.seek(seconds)
  },
  setRate: (rate) => {
    if (howl) {
      howl.rate(rate)
      emit('rate-change', rate)
    }
  },
  getDuration: () => duration.value,
  getCurrentTime: () => currentTime.value
})

// 组件卸载清理
onUnmounted(() => {
  if (howl) {
    howl.unload()
    cancelAnimationFrame(animationFrameId)
  }
})

initPlayer()
</script>

<template>
  <v-card
    class="audio-player"
    :color="color"
    variant="outlined"
    elevation="1"
  >
    <v-row align="center" class="pa-3" v-if="showControls">
      <!-- 播放控制 -->
      <v-col cols="auto">
        <v-btn
          :icon="isPlaying ? 'mdi-pause' : 'mdi-play'"
          @click="togglePlay"
          :color="color"
        />
      </v-col>

      <!-- 进度条 -->
      <v-col>
        <v-slider
          v-model="progress"
          @update:model-value="seek"
          :max="100"
          hide-details
          thumb-label="always"
          :color="color"
        >
          <template v-slot:thumb-label="{ modelValue }">
            {{ formatTime((modelValue / 100) * duration) }}
          </template>
        </v-slider>
        <div class="d-flex justify-space-between mt-1 text-caption">
          <span>{{ formatTime(currentTime) }}</span>
          <span>{{ formatTime(duration) }}</span>
        </div>
      </v-col>

      <!-- 速率控制 -->
      <v-col cols="auto">
        <v-menu>
          <template v-slot:activator="{ props: menuProps }">
            <v-tooltip text="播放速率">
              <template v-slot:activator="{ props: tooltipProps }">
                <v-btn
                  v-bind="{ ...menuProps, ...tooltipProps }"
                  :color="color"
                  variant="text"
                  class="text-body-2"
                >
                  {{ playbackRate }}x
                </v-btn>
              </template>
            </v-tooltip>
          </template>
          <v-list density="compact">
            <v-list-item
              v-for="rate in [0.5, 1.0, 1.5, 2.0]"
              :key="rate"
              :value="rate"
              @click="$emit('update:playbackRate', rate)"
            >
              <v-list-item-title>{{ rate }}x</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-col>

      <!-- 音量控制 -->
      <v-col cols="auto">
        <v-menu offset-y>
          <template v-slot:activator="{ props }">
            <v-btn
              v-bind="props"
              :icon="isMuted ? 'mdi-volume-off' : 'mdi-volume-high'"
              :color="color"
            />
          </template>
          <v-card class="pa-4">
            <v-slider
              v-model="volume"
              vertical
              :max="1"
              :step="0.1"
              :color="color"
              thumb-label="always"
              style="height: 120px"
            />
          </v-card>
        </v-menu>
      </v-col>

      <!-- 循环控制 -->
      <v-col cols="auto">
        <v-tooltip :text="loop ? '关闭循环' : '开启循环'">
          <template v-slot:activator="{ props }">
            <v-btn
              v-bind="props"
              :icon="loop ? 'mdi-repeat-on' : 'mdi-repeat-off'"
              :color="loop ? color : ''"
              @click="$emit('update:loop', !loop)"
            />
          </template>
        </v-tooltip>
      </v-col>
    </v-row>

    <!-- 无控制条模式 -->
    <audio v-else :src="src" />
  </v-card>
</template>

<style scoped>
.audio-player {
  max-width: 800px;
  margin: 0 auto;
  transition: all 0.3s ease;
}

.audio-player:hover {
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
</style>
