import { defineNuxtConfig } from 'nuxt/config'
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify';

export default defineNuxtConfig({
  // Global page headers
  srcDir: "src",

  app: {
    head: {
      titleTemplate: '%s',
      title: '金银花-音轨分离',
      htmlAttrs: {
        lang: 'zh',
      },
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { hid: 'description', name: 'description', content: '金银花-音轨分离' },
        { name: 'format-detection', content: 'telephone=no' },
        { hid: 'twitter:site', name: 'twitter:site', content: '@NdoleStudio' },
        { hid: 'twitter:card', name: 'twitter:card', content: 'summary_large_image' },
        { hid: 'og:title', name: 'og:title', content: '金银花-音轨分离' },
        { hid: 'og:description', name: 'og:description', content: '金银花-音轨分离' },
        { hid: 'og:image', name: 'og:image', content: '金银花-音轨分离' },
      ],
      link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
    },
  },

  // Global CSS
  css: [],

  // Plugins
  plugins: [
    '~/plugins/pinia.ts',
    '~/plugins/auth.ts',
    '~/plugins/http.ts',
    { src: '~/plugins/vue-glow', mode: 'client' },
    { src: '~/plugins/chart', mode: 'client' },
  ],

  // Auto import components
  components: true,

  // Modules
  modules: [
      (_options, nuxt) => {
      nuxt.hooks.hook('vite:extendConfig', (config) => {
        // @ts-expect-error
        config.plugins.push(vuetify({ autoImport: true }))
      })
    },
    '@nuxtjs/sitemap',
  ],

  runtimeConfig: {
    public: {
      baseURL: process.env.API_BASE_URL // 确保你的 BASE_URL 在这里配置
    }
  },

  // Vuetify module configuration
  vuetify: {
    treeShake: true,
    customVariables: ['~/assets/variables.scss'],
    defaultAssets: {
      icons: 'mdiSvg',
    },
    theme: {
      dark: true,
    },
  },

  // Sitemap configuration
  sitemap: {
    hostname: 'http://www.aiznbs.com',
    gzip: true,
    trailingSlash: true,
    exclude: [
      '/messages',
      '/settings',
      '/threads**',
      '/billing',
      '/bulk-messages',
    ],
  },

  publicRuntimeConfig: {
    apiBaseUrl: process.env.API_URL,
  },

  // Build Configuration
  build: {
    transpile: ['vuetify', 'chart.js', 'vue-chartjs'],
  },

  // Vite configuration
  vite: {
    vue: {
      template: {
        transformAssetUrls,
      },
    },
    css: {
      preprocessorOptions: {
        scss: {
          api: 'modern-compiler' // or "modern"
        }
      }
    }
  },

  // Server configuration
  server: {
    host: '0.0.0.0',
    port: 3000,
  },
});