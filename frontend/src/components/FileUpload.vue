<template>
  <div
    class="upload-container"
    :style="{ width: width, height: height }"
    @click="triggerFileInput"
  >
    <input
      type="file"
      ref="fileInput"
      accept="audio/*"
      @change="handleFileChange"
      style="display: none;"
    />
    <v-icon class="upload-icon">mdi-plus</v-icon>
    <p>{{ uploadText }}</p>
  </div>
</template>

<script lang="ts" setup>
import { ref, defineProps } from 'vue';

// 定义组件的属性
const props = defineProps<{
  uploadText: string;
  width?: string;
  height?: string;
  onFileChange: (file: File) => void; // 定义传入的文件处理函数
}>();

const fileInput = ref<HTMLInputElement | null>(null);

// 触发文件输入框点击
const triggerFileInput = () => {
  fileInput.value?.click();
};

// 处理文件选择
const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const files = target.files;
  console.log(files)
  if (files && files.length > 0) {
    // 调用传入的 onFileChange 方法，并将文件对象传递给调用者
    props.onFileChange(files[0]);
  }
};
</script>

<style scoped>
.upload-container {
  border: 2px dashed #ccc;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  text-align: center;
}

.upload-icon {
  font-size: 48px;
  color: #ccc;
}
</style>
