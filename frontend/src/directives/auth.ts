import { DirectiveBinding, getCurrentInstance } from 'vue';
import { useAuthStore } from '@/stores/index'; // 引入 Pinia store

const authDirective = {
  beforeMount(el: HTMLElement, binding: DirectiveBinding) {
    const authStore = useAuthStore();
    const requiredPermission = binding.value; // 获取所需的权限
    const instance = getCurrentInstance(); // 获取当前实例

    // 添加点击事件
    el.addEventListener('click', (event) => {
      event.stopImmediatePropagation();

      // 检查用户是否登录
      if (!authStore.isLoggedIn) {
        // 获取 loginDialog 的引用
        const loginDialog = instance?.appContext.provides.loginDialog;
        console.log("33333333333333333")
        console.log(loginDialog)
        if (loginDialog && loginDialog.value) {
          loginDialog.value.visible = true; // 显示登录弹框
        }
      } else {
        // 如果已经登录，执行与按钮相关的操作
        // 例如，调用与按钮相关的回调或方法
        console.log('用户已登录，执行相关操作');
      }
    });
  },
};

export default authDirective;