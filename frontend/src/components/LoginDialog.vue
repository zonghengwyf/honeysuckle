<template>
  <v-dialog v-model="userStore.showLoginDialog" max-width="600px">
    <v-card>
      <v-card-title>登录</v-card-title>
      <v-card-text>
        <v-text-field v-model="username" label="用户名" />
        <v-text-field v-model="password" label="密码" type="password" />
      </v-card-text>
      <v-card-actions>
        <v-btn @click="handleLogin">登录</v-btn>
        <v-btn @click="userStore.showLoginDialog = false">取消</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { useUserStore } from '@/stores/index';

const userStore = useUserStore();
const username = ref('');
const password = ref('');

const handleLogin = () => {
  // 这里可以添加实际的登录逻辑
  userStore.login();
};
</script>