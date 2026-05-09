import { defineStore } from "pinia";
import { ref } from "vue";
import { call } from "@/bridge";

export interface ProcessStatus {
  running: boolean;
  pid: number | null;
  start_time: string | null;
  uptime: string | null;
}

export interface ProcessConfig {
  port: number; bind: string; auth_mode: string; mode: string;
}

export const useProcessStore = defineStore("process", () => {
  const status = ref<ProcessStatus>({ running: false, pid: null, start_time: null, uptime: null });
  const config = ref<ProcessConfig>({ port: 18789, bind: "loopback", auth_mode: "token", mode: "local" });
  const logs = ref<string[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function fetchStatus() {
    try { status.value = (await call("process.getStatus")) as ProcessStatus; }
    catch (e) { error.value = (e as Error).message; }
  }

  async function fetchConfig() {
    try { config.value = (await call("process.getConfig")) as ProcessConfig; }
    catch (e) { error.value = (e as Error).message; }
  }

  async function fetchLogs(lines = 100) {
    try { logs.value = (await call("process.getLogs", { lines })) as string[]; }
    catch (e) { error.value = (e as Error).message; }
  }

  async function startProcess() { loading.value = true; try { const r = (await call("process.start")) as { success: boolean; message: string }; if (!r.success) error.value = r.message; await fetchStatus(); } catch (e) { error.value = (e as Error).message; } finally { loading.value = false; } }
  async function stopProcess() { loading.value = true; try { const r = (await call("process.stop")) as { success: boolean; message: string }; if (!r.success) error.value = r.message; await fetchStatus(); } catch (e) { error.value = (e as Error).message; } finally { loading.value = false; } }
  async function restartProcess() { loading.value = true; try { const r = (await call("process.restart")) as { success: boolean; message: string }; if (!r.success) error.value = r.message; await fetchStatus(); } catch (e) { error.value = (e as Error).message; } finally { loading.value = false; } }

  return { status, config, logs, loading, error, fetchStatus, fetchConfig, fetchLogs, startProcess, stopProcess, restartProcess };
});
