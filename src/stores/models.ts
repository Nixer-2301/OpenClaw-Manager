import { defineStore } from "pinia";
import { ref } from "vue";
import { call } from "@/bridge";

export interface Model {
  provider: string; id: string; name: string; api: string; enabled: boolean;
  base_url: string; context_window: number; max_tokens: number; reasoning: boolean;
}

export const useModelsStore = defineStore("models", () => {
  const models = ref<Model[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function fetchModels() {
    loading.value = true; error.value = null;
    try { models.value = (await call("models.getAll")) as Model[]; }
    catch { models.value = []; }
    finally { loading.value = false; }
  }

  async function addModel(model: Record<string, unknown>) {
    try { models.value = (await call("models.add", model)) as Model[]; }
    catch (e) { error.value = (e as Error).message; throw e; }
  }

  async function deleteModel(provider: string, id: string) {
    try { models.value = (await call("models.delete", { provider, id })) as Model[]; }
    catch (e) { error.value = (e as Error).message; throw e; }
  }

  return { models, loading, error, fetchModels, addModel, deleteModel };
});
