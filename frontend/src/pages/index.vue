<template>
  <div>
    <v-container>
      <v-row :class="{ 'py-16': isLgAndUp }">
        <v-col
          cols="12"
          md="6"
          :class="{
            'text-center pt-16': isMdAndDown,
            'py-16': isLgAndUp,
          }"
        >
          <h1
            class="text-h2 font-weight-bold pb-1 gradient-header"
            :class="{
              'mt-16': isLgAndUp,
              'mt-10': isMdOnly,
              'mt-8': isSmAndDown,
            }"
          >
            人声和音乐分离
          </h1>
          <h2 class="text--secondary text-h5 mt-8 mb-8">
            <span class="gradient-underline">人声分离</span> 基于AI将音频文件的人声和乐器分离
          </h2>
          <div :class="{ 'text-center': isMdAndDown }">
            <v-btn
              color="primary"
              large
              class="mt-4 mb-4"
              v-auth="uploadAudioFile"
            >
              <v-icon v-if="isLgAndUp" left>
                {{ mdiSend }}
              </v-icon>
              上传文件
            </v-btn>
            <v-btn
              large
              color="secondary"
              class="mt-4 mb-4 ml-4"
              href="#"
            >
              <v-icon v-if="isLgAndUp" left color="#ffe500">
                {{ mdiCreation }}
              </v-icon>
              查看示例
            </v-btn>
          </div>
        </v-col>
        <v-col
          v-if="isMdAndUp"
          cols="12"
          md="6"
          class="py-16"
        >
          <v-img
            class="mx-auto mb-4"
            max-height="700"
            max-width="98%"
            contain
            :src="voice_2_stems"
          ></v-img>
        </v-col>
      </v-row>
    </v-container>
    <!--
    <v-sheet class="py-16">
      <v-container>
        <v-row class="mb-16">
          <v-col cols="12" md="6" class="d-flex align-center" :order-lg="2">
            <div>
              <h3 class="text-h3 mb-1">4轨乐器分离</h3>
              <h5 class="text-h6 font-weight-light">声乐/鼓/贝司/其他分离</h5>
              <v-btn to="#" class="primary">开始使用</v-btn>
            </div>
          </v-col>
          <v-col cols="12" md="6" :order-lg="1">
            <v-img
              class="mb-4"
              max-height="400"
              contain
              :src="voice_4_stems"
            ></v-img>
          </v-col>
        </v-row>
        <v-row class="mb-16 mt-16">
          <v-col cols="12" md="6" class="d-flex align-center" :order-lg="1">
            <div>
              <h3 class="text-h3 mb-1">5轨乐器分离</h3>
              <h5 class="text-h6 font-weight-light">声乐/鼓/贝司/钢琴/其他分离</h5>
              <v-btn to="#" class="primary">开始使用</v-btn>
            </div>
          </v-col>
          <v-col cols="12" md="6" :order-lg="2">
            <v-img
              class="mb-4"
              max-height="400"
              contain
              :src="voice_5_stems"
            ></v-img>
          </v-col>
        </v-row>
      </v-container>
    </v-sheet>
    -->
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import { mdiSend as mdiSendIcon, mdiCreation as mdiCreationIcon } from '@mdi/js'; // 重命名导入

import { useUserStore } from '@/stores/index';
import { useBreakpoint } from '@/composables/useBreakpoint';
import voice_2_stems from '@/assets/img/voice-2-stems.svg';
import voice_4_stems from '@/assets/img/voice-4-stems.svg';
import voice_5_stems from '@/assets/img/voice-5-stems.svg';

// 直接使用导入的图标
const mdiSend = mdiSendIcon;
const mdiCreation = mdiCreationIcon;
// 使用 Vuetify 的响应式显示
const { isLgAndUp, isMdAndDown, isMdAndUp, isSmAndDown, isMdOnly } = useBreakpoint();
const userStore = useUserStore();
const router = useRouter();

const uploadAudioFile = async () => {
    router.push('/audio/separate');
};

// 指定布局
definePageMeta({
  layout: 'default' // 使用自定义布局
});
</script>

<style lang="scss">
.fade-enter-active {
  transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-active {
  opacity: 0;
}

.min-h-650 {
  min-height: 650px;
}

.gradient-header {
  color: #1ad37f;
  background-image: linear-gradient(0deg, #1ad37f 14%, #329ef4 55%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.gradient-underline {
  color: white;
}
</style>