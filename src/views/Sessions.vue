<script setup lang="ts">
import { onMounted, onUnmounted } from "vue";
import { useSessionsStore } from "@/stores";
import { useI18n } from "@/composables/useI18n";

const store = useSessionsStore();
const { t } = useI18n();
let refreshTimer: number | null = null;

onMounted(async () => { await store.fetchConnectionStatus(); if (store.connectionStatus.connected) await store.fetchSessions(); refreshTimer = window.setInterval(() => store.fetchConnectionStatus(), 10000); });
onUnmounted(() => { if (refreshTimer) clearInterval(refreshTimer); });

const handleTest = async () => { const ok = await store.testConnection(); if (ok) await store.fetchSessions(); };
</script>

<template>
  <div class="space-y-4">
    <h2 class="text-xl font-bold tracking-tight" style="font-family: 'Syne', sans-serif;">{{ t("sessions") }}</h2>

    <div class="rounded-lg p-4" style="background-color: var(--surface); border: 1px solid var(--border);">
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center gap-2">
          <div :class="['w-2 h-2 rounded-full', store.connectionStatus.connected ? 'bg-green-400' : 'bg-red-400']" />
          <span class="text-sm">{{ store.connectionStatus.connected ? t("connected") : t("disconnected") }}</span>
        </div>
        <button @click="handleTest" class="px-2 py-1 text-xs rounded-md" style="background-color: var(--border); color: var(--text);">{{ t("test") }}</button>
      </div>
      <div class="text-xs" style="color: var(--muted);">{{ t("server") }}: {{ store.connectionStatus.server || '-' }}</div>
    </div>

    <div v-if="store.connectionStatus.connected" class="rounded-lg p-4" style="background-color: var(--surface); border: 1px solid var(--border);">
      <div class="text-xs uppercase mb-2" style="color: var(--muted);">{{ t("sessions") }}</div>
      <div v-if="store.loading" class="text-center py-4"><div class="animate-spin rounded-full h-6 w-6 border-b-2 mx-auto" style="border-color: var(--primary);"></div><p class="text-xs mt-2" style="color: var(--muted);">{{ t("loading") }}</p></div>
      <div v-else-if="Array.isArray(store.sessions) && store.sessions.length === 0" class="text-center py-4 text-sm" style="color: var(--muted);">{{ t("noSessions") }}</div>
      <div v-else class="rounded p-3 overflow-auto max-h-48 text-xs" style="background-color: var(--bg); color: var(--muted);"><pre>{{ JSON.stringify(store.sessions, null, 2) }}</pre></div>
    </div>
  </div>
</template>
