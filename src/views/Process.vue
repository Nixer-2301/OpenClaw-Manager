<script setup lang="ts">
import { onMounted, onUnmounted, ref } from "vue";
import { useProcessStore } from "@/stores";
import { useI18n } from "@/composables/useI18n";

const store = useProcessStore();
const { t } = useI18n();
let refreshTimer: number | null = null;
const message = ref("");

onMounted(async () => { await refresh(); refreshTimer = window.setInterval(refresh, 5000); });
onUnmounted(() => { if (refreshTimer) clearInterval(refreshTimer); });

async function refresh() { await store.fetchStatus(); await store.fetchConfig(); }

async function handleStart() { await store.startProcess(); message.value = store.error || t("start"); setTimeout(() => message.value = "", 2000); }
async function handleStop() { await store.stopProcess(); message.value = store.error || t("stop"); setTimeout(() => message.value = "", 2000); }
async function handleRestart() { await store.restartProcess(); message.value = store.error || t("restart"); setTimeout(() => message.value = "", 2000); }
</script>

<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-bold tracking-tight" style="font-family: 'Syne', sans-serif;">{{ t("process") }}</h2>
      <span v-if="message" class="text-xs text-green-400">{{ message }}</span>
    </div>

    <div class="rounded-lg p-4" style="background-color: var(--surface); border: 1px solid var(--border);">
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center gap-2">
          <div :class="['w-2 h-2 rounded-full', store.status.running ? 'bg-green-400' : 'bg-red-400']" />
          <span class="text-sm">{{ store.status.running ? t("running") : t("stopped") }}</span>
        </div>
        <span class="text-xs" style="color: var(--muted);">{{ t("pid") }}: {{ store.status.pid || '-' }}</span>
      </div>

      <div class="grid grid-cols-4 gap-2 mb-3">
        <div class="rounded p-2" style="background-color: var(--bg);"><div class="text-[10px] uppercase" style="color: var(--muted);">{{ t("uptime") }}</div><div class="text-xs mt-1">{{ store.status.uptime || '-' }}</div></div>
        <div class="rounded p-2" style="background-color: var(--bg);"><div class="text-[10px] uppercase" style="color: var(--muted);">{{ t("port") }}</div><div class="text-xs mt-1">{{ store.config.port }}</div></div>
        <div class="rounded p-2" style="background-color: var(--bg);"><div class="text-[10px] uppercase" style="color: var(--muted);">{{ t("bind") }}</div><div class="text-xs mt-1">{{ store.config.bind }}</div></div>
        <div class="rounded p-2" style="background-color: var(--bg);"><div class="text-[10px] uppercase" style="color: var(--muted);">{{ t("auth") }}</div><div class="text-xs mt-1">{{ store.config.auth_mode }}</div></div>
      </div>

      <div class="flex gap-2">
        <button @click="handleStart" :disabled="store.status.running" class="px-3 py-1.5 text-xs rounded-md bg-green-600 text-white disabled:opacity-30">{{ t("start") }}</button>
        <button @click="handleStop" :disabled="!store.status.running" class="px-3 py-1.5 text-xs rounded-md bg-red-600 text-white disabled:opacity-30">{{ t("stop") }}</button>
        <button @click="handleRestart" :disabled="!store.status.running" class="px-3 py-1.5 text-xs rounded-md bg-yellow-600 text-white disabled:opacity-30">{{ t("restart") }}</button>
        <button @click="refresh()" class="px-3 py-1.5 text-xs rounded-md" style="background-color: var(--border); color: var(--text);">{{ t("refresh") }}</button>
      </div>
    </div>

    <div class="rounded-lg p-4 text-xs" style="background-color: var(--surface); border: 1px solid var(--border); color: var(--muted);">
      <p>{{ t("processInfo") }}</p>
      <p class="mt-1">{{ t("status") }}: <span :class="store.status.running ? 'text-green-400' : 'text-red-400'">{{ store.status.running ? t("running") : t("notDetected") + ' ' + store.config.port }}</span></p>
    </div>
  </div>
</template>
