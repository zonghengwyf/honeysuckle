import { defineNuxtPlugin } from '#app'
import { $fetch } from 'ofetch'

export default defineNuxtPlugin((nuxtApp) => {
  const config = useRuntimeConfig().public

  // 创建一个自定义的 fetch 函数
  const apiFetch = async (endpoint: string, options = {}) => {
    return await $fetch(`${config.baseURL}${endpoint}`, options)
  }

  // 将 apiFetch 方法添加到 nuxtApp
  nuxtApp.provide('apiFetch', apiFetch)
})
