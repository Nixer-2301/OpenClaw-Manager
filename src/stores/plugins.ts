import { defineStore } from "pinia";
import { ref } from "vue";
import { call } from "@/bridge";

export interface Plugin {
  name: string; description: string; version: string; enabled: boolean; path: string;
}

export const usePluginsStore = defineStore("plugins", () => {
  const plugins = ref<Plugin[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function fetchPlugins() {
    loading.value = true; error.value = null;
    try { plugins.value = (await call("plugins.getAll")) as Plugin[]; }
    catch { plugins.value = []; }
    finally { loading.value = false; }
  }

  async function togglePlugin(name: string) {
    try { plugins.value = (await call("plugins.toggle", { name })) as Plugin[]; }
    catch (e) { error.value = (e as Error).message; throw e; }
  }

  return { plugins, loading, error, fetchPlugins, togglePlugin };
});
