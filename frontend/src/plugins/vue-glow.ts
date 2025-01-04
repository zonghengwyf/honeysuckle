// src/plugins/vue-glow.ts
import { defineNuxtPlugin } from '#app';
import VueGlow from 'vue-glow';

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.component('VueGlow', VueGlow);
});