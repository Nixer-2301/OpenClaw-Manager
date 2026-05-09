import { defineStore } from "pinia";
import { ref } from "vue";
import { call } from "@/bridge";

export interface Overview { sessions: number; user_skills: number; system_skills: number; models: number; plugins: number; }

export const useStatsStore = defineStore("stats", () => {
  const overview = ref<Overview>({ sessions: 0, user_skills: 0, system_skills: 0, models: 0, plugins: 0 });
  const dailyStats = ref<Record<string, number>>({});
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function fetchOverview() {
    loading.value = true; error.value = null;
    try { overview.value = (await call("stats.getOverview")) as Overview; }
    catch (e) { error.value = (e as Error).message; }
    finally { loading.value = false; }
  }

  async function fetchDailyStats(days = 7) {
    try { dailyStats.value = (await call("stats.getDaily", { days })) as Record<string, number>; }
    catch (e) { error.value = (e as Error).message; }
  }

  return { overview, dailyStats, loading, error, fetchOverview, fetchDailyStats };
});
