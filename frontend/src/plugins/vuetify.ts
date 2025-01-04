import { createVuetify } from 'vuetify';
import 'vuetify/styles'; // 引入 Vuetify 样式
import "@mdi/font/css/materialdesignicons.css";
import { aliases, mdi } from "vuetify/iconsets/mdi";

export default defineNuxtPlugin((nuxtApp) => {
  const vuetify = createVuetify({
    icons: {
      defaultSet: "mdi",
      aliases,
      sets: {
        mdi,
      },
    },
  }); // 创建 Vuetify 实例
  nuxtApp.vueApp.use(vuetify); // 将 Vuetify 应用到 Vue 应用中
});