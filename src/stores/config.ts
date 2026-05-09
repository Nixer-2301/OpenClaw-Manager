import { defineStore } from "pinia";
import { ref } from "vue";
import { call } from "@/bridge";

export interface Backup { path: string; name: string; time: string; }

export const useConfigStore = defineStore("config", () => {
  const content = ref("");
  const backups = ref<Backup[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const validationMessage = ref<string | null>(null);
  const isValid = ref<boolean | null>(null);

  async function fetchConfig() {
    loading.value = true; error.value = null;
    try { content.value = (await call("config.read")) as string; }
    catch (e) { error.value = (e as Error).message; }
    finally { loading.value = false; }
  }

  async function saveConfig() {
    try { await call("config.save", { content: content.value }); }
    catch (e) { error.value = (e as Error).message; throw e; }
  }

  async function validateConfig() {
    try { const r = (await call("config.validate", { content: content.value })) as { valid: boolean; message: string }; isValid.value = r.valid; validationMessage.value = r.message; }
    catch (e) { error.value = (e as Error).message; }
  }

  async function formatConfig() {
    content.value = JSON.stringify(JSON.parse(content.value), null, 2);
  }

  async function createBackup() {
    try { await call("config.backup"); await fetchBackups(); }
    catch (e) { error.value = (e as Error).message; }
  }

  async function fetchBackups() {
    try { backups.value = (await call("config.listBackups")) as Backup[]; }
    catch (e) { error.value = (e as Error).message; }
  }

  async function restoreBackup(path: string) {
    try { await call("config.restore", { path }); await fetchConfig(); }
    catch (e) { error.value = (e as Error).message; }
  }

  return { content, backups, loading, error, validationMessage, isValid, fetchConfig, saveConfig, validateConfig, formatConfig, createBackup, fetchBackups, restoreBackup };
});
