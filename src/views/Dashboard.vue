<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useStatsStore, useProcessStore } from "@/stores";
import { useI18n } from "@/composables/useI18n";

const statsStore = useStatsStore();
const processStore = useProcessStore();
const { t } = useI18n();

interface StatCard {
  title: string;
  value: string | number;
  color: string;
}

const stats = ref<StatCard[]>([
  { title: "Skills", value: "...", color: "var(--primary)" },
  { title: t("models"), value: "...", color: "#a6e3a1" },
  { title: t("plugins"), value: "...", color: "#f38ba8" },
  { title: t("process"), value: "...", color: "#f9e2af" },
]);

onMounted(async () => {
  await Promise.all([statsStore.fetchOverview(), processStore.fetchStatus()]);
  stats.value = [
    { title: "Skills", value: statsStore.overview.user_skills + statsStore.overview.system_skills, color: "var(--primary)" },
    { title: t("models"), value: statsStore.overview.models, color: "#a6e3a1" },
    { title: t("plugins"), value: statsStore.overview.plugins, color: "#f38ba8" },
    { title: t("process"), value: processStore.status.running ? t("running") : t("stopped"), color: processStore.status.running ? "#a6e3a1" : "#f38ba8" },
  ];
});
</script>

<template>
  <div class="space-y-4">
    <div class="rounded-lg p-5" style="background-color: var(--surface); border: 1px solid var(--border);">
      <h2 class="text-lg font-semibold">{{ t("welcome") }}</h2>
      <p class="text-sm mt-1" style="color: var(--muted);">{{ t("welcomeDesc") }}</p>
    </div>

    <div class="grid grid-cols-4 gap-3">
      <div v-for="stat in stats" :key="stat.title" class="rounded-lg p-4" style="background-color: var(--surface); border: 1px solid var(--border);">
        <div class="text-xs uppercase" style="color: var(--muted);">{{ stat.title }}</div>
        <div class="text-2xl font-bold mt-1" :style="{ color: stat.color }">{{ stat.value }}</div>
      </div>
    </div>

    <div class="grid grid-cols-2 gap-3">
      <router-link to="/skills" class="flex items-center p-4 rounded-lg transition-colors" style="background-color: var(--surface); border: 1px solid var(--border);">
        <div class="w-8 h-8 rounded flex items-center justify-center mr-3" style="background-color: var(--primary); opacity: 0.2;">
          <svg class="w-4 h-4" style="color: var(--primary);" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" /></svg>
        </div>
        <div>
          <div class="text-sm font-medium">{{ t("skills") }}</div>
          <div class="text-xs" style="color: var(--muted);">{{ t("manageSkills") }}</div>
        </div>
      </router-link>

      <router-link to="/process" class="flex items-center p-4 rounded-lg transition-colors" style="background-color: var(--surface); border: 1px solid var(--border);">
        <div class="w-8 h-8 rounded flex items-center justify-center mr-3" style="background-color: #a6e3a1; opacity: 0.2;">
          <svg class="w-4 h-4" style="color: #a6e3a1;" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5.25 14.25h13.5m-13.5 0a3 3 0 01-3-3m3 3a3 3 0 100 6h13.5a3 3 0 100-6m-16.5-3a3 3 0 013-3h13.5a3 3 0 013 3m-19.5 0a4.5 4.5 0 01.9-2.7L5.737 5.1a3.375 3.375 0 012.7-1.35h7.126c1.062 0 2.062.5 2.7 1.35l2.587 3.45a4.5 4.5 0 01.9 2.7m0 0a3 3 0 01-3 3m0 3h.008v.008h-.008v-.008zm0-6h.008v.008h-.008v-.008zm-3 6h.008v.008h-.008v-.008zm0-6h.008v.008h-.008v-.008z" /></svg>
        </div>
        <div>
          <div class="text-sm font-medium">{{ t("process") }}</div>
          <div class="text-xs" style="color: var(--muted);">{{ t("manageProcess") }}</div>
        </div>
      </router-link>

      <router-link to="/config" class="flex items-center p-4 rounded-lg transition-colors" style="background-color: var(--surface); border: 1px solid var(--border);">
        <div class="w-8 h-8 rounded flex items-center justify-center mr-3" style="background-color: #f38ba8; opacity: 0.2;">
          <svg class="w-4 h-4" style="color: #f38ba8;" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17.25 6.75L22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3l-4.5 16.5" /></svg>
        </div>
        <div>
          <div class="text-sm font-medium">{{ t("config") }}</div>
          <div class="text-xs" style="color: var(--muted);">{{ t("manageConfig") }}</div>
        </div>
      </router-link>

      <router-link to="/logs" class="flex items-center p-4 rounded-lg transition-colors" style="background-color: var(--surface); border: 1px solid var(--border);">
        <div class="w-8 h-8 rounded flex items-center justify-center mr-3" style="background-color: #f9e2af; opacity: 0.2;">
          <svg class="w-4 h-4" style="color: #f9e2af;" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" /></svg>
        </div>
        <div>
          <div class="text-sm font-medium">{{ t("logs") }}</div>
          <div class="text-xs" style="color: var(--muted);">{{ t("manageLogs") }}</div>
        </div>
      </router-link>
    </div>
  </div>
</template>
