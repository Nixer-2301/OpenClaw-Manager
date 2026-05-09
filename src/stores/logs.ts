import { defineStore } from "pinia";
import { ref } from "vue";
import { call } from "@/bridge";

export interface LogFile { name: string; path: string; }
export interface LogStats { total: number; info: number; warn: number; error: number; }

export const useLogsStore = defineStore("logs", () => {
  const logFiles = ref<LogFile[]>([]);
  const currentFile = ref<string | null>(null);
  const logContent = ref<string[]>([]);
  const logStats = ref<LogStats>({ total: 0, info: 0, warn: 0, error: 0 });
  const levelFilter = ref("ALL");
  const searchKeyword = ref("");
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function fetchLogFiles() {
    loading.value = true; error.value = null;
    try { logFiles.value = (await call("logs.getFiles")) as LogFile[]; }
    catch (e) { error.value = (e as Error).message; }
    finally { loading.value = false; }
  }

  async function fetchLogContent(filePath: string) {
    loading.value = true; currentFile.value = filePath;
    try { logContent.value = (await call("logs.read", { file: filePath, level: levelFilter.value, keyword: searchKeyword.value })) as string[]; }
    catch (e) { error.value = (e as Error).message; }
    finally { loading.value = false; }
  }

  async function fetchLogStats(filePath: string) {
    try { logStats.value = (await call("logs.getStats", { file: filePath })) as LogStats; }
    catch (e) { error.value = (e as Error).message; }
  }

  return { logFiles, currentFile, logContent, logStats, levelFilter, searchKeyword, loading, error, fetchLogFiles, fetchLogContent, fetchLogStats };
});
