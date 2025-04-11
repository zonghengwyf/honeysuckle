// stores/separator.ts
import { defineStore } from 'pinia'
import type {
  SeparateAudioListPayload,
  SeparateTracksListPayload,
  SeparateAudioPayload,
  OperateResponse,
  SeparateAudioResponse,
  SeparateTracksResponse
} from '@/models/api'

interface FileProcessingState {
  [key: string]: boolean
}

interface Track {
  file_id: number
  file_name: string
  audioSrc: string
  size?: string
}

interface ProcessedFile {
  id: string
  status: -1 | 0 | 1 | 2
  fileName: string
  createdAt: string
  separateType: string
  size?: string
  tracks?: Track[]
  error?: string
  audio_file_id?: number
}

export const useSeparatorStore = defineStore('separator', {
  state: () => ({
    processedFiles: [] as ProcessedFile[],
    currentProcessing: null as string | null,
    uploadProgress: 0,
    downloadProgress: 0,
    isLoading: false,
    error: null as string | null,
    processingStates: {} as FileProcessingState
  }),

  actions: {
    // 统一处理请求错误
    handleError(error: any) {
      this.error = error.message || '请求处理失败'
      console.error('[Separator Store Error]:', error)
      // 此处可接入通知系统
    },

    // 文件上传与处理
    async uploadFile(fileData: ProcessedFile) {
      try {
        this.processedFiles.unshift(fileData)
        this.uploadProgress = 0
        // 模拟上传进度
        const progressInterval = setInterval(() => {
          this.uploadProgress = Math.min(this.uploadProgress + 20, 100)
        }, 200)
        
        await new Promise(resolve => setTimeout(resolve, 1000))
        clearInterval(progressInterval)
      } catch (error) {
        this.handleError(error)
      }
    },

    // 音频分离处理
    async processFile(payload: {
      fileId: string
      type: string
    }) {
      try {
        const { $apiFetch } = useNuxtApp()
        this.processingStates[payload.fileId] = true
        this.currentProcessing = payload.fileId

        const formData = new FormData()
        const targetFile = this.processedFiles.find(f => f.id === payload.fileId)
        if (targetFile?.file) {
          formData.append('file', targetFile.file)
        }
        formData.append('separate_type', payload.type)

        const response = await $apiFetch<SeparateAudioResponse>('/audio/separator/voices', {
          method: 'POST',
          body: formData,
          onUploadProgress: (progressEvent) => {
            this.uploadProgress = Math.round(
              (progressEvent.loaded / (progressEvent.total || 1)) * 100
            )
          }
        })

        if (response.data) {
          this.updateFileStatus(payload.fileId, 1)
          await this.fetchProcessedFiles()
        }
        return response
      } catch (error) {
        this.updateFileStatus(payload.fileId, -1, error)
        throw error
      } finally {
        this.processingStates[payload.fileId] = false
        this.currentProcessing = null
      }
    },

    // 获取处理结果列表
    async fetchProcessedFiles() {
      try {
        this.isLoading = true
        const { $apiFetch } = useNuxtApp()
        const response = await $apiFetch<SeparateAudioResponse>('/audio/separator/voices-list', {
          method: 'GET'
        })

        if (response.data) {
          this.processedFiles = response.data.map(item => ({
            id: item.id,
            status: item.status,
            fileName: item.file_name,
            createdAt: item.create_time,
            separateType: item.separator,
            size: item.file_size ? this.convertFileSize(item.file_size) : undefined,
            error: item.error,
            audio_file_id: item.audio_file_id
          }))
        }
        return response
      } catch (error) {
        this.handleError(error)
        throw error
      } finally {
        this.isLoading = false
      }
    },

    // 获取音轨详情
    async fetchTracks(payload: { taskId: string } & SeparateTracksListPayload) {
      try {
        const { $apiFetch } = useNuxtApp()
        const response = await $apiFetch<SeparateTracksResponse>(
          `/audio/separator/tracks/${payload.taskId}`,
          { method: 'GET', params: payload }
        )

        if (response.data) {
          const index = this.processedFiles.findIndex(f => f.id === payload.taskId)
          if (index !== -1) {
            this.processedFiles[index].tracks = response.data.map(track => ({
              file_id: track.file_id,
              file_name: track.file_name,
              audioSrc: track.audio_src,
              size: track.file_size ? this.convertFileSize(track.file_size) : undefined
            }))
          }
        }
        return response
      } catch (error) {
        this.handleError(error)
        throw error
      }
    },

    // 文件删除操作
    async deleteFile(fileId: string) {
      try {
        const { $apiFetch } = useNuxtApp()
        const response = await $apiFetch<OperateResponse>(
          `/audio/separator/voices/${fileId}`,
          { method: 'DELETE' }
        )

        if (response.success) {
          this.processedFiles = this.processedFiles.filter(f => f.id !== fileId)
        }
        return response
      } catch (error) {
        this.handleError(error)
        throw error
      }
    },

    // 文件下载处理
    async downloadFile(fileId: string) {
      try {
        const { $apiFetch } = useNuxtApp()
        const controller = new AbortController()
        
        const response = await $apiFetch<Blob>(
          `/audio/separator/voices/download/${fileId}`,
          {
            method: 'GET',
            responseType: 'blob',
            signal: controller.signal,
            onDownloadProgress: (progressEvent) => {
              this.downloadProgress = Math.round(
                (progressEvent.loaded / (progressEvent.total || 1)) * 100
              )
            }
          }
        )

        this.handleBlobDownload(response, fileId)
        return response
      } catch (error) {
        this.handleError(error)
        throw error
      }
    },

    // 辅助方法
    updateFileStatus(fileId: string, status: -1 | 0 | 1 | 2, error?: any) {
      const index = this.processedFiles.findIndex(f => f.id === fileId)
      if (index !== -1) {
        this.processedFiles[index].status = status
        if (error) {
          this.processedFiles[index].error = error.message || '处理失败'
        }
      }
    },

    convertFileSize(bytes: number) {
      const units = ['B', 'KB', 'MB', 'GB']
      let size = bytes
      let unitIndex = 0
      while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024
        unitIndex++
      }
      return `${size.toFixed(1)} ${units[unitIndex]}`
    },

    handleBlobDownload(blob: Blob, fileName: string) {
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `${fileName}.zip`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    }
  },

  getters: {
    completedFiles: (state) => state.processedFiles.filter(f => f.status === 2),
    failedFiles: (state) => state.processedFiles.filter(f => f.status === -1),
    isProcessing: (state) => !!state.currentProcessing,
    getFileById: (state) => (id: string) => state.processedFiles.find(f => f.id === id)
  }
})
