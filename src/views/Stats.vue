<script setup lang="ts">
import { onMounted, ref, computed } from "vue";
import { useStatsStore } from "@/stores";
import { useI18n } from "@/composables/useI18n";

const store = useStatsStore();
const { t } = useI18n();
const dateRange = ref(7);

const chartData = computed(() => Object.entries(store.dailyStats).sort(([a],[b]) => a.localeCompare(b)).map(([date, count]) => ({ label: date.slice(5), value: count })));

onMounted(async () => await Promise.all([store.fetchOverview(), store.fetchDailyStats(dateRange.value)]));
const updateRange = async (days: number) => { dateRange.value = days; await store.fetchDailyStats(days); };
</script>

<template>
  <div class="space-y-4">
    <h2 class="text-xl font-bold tracking-tight" style="font-family: 'Syne', sans-serif;">{{ t("stats") }}</h2>

    <div class="grid grid-cols-3 gap-3">
      <div class="rounded-lg p-4" style="background-color: var(--surface); border: 1px solid var(--border);"><div class="text-xs uppercase" style="color: var(--muted);">{{ t("sessions") }}</div><div class="text-2xl font-bold mt-1" style="color: var(--primary);">{{ store.overview.sessions }}</div></div>
      <div class="rounded-lg p-4" style="background-color: var(--surface); border: 1px solid var(--border);"><div class="text-xs uppercase" style="color: var(--muted);">{{ t("skills") }}</div><div class="text-2xl font-bold mt-1 text-green-400">{{ store.overview.user_skills + store.overview.system_skills }}</div></div>
      <div class="rounded-lg p-4" style="background-color: var(--surface); border: 1px solid var(--border);"><div class="text-xs uppercase" style="color: var(--muted);">{{ t("models") }}</div><div class="text-2xl font-bold mt-1 text-yellow-400">{{ store.overview.models }}</div></div>
    </div>

    <div class="flex gap-2">
      <button v-for="d in [7, 30, 90]" :key="d" @click="updateRange(d)" class="px-3 py-1 text-xs rounded-md" :style="{ backgroundColor: dateRange === d ? 'var(--primary)' : 'var(--border)', color: dateRange === d ? '#ffffff' : 'var(--text)' }">{{ d }}d</button>
    </div>

    <div class="rounded-lg overflow-hidden" style="background-color: var(--surface); border: 1px solid var(--border);">
      <div class="px-4 py-2 text-xs uppercase" style="border-bottom: 1px solid var(--border); color: var(--muted);">{{ t("dailySessions") }}</div>
      <div v-if="chartData.length === 0" class="p-8 text-center text-sm" style="color: var(--muted);">{{ t("noData") }}</div>
      <table v-else class="w-full">
        <thead><tr style="border-bottom: 1px solid var(--border);"><th class="px-4 py-2 text-left text-xs uppercase" style="color: var(--muted);">{{ t("date") }}</th><th class="px-4 py-2 text-left text-xs uppercase" style="color: var(--muted);">{{ t("sessions_") }}</th></tr></thead>
        <tbody><tr v-for="item in chartData" :key="item.label" style="border-bottom: 1px solid var(--border);"><td class="px-4 py-2 text-xs" style="color: var(--muted);">{{ item.label }}</td><td class="px-4 py-2 text-xs">{{ item.value }}</td></tr></tbody>
      </table>
    </div>
  </div>
</template>
