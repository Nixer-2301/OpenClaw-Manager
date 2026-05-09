<script setup lang="ts">
import { onMounted } from "vue";
import { useModelsStore } from "@/stores";
import { useI18n } from "@/composables/useI18n";

const store = useModelsStore();
const { t } = useI18n();

onMounted(() => store.fetchModels());
</script>

<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-xl font-bold tracking-tight" style="font-family: 'Syne', sans-serif;">{{ t("models") }}</h2>
        <p class="text-xs mt-1" style="color: var(--muted);">{{ store.models.length }} {{ t("models") }}</p>
      </div>
    </div>

    <div v-if="store.loading" class="text-center py-8"><div class="animate-spin rounded-full h-6 w-6 border-b-2 mx-auto" style="border-color: var(--primary);"></div><p class="text-xs mt-2" style="color: var(--muted);">{{ t("loading") }}</p></div>
    <div v-else-if="store.models.length === 0" class="rounded-lg p-8 text-center text-sm" style="background-color: var(--surface); border: 1px solid var(--border); color: var(--muted);">{{ t("noModels") }}</div>
    <div v-else class="grid grid-cols-2 gap-3">
      <div v-for="model in store.models" :key="`${model.provider}/${model.id}`" class="rounded-lg p-4" style="background-color: var(--surface); border: 1px solid var(--border);">
        <div class="flex justify-between mb-2">
          <div>
            <div class="text-sm font-medium">{{ model.name }}</div>
            <div class="text-xs" style="color: var(--muted);">{{ t("modelProvider") }}: {{ model.provider }} / {{ t("modelId") }}: {{ model.id }}</div>
          </div>
          <span v-if="model.reasoning" class="px-1.5 py-0.5 text-xs rounded" style="background-color: var(--border); color: var(--primary);">{{ t("reasoning") }}</span>
        </div>
        <div class="text-xs mb-3" style="color: var(--muted);">
          <div>{{ t("context") }}: {{ model.context_window.toLocaleString() }}</div>
          <div>{{ t("maxTokens") }}: {{ model.max_tokens.toLocaleString() }}</div>
        </div>
        <button @click="store.deleteModel(model.provider, model.id)" class="text-xs text-red-400">{{ t("del") }}</button>
      </div>
    </div>
  </div>
</template>
