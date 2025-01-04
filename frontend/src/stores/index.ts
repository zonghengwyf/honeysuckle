// store/userStore.ts
import { defineStore } from 'pinia'
import {
  SeparateAudioPayload,
  SeparateAudioResponse
} from '@/models/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    isLoggedIn: false,
    showLoginDialog: false,
  }),
  actions: {
    async login(username: string, password: string) {
      try {
        const { $apiFetch } = useNuxtApp()

        const response = await $apiFetch('/user/login', {
          method: 'POST',
          body: {
            // 登录所需的其他信息，例如用户名和密码
            username: username,
            password: password,
          }
        });

        if (response.data) {
          this.isLoggedIn = true;
          this.showLoginDialog = false;
        } else {
          console.error('登录失败:', response.message);
        }
      } catch (error) {
        console.error('登录失败:', error);
      }
    },
    logout() {
      this.isLoggedIn = false;
    },
  },
});

export const useSeparateStore = defineStore('separate', {
  state: () => ({

  }),

  actions: {
    async separateAudio(payload: SeparateAudioPayload): Promise<SeparateAudioResponse> {
      try {
        const { $apiFetch } = useNuxtApp();

        // 创建 FormData 对象
        const formData = new FormData();
        formData.append('audio', payload.audio); // 添加音频文件
        formData.append('separate_type', payload.separateType); // 添加分离方式

        const response = await $apiFetch('/audio/separate/task', {
          method: 'POST',
          body: formData, // 使用 FormData 作为请求体
        }) as SeparateAudioResponse; // 类型断言

        if (response.data) {
          // 在这里处理成功的响应
          console.log('分离成功:', response.data);
          return response; // 返回响应
        } else {
          this.handleError(response.message);
          return response; // 返回响应以便调用者处理
        }
      } catch (error) {
        this.handleError(error);
        throw error; // 抛出错误以便调用者处理
      }
    },

    handleError(error: any) {
      // 统一处理错误
      console.error('分离失败:', error);
      // 这里可以添加更多的错误处理逻辑，比如显示通知等
    }
  }
});

