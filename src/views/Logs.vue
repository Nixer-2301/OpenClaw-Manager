<script setup lang="ts">
import { onMounted, watch } from "vue";
import { useLogsStore } from "@/stores";
import { useI18n } from "@/composables/useI18n";

const store = useLogsStore();
const { t } = useI18n();

onMounted(() => store.fetchLogFiles());

watch(() => store.currentFile, (f) => { if (f) { store.fetchLogContent(f); store.fetchLogStats(f); } });
watch(() => [store.levelFilter, store.searchKeyword], () => { if (store.currentFile) store.fetchLogContent(store.currentFile); });
</script>

<template>
  <div class="space-y-4">
    <h2 class="text-xl font-bold tracking-tight" style="font-family: 'Syne', sans-serif;">{{ t("logs") }}</h2>

    <div class="flex gap-2">
      <select v-model="store.currentFile" class="px-2 py-1.5 text-sm rounded-md" style="background-color: var(--input-bg); border: 1px solid var(--border); color: var(--text);">
        <option :value="null">{{ t("selectFile") }}</option>
        <option v-for="f in store.logFiles" :key="f.path" :value="f.path">{{ f.name }}</option>
      </select>
      <select v-model="store.levelFilter" class="px-2 py-1.5 text-sm rounded-md" style="background-color: var(--input-bg); border: 1px solid var(--border); color: var(--text);">
        <option value="ALL">{{ t("all") }}</option>
        <option value="INFO">{{ t("info") }}</option>
        <option value="WARN">{{ t("warn") }}</option>
        <option value="ERROR">{{ t("error") }}</option>
      </select>
      <input v-model="store.searchKeyword" :placeholder="t('search')" class="flex-1 px-2 py-1.5 text-sm rounded-md" style="background-color: var(--input-bg); border: 1px solid var(--border); color: var(--text);" />
    </div>

    <div v-if="store.currentFile" class="flex gap-4 text-xs" style="color: var(--muted);">
      <span>{{ t("total") }}: {{ store.logStats.total }}</span>
      <span class="text-green-400">{{ t("info") }}: {{ store.logStats.info }}</span>
      <span class="text-yellow-400">{{ t("warn") }}: {{ store.logStats.warn }}</span>
      <span class="text-red-400">{{ t("error") }}: {{ store.logStats.error }}</span>
    </div>

    <div v-if="store.loading" class="text-center py-8"><div class="animate-spin rounded-full h-6 w-6 border-b-2 mx-auto" style="border-color: var(--primary);"></div><p class="text-xs mt-2" style="color: var(--muted);">{{ t("loading") }}</p></div>
    <div v-else-if="!store.currentFile" class="rounded-lg p-8 text-center text-sm" style="background-color: var(--surface); border: 1px solid var(--border); color: var(--muted);">{{ t("noLogs") }}</div>
    <div v-else class="rounded-lg overflow-hidden" style="background-color: var(--surface); border: 1px solid var(--border);">
      <div class="p-3 h-72 overflow-y-auto text-xs" style="background-color: var(--bg);">
        <div v-if="store.logContent.length === 0" style="color: var(--muted);">{{ t("noData") }}</div>
        <div v-for="(line, i) in store.logContent" :key="i" class="whitespace-pre-wrap leading-relaxed" style="color: var(--muted);">{{ line }}</div>
      </div>
    </div>
  </div>
</template>
