<script setup lang="ts">
import { onMounted } from "vue";
import { usePluginsStore } from "@/stores";
import { useI18n } from "@/composables/useI18n";

const store = usePluginsStore();
const { t } = useI18n();

onMounted(() => store.fetchPlugins());
</script>

<template>
  <div class="space-y-4">
    <div>
      <h2 class="text-xl font-bold tracking-tight" style="font-family: 'Syne', sans-serif;">{{ t("plugins") }}</h2>
      <p class="text-xs mt-1" style="color: var(--muted);">{{ store.plugins.length }} {{ t("plugins") }}</p>
    </div>

    <div v-if="store.loading" class="text-center py-8"><div class="animate-spin rounded-full h-6 w-6 border-b-2 mx-auto" style="border-color: var(--primary);"></div><p class="text-xs mt-2" style="color: var(--muted);">{{ t("loading") }}</p></div>
    <div v-else-if="store.plugins.length === 0" class="rounded-lg p-8 text-center text-sm" style="background-color: var(--surface); border: 1px solid var(--border); color: var(--muted);">{{ t("noPlugins") }}</div>
    <div v-else class="space-y-2">
      <div v-for="plugin in store.plugins" :key="plugin.name" class="rounded-lg p-3 flex items-center justify-between" style="background-color: var(--surface); border: 1px solid var(--border);">
        <div class="flex-1">
          <div class="flex items-center gap-2">
            <span class="text-sm font-medium">{{ plugin.name }}</span>
            <span class="text-xs" style="color: var(--muted);">{{ plugin.version || 'v1.0' }}</span>
          </div>
          <div class="text-xs mt-0.5" style="color: var(--muted);">{{ plugin.description || '-' }}</div>
        </div>
        <div class="flex items-center gap-2">
          <span :class="['text-xs', plugin.enabled ? 'text-green-400' : 'text-red-400']">{{ plugin.enabled ? t("on") : t("off") }}</span>
          <button @click="store.togglePlugin(plugin.name)" class="px-2 py-1 text-xs rounded-md" style="background-color: var(--border); color: var(--text);">{{ plugin.enabled ? t("off") : t("on") }}</button>
        </div>
      </div>
    </div>
  </div>
</template>
