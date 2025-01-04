<template>
  <v-app>
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">登录</span>
        </v-card-title>
        <v-card-text>
          <v-tabs v-model="tab" background-color="transparent">
            <v-tab>微信登录</v-tab>
            <v-tab>手机号登录</v-tab>
          </v-tabs>
          <v-tabs-items v-model="tab">
            <v-tab-item>
              <v-card>
                <v-card-text>
                  <v-btn @click="scanQRCode">扫描二维码登录</v-btn>
                  <v-img v-if="qrCodeUrl" :src="qrCodeUrl" class="qr-code" />
                </v-card-text>
              </v-card>
            </v-tab-item>
            <v-tab-item>
              <v-card>
                <v-card-text>
                  <v-text-field
                    v-model="phoneNumber"
                    label="手机号"
                    prepend-icon="mdi-phone"
                    type="tel"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="code"
                    label="验证码"
                    prepend-icon="mdi-key"
                    type="text"
                    required
                  ></v-text-field>
                  <v-btn @click="sendCode" :disabled="codeSent">发送验证码</v-btn>
                </v-card-text>
                <v-card-actions>
                  <v-btn @click="loginWithPhone">登录</v-btn>
                </v-card-actions>
              </v-card>
            </v-tab-item>
          </v-tabs-items>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="dialog = false">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-btn @click="dialog = true">打开登录弹窗</v-btn>
  </v-app>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';

@Component
export default class Login extends Vue {
  dialog: boolean = false;
  tab: number = 0; // 0: 微信登录, 1: 手机号登录
  qrCodeUrl: string | null = null; // 用于保存二维码 URL
  phoneNumber: string = '';
  code: string = '';
  codeSent: boolean = false; // 是否已发送验证码

  scanQRCode() {
    // 这里调用你的后端接口生成二维码 URL
    this.qrCodeUrl = 'https://example.com/path/to/qr-code'; // 替换为实际的二维码 URL
  }

  sendCode() {
    // 发送验证码的逻辑
    this.codeSent = true;
    // 这里可以添加你的 API 调用来发送验证码
    console.log(`发送验证码到 ${this.phoneNumber}`);
  }

  loginWithPhone() {
    // 手机号登录逻辑
    console.log(`手机号: ${this.phoneNumber}, 验证码: ${this.code}`);
    // 这里添加你的登录 API 调用
  }
}
</script>

<style scoped>
.qr-code {
  max-width: 100%;
  margin-top: 20px;
}
</style>
