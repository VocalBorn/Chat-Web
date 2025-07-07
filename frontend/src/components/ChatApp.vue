<template>
  <div style="padding: 2rem">
    <h1>Vue Chat App</h1>

    <!-- 👤 使用者名稱輸入 -->
    <div v-if="!username">
      <input v-model="tempName" placeholder="Enter your name" />
      <button @click="confirmName">Join Chat</button>
    </div>

    <!-- 💬 聊天室畫面 -->
    <div v-else>
      <div style="margin-bottom: 1rem">Hello, {{ username }} 👋</div>
      <div style="border: 1px solid #ccc; padding: 1rem; height: 200px; overflow-y: scroll;">
        <div v-for="(msg, index) in messages" :key="index">{{ msg }}</div>
      </div>
      <input v-model="input" @keyup.enter="sendMessage" />
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { io, Socket } from 'socket.io-client';

const socket: Socket = io('http://127.0.0.1:8000'); // 連接後端

const username = ref('');
const tempName = ref('');
const input = ref('');
const messages = ref<string[]>([]);

// 使用者輸入名稱並確認
function confirmName() {
  if (tempName.value.trim()) {
    username.value = tempName.value.trim();
  }
}

// 接收聊天訊息
onMounted(() => {
  socket.on('chat_message', (msg: string) => {
    console.log('📨 收到訊息：', msg);
    messages.value.push(msg);
  });

  socket.on('connect', () => {
    console.log('🟢 已連線');
  });
});

// 發送訊息時帶上使用者名稱
function sendMessage() {
  if (input.value.trim() && username.value) {
    socket.emit('chat_message', {
      user: username.value,
      message: input.value,
    });
    input.value = '';
  }
}
</script>
