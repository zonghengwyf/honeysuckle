<template>
  <v-app :dark="themeDark">
    <v-app-bar elevate-on-scroll height="70" fixed>
      <v-container>
        <v-row>
          <v-col class="w-full d-flex">
            <nuxt-link to="/" class="text-decoration-none mt-5 d-flex">
              <v-avatar tile size="33" class="mt-1">
                <v-img contain :src="logoSrc"></v-img>
              </v-avatar>
              <h3 v-if="isLgAndUp" class="text-h4 ml-1 text--primary">
                金银花
              </h3>
            </nuxt-link>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              class="my-5"
              :large="isLgAndUp"
              @click="userStore.showLoginDialog = true"
            >
              登录
            </v-btn>
            <v-btn @click="themeDark = !themeDark">切换主题</v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-app-bar>

    <v-main>
      <NuxtPage></NuxtPage>
    </v-main>

    <v-footer class="pt-4">
      <v-container>
        <v-row class="mt-4">
          <v-col class="text-center">
            <p class="text--secondary">
              备案号:
              <a href="https://beian.miit.gov.cn/#/Integrated/index" target="_blank" class="text--primary">
                <strong>鄂ICP备20001614号-1</strong>
              </a>
            </p>
          </v-col>
        </v-row>
      </v-container>
    </v-footer>

    <LoginDialog />
  </v-app>
</template>

<script lang="ts" setup>
import { computed } from 'vue';
import { ref } from 'vue';

import { useUserStore } from '@/stores/index';
import LoginDialog from '@/components/LoginDialog.vue';
import { useBreakpoint } from '@/composables/useBreakpoint';
import logoSrc from '@/assets/img/logo.svg';

const themeDark = ref(true); // 设置初始主题
const { isLgAndUp } = useBreakpoint();
const userStore = useUserStore();
</script>

<style scoped>
.theme-btn {
  transition: color 0.3s ease;
}
</style>
