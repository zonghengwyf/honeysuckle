import { ref, watch } from 'vue';
import { useDisplay } from 'vuetify';

export const useBreakpoint = () => {
  const { lgAndUp, mdAndDown, mdAndUp, smAndDown, mdOnly } = useDisplay();

  const isLgAndUp = ref<boolean>(lgAndUp);
  const isMdAndDown = ref<boolean>(mdAndDown);
  const isMdAndUp = ref<boolean>(mdAndUp);
  const isSmAndDown = ref<boolean>(smAndDown);
  const isMdOnly = ref<boolean>(mdOnly);

  // 监听变化
  watch(() => lgAndUp, (val) => isLgAndUp.value = val);
  watch(() => mdAndDown, (val) => isMdAndDown.value = val);
  watch(() => mdAndUp, (val) => isMdAndUp.value = val);
  watch(() => smAndDown, (val) => isSmAndDown.value = val);
  watch(() => mdOnly, (val) => isMdOnly.value = val);

  return { isLgAndUp, isMdAndDown, isMdAndUp, isSmAndDown, isMdOnly };
};