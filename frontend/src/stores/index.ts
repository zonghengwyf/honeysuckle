// store/userStore.ts
import { defineStore } from 'pinia'

import { separatorStore } from '@/stores/separator'

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

export const useSeparateStore = defineStore('separator', separatorStore);

