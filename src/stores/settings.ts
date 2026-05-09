import { defineStore } from "pinia";
import { ref } from "vue";
import { call } from "@/bridge";

export interface AllSettings {
  general: { default_tab: number; auto_refresh: boolean; confirm_delete: boolean; confirm_batch: boolean };
  paths: { openclaw_dir: string; user_skills_dir: string; backup_dir: string; max_backups: number };
  interface: { theme: string; font_size: number; table_row_height: number };
  file_watcher: { enabled: boolean; refresh_interval: number };
}

export const useSettingsStore = defineStore("settings", () => {
  const settings = ref<AllSettings>({
    general: { default_tab: 0, auto_refresh: true, confirm_delete: true, confirm_batch: true },
    paths: { openclaw_dir: "", user_skills_dir: "", backup_dir: "", max_backups: 10 },
    interface: { theme: "dark", font_size: 10, table_row_height: 30 },
    file_watcher: { enabled: true, refresh_interval: 5 },
  });
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function fetchSettings() {
    loading.value = true; error.value = null;
    try { settings.value = (await call("settings.getAll")) as AllSettings; }
    catch (e) { error.value = (e as Error).message; }
    finally { loading.value = false; }
  }

  async function saveSettings() {
    loading.value = true; error.value = null;
    try { await call("settings.save", settings.value as unknown as Record<string, unknown>); }
    catch (e) { error.value = (e as Error).message; throw e; }
    finally { loading.value = false; }
  }

  async function resetSettings() {
    loading.value = true; error.value = null;
    try { settings.value = (await call("settings.reset")) as AllSettings; }
    catch (e) { error.value = (e as Error).message; }
    finally { loading.value = false; }
  }

  function applyTheme() {
    const isDark = settings.value.interface.theme === "dark";
    document.documentElement.classList.toggle("dark", isDark);
    localStorage.setItem("theme", settings.value.interface.theme);
  }

  return { settings, loading, error, fetchSettings, saveSettings, resetSettings, applyTheme };
});
