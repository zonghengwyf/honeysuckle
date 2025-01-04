import { defineNuxtPlugin } from '#app';
import { DirectiveBinding } from 'vue';
import { useUserStore } from '@/stores/index';

const vAuth = {
  clickHandler: null as ((event: MouseEvent) => void) | null,

  handleClick(el: HTMLElement, binding: DirectiveBinding) {
    const userStore = useUserStore();
    return (event: MouseEvent) => {
      event.preventDefault();
      if (!userStore.isLoggedIn) {
        userStore.showLoginDialog = true; // 显示登录对话框
      } else {
        // 如果已登录，执行绑定的函数
        if (binding.value && typeof binding.value === 'function') {
          binding.value();
        }
      }
    };
  },

  beforeMount(el: HTMLElement, binding: DirectiveBinding) {
    const userStore = useUserStore();
    vAuth.clickHandler = vAuth.handleClick(el, binding);

    el.addEventListener('click', vAuth.clickHandler);

    // 监听用户状态变化
    userStore.$subscribe(() => {
      if (userStore.isLoggedIn) {
        el.removeEventListener('click', vAuth.clickHandler);
        el.addEventListener('click', binding.value);
      } else {
        el.removeEventListener('click', binding.value);
        el.addEventListener('click', vAuth.clickHandler);
      }
    });
  },

  unmounted(el: HTMLElement) {
    if (vAuth.clickHandler) {
      el.removeEventListener('click', vAuth.clickHandler);
    }
  },
};

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.directive('auth', vAuth);
});