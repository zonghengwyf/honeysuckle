<template>
  <v-container class="audio-manager">
    <v-row>
      <v-col cols="12">
        <v-card flat>
          <!-- 文件上传区域 -->
          <v-card-title class="px-0">
            <FileUpload
              upload-text="上传音频文件"
              :on-file-change="handleFileChange"
              class="audio-upload"
              :style="{ height: audioFiles.length > 0 ? '200px' : '400px' }"
              accept="audio/*"
            />
          </v-card-title>

          <!-- 音频列表 -->
          <v-card-text class="pa-0">
            <v-data-table
              :items="audioFiles"
              :headers="headers"
              :expanded.sync="expandedRows"
              :show-expand="hasSeparatedTracks"
              no-data-text="暂无音频文件"
              item-key="id"
              hide-default-footer
              class="audio-table"
              @update:expanded="handleRowExpand"
            >
              <!-- 状态指示列 -->
              <template #item.status="{ item }">
                <v-tooltip bottom>
                  <template #activator="{ props }">
                    <v-icon
                      v-bind="props"
                      :color="getStatusColor(item.status)"
                      class="status-icon"
                    >
                      {{ getStatusIcon(item.status) }}
                    </v-icon>
                  </template>
                  <span>{{ item.error || statusMessages[item.status] }}</span>
                </v-tooltip>
              </template>

              <!-- 播放控制列 -->
              <template #item.control="{ item }">
                <div class="play-control">
                  <v-btn
                    :icon="playStates[item.id]?.isPlaying ? 'mdi-pause' : 'mdi-play'"
                    variant="text"
                    @click="toggleAudio(item)"
                  />
                  <AudioPlayer
                    v-model:visible="playStates[item.id]?.visible"
                    :src="item.audioSrc"
                    :mini-mode="true"
                    @update:is-playing="handlePlayStateChange(item.id, $event)"
                  />
                </div>
              </template>

              <!-- 分离方式选择 -->
              <template #item.separateType="{ item }">
                <v-select
                  v-model="item.separateType"
                  :items="separateTypeOptions"
                  item-title="label"
                  item-value="value"
                  density="compact"
                  variant="underlined"
                  :disabled="item.status !== 0"
                  hide-details
                />
              </template>

              <!-- 操作按钮 -->
              <template #item.actions="{ item }">
                <div class="action-buttons">
                  <v-btn
                    color="success"
                    :loading="loadingStates[item.id]?.separating"
                    :disabled="!canSeparate(item)"
                    @click="startSeparation(item)"
                  >
                    <template #loader>
                      <v-progress-circular indeterminate size="20" width="2"/>
                    </template>
                    {{ loadingStates[item.id]?.separating ? '分离中...' : '开始分离' }}
                  </v-btn>
                  <v-btn
                    icon="mdi-download"
                    variant="text"
                    :disabled="!item.audio_file_id"
                    @click="downloadFile(item.audio_file_id!)"
                  />
                  <v-btn
                    icon="mdi-delete"
                    variant="text"
                    color="error"
                    @click="removeAudio(item.id)"
                  />
                </div>
              </template>

              <!-- 扩展音轨列表 -->
              <template #expanded-row="{ item }">
                <v-table v-if="item.tracks?.length" density="compact">
                  <thead>
                    <tr>
                      <th v-for="header in trackHeaders" :key="header.value">
                        {{ header.text }}
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="track in item.tracks" :key="track.id">
                      <td>
                        <div class="track-control">
                          <v-btn
                            :icon="playStates[track.id]?.isPlaying ? 'mdi-pause' : 'mdi-play'"
                            size="small"
                            @click="toggleAudio(track)"
                          />
                          <AudioPlayer
                            v-model:visible="playStates[track.id]?.visible"
                            :src="track.audioSrc"
                            :mini-mode="true"
                            @update:is-playing="handlePlayStateChange(track.id, $event)"
                          />
                        </div>
                      </td>
                      <td>{{ track.file_name }}</td>
                      <td>
                        <v-btn
                          icon="mdi-download"
                          size="small"
                          @click="downloadFile(track.file_id)"
                        />
                      </td>
                    </tr>
                  </tbody>
                </v-table>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import AudioPlayer from '@/components/audio/AudioPlayer.vue';
import FileUpload from '@/components/FileUpload.vue';
import { useBreakpoint } from '@/composables/useBreakpoint';
import { convertKbToReadableSize } from '@/utils/files';
import { Howl } from 'howler'
import { storeToRefs } from 'pinia'
import { useSeparateStore } from '@/stores/separate'
import { convertFileSize } from '@/utils/file'

// 类型定义
interface Track {
  id: string
  file_id: string
  file_name: string
  audioSrc: string
}

interface AudioFile {
  id: string
  status: FileStatus
  audioSrc: string
  fileName: string
  createdAt: string
  separateType?: SeparationType
  file?: File
  size?: string
  tracks?: Track[]
  error?: string
  audio_file_id?: string
}

type FileStatus = -1 | 0 | 1 | 2
type SeparationType = '2stems' | '4stems' | '5stems'
type PlayState = { visible: boolean; isPlaying: boolean }

// 组件配置
const headers = [
  { title: '状态', key: 'status', width: 80 },
  { title: '控制', key: 'control', width: 120 },
  { title: '文件名', key: 'fileName' },
  { title: '创建时间', key: 'createdAt', width: 180 },
  { title: '分离方式', key: 'separateType', width: 150 },
  { title: '操作', key: 'actions', width: 250 },
  { title: '', key: 'data-table-expand' }
]

const trackHeaders = [
  { text: '控制', value: 'control' },
  { text: '音轨名称', value: 'fileName' },
  { text: '下载', value: 'download' }
]

const separateTypeOptions = [
  { label: '人声分离', value: '2stems' },
  { label: '4轨分离', value: '4stems' },
  { label: '5轨分离', value: '5stems' }
]

const statusMessages: Record<FileStatus, string> = {
  [-1]: '分离失败',
  0: '等待处理',
  1: '处理中',
  2: '已完成'
}

// 响应式状态
const audioFiles = ref<AudioFile[]>([])
const expandedRows = ref<string[]>([])
const playStates = ref<Record<string, PlayState>>({})
const loadingStates = ref<Record<string, { separating: boolean }>>({})
const separateStore = useSeparateStore()

// 初始化加载数据
onMounted(async () => {
  try {
    const { data } = await separateStore.fetchAudioFiles()
    audioFiles.value = data.map(formatAudioFile)
  } catch (error) {
    console.error('初始化加载失败:', error)
  }
})

// 文件格式转换
const formatAudioFile = (raw: any): AudioFile => ({
  id: raw.id,
  status: raw.status,
  audioSrc: raw.audio_url,
  fileName: raw.file_name,
  createdAt: new Date(raw.created_at).toLocaleString(),
  separateType: raw.separation_type,
  size: convertFileSize(raw.file_size),
  error: raw.error_message,
  audio_file_id: raw.audio_file_id,
  tracks: raw.tracks?.map((t: any) => ({
    id: t.track_id,
    file_id: t.file_id,
    file_name: t.file_name,
    audioSrc: t.audio_url
  }))
})

// 文件上传处理
const handleFileChange = async (file: File) => {
  try {
    const audioSrc = URL.createObjectURL(file)
    const newFile: AudioFile = {
      id: crypto.randomUUID(),
      status: 0,
      audioSrc,
      fileName: file.name,
      createdAt: new Date().toLocaleString(),
      file,
      size: convertFileSize(file.size)
    }

    const { data } = await separateStore.uploadFile(file)
    newFile.audio_file_id = data.file_id
    audioFiles.value.unshift(newFile)
  } catch (error) {
    console.error('文件上传失败:', error)
    showError('文件上传失败，请重试')
  }
}

// 音频播放控制
const toggleAudio = (target: AudioFile | Track) => {
  const state = playStates.value[target.id] ||= { visible: false, isPlaying: false }
  state.visible = true
  state.isPlaying = !state.isPlaying
}

const handlePlayStateChange = (id: string, playing: boolean) => {
  if (playStates.value[id]) {
    playStates.value[id].isPlaying = playing
  }
}

// 音轨分离处理
const startSeparation = async (item: AudioFile) => {
  try {
    loadingStates.value[item.id] = { separating: true }

    const { data } = await separateStore.startSeparation({
      fileId: item.audio_file_id!,
      type: item.separateType!
    })

    const index = audioFiles.value.findIndex(f => f.id === item.id)
    if (index !== -1) {
      audioFiles.value[index] = {
        ...item,
        status: 1,
        tracks: data.tracks?.map(formatTrack)
      }
    }
  } catch (error) {
    console.error('分离失败:', error)
    showError('音轨分离失败，请检查设置')
  } finally {
    delete loadingStates.value[item.id]
  }
}

const formatTrack = (raw: any): Track => ({
  id: raw.track_id,
  file_id: raw.file_id,
  file_name: raw.file_name,
  audioSrc: raw.audio_url
})

// 文件下载
const downloadFile = async (fileId: string) => {
  try {
    const blob = await separateStore.downloadFile(fileId)
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `audio_${Date.now()}${getFileExtension(blob.type)}`
    document.body.appendChild(link)
    link.click()
    link.remove()
    URL.revokeObjectURL(url)
  } catch (error) {
    console.error('下载失败:', error)
    showError('文件下载失败，请重试')
  }
}

const getFileExtension = (mimeType: string) => {
  const extensions: Record<string, string> = {
    'audio/mpeg': '.mp3',
    'audio/wav': '.wav',
    'audio/ogg': '.ogg'
  }
  return extensions[mimeType] || '.audio'
}

// 文件删除
const removeAudio = async (fileId: string) => {
  try {
    await separateStore.deleteFile(fileId)
    const index = audioFiles.value.findIndex(f => f.id === fileId)
    if (index !== -1) {
      const [removed] = audioFiles.value.splice(index, 1)
      cleanupFileResources(removed)
    }
  } catch (error) {
    console.error('删除失败:', error)
    showError('文件删除失败，请重试')
  }
}

const cleanupFileResources = (file: AudioFile) => {
  if (file.audioSrc?.startsWith('blob:')) {
    URL.revokeObjectURL(file.audioSrc)
  }
  delete playStates.value[file.id]
  file.tracks?.forEach(track => delete playStates.value[track.id])
}

// 表格扩展行控制
const hasSeparatedTracks = computed(() =>
  audioFiles.value.some(f => f.status === 2 && f.tracks?.length)
)

const handleRowExpand = async ({ 0: itemId }) => {
  if (!itemId) return

  const item = audioFiles.value.find(f => f.id === itemId)
  if (item?.status === 2 && !item.tracks) {
    try {
      const { data } = await separateStore.fetchTracks(item.audio_file_id!)
      item.tracks = data.tracks.map(formatTrack)
    } catch (error) {
      console.error('加载音轨失败:', error)
    }
  }
}

// 状态显示辅助
const getStatusIcon = (status: FileStatus) => {
  const icons: Record<FileStatus, string> = {
    [-1]: 'mdi-alert-circle',
    0: 'mdi-clock-outline',
    1: 'mdi-progress-helper',
    2: 'mdi-check-circle'
  }
  return icons[status]
}

const getStatusColor = (status: FileStatus) => {
  const colors: Record<FileStatus, string> = {
    [-1]: 'error',
    0: 'grey',
    1: 'warning',
    2: 'success'
  }
  return colors[status]
}

// 清理资源
onUnmounted(() => {
  audioFiles.value.forEach(cleanupFileResources)
})

// 工具函数
const showError = (message: string) => {
  // 实现错误提示逻辑
}

const canSeparate = (item: AudioFile) =>
  item.status === 0 && !!item.separateType
</script>

<style scoped>
.audio-manager {
  max-width: 1200px;
  margin: 0 auto;
}

.audio-upload {
  transition: height 0.3s ease;
  border: 2px dashed rgba(var(--v-border-color), 0.5);
  border-radius: 8px;
}

.audio-table {
  --v-table-header-height: 48px;
}

.play-control {
  display: flex;
  align-items: center;
  gap: 8px;
}

.action-buttons {
  display: flex;
  gap: 8px;
  align-items: center;
}

.status-icon {
  cursor: help;
}

.track-control {
  display: flex;
  align-items: center;
  gap: 4px;
}
</style>
