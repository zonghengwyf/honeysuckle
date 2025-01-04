// middleware/auth.ts
import { Context, Middleware } from '@nuxt/types';

const authMiddleware: Middleware = (context: Context) => {
  // 检查用户是否已登录
  if (!context.store.getters.getAuthUser) {
    // 显示登录对话框
    context.store.commit('showLoginDialog', true);

    // 可选：重定向到首页或其他页面
  }
};

export default authMiddleware;
