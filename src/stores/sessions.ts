import { defineStore } from "pinia";
import { ref } from "vue";
import { call } from "@/bridge";

export interface ConnectionStatus { connected: boolean; server: string; }

export const useSessionsStore = defineStore("sessions", () => {
  const connectionStatus = ref<ConnectionStatus>({ connected: false, server: "" });
  const sessions = ref<unknown[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function fetchConnectionStatus() {
    try { connectionStatus.value = (await call("sessions.getStatus")) as ConnectionStatus; }
    catch (e) { error.value = (e as Error).message; }
  }

  async function testConnection() {
    try { return (await call("sessions.testConnection")) as boolean; }
    catch (e) { error.value = (e as Error).message; return false; }
  }

  async function fetchSessions() {
    loading.value = true; error.value = null;
    try { sessions.value = (await call("sessions.getAll")) as unknown[]; }
    catch (e) { error.value = (e as Error).message; }
    finally { loading.value = false; }
  }

  return { connectionStatus, sessions, loading, error, fetchConnectionStatus, testConnection, fetchSessions };
});
