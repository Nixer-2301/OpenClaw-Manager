<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useConfigStore } from "@/stores";
import { useI18n } from "@/composables/useI18n";

const store = useConfigStore();
const { t } = useI18n();
const message = ref("");

onMounted(() => { store.fetchConfig(); store.fetchBackups(); });

const handleSave = async () => { try { await store.saveConfig(); message.value = "OK"; setTimeout(() => message.value = "", 2000); } catch { message.value = "Err"; setTimeout(() => message.value = "", 2000); } };
</script>

<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-bold tracking-tight" style="font-family: 'Syne', sans-serif;">{{ t("config") }}</h2>
      <div class="flex items-center gap-2">
        <span v-if="message" class="text-xs" style="color: var(--primary);">{{ message }}</span>
        <button @click="store.validateConfig()" class="px-2 py-1 text-xs rounded-md" style="background-color: var(--border); color: var(--text);">{{ t("validate") }}</button>
        <button @click="store.formatConfig()" class="px-2 py-1 text-xs rounded-md" style="background-color: var(--border); color: var(--text);">{{ t("format") }}</button>
        <button @click="store.createBackup()" class="px-2 py-1 text-xs rounded-md" style="background-color: var(--border); color: var(--text);">{{ t("backup") }}</button>
        <button @click="handleSave" class="px-2 py-1 text-xs rounded-md font-medium" style="background-color: var(--primary); color: #ffffff;">{{ t("save") }}</button>
      </div>
    </div>

    <div v-if="store.isValid !== null" class="rounded p-2 text-xs" :style="{ backgroundColor: 'var(--bg)', color: store.isValid ? '#a6e3a1' : '#f38ba8' }">{{ store.validationMessage }}</div>

    <div class="rounded-lg overflow-hidden" style="background-color: var(--surface); border: 1px solid var(--border);">
      <div class="px-3 py-1.5 text-xs" style="border-bottom: 1px solid var(--border); color: var(--muted);">{{ t("openclawJson") }}</div>
      <textarea v-model="store.content" class="w-full h-72 p-3 text-xs font-mono" style="background-color: var(--bg); color: var(--text); resize: none;" spellcheck="false"></textarea>
    </div>

    <div v-if="store.backups.length > 0" class="rounded-lg p-3" style="background-color: var(--surface); border: 1px solid var(--border);">
      <div class="text-xs uppercase mb-2" style="color: var(--muted);">{{ t("backups") }}</div>
      <div class="space-y-1">
        <div v-for="b in store.backups" :key="b.path" class="flex items-center justify-between p-2 rounded" style="background-color: var(--bg);">
          <span class="text-xs" style="color: var(--muted);">{{ b.name }}</span>
          <button @click="store.restoreBackup(b.path)" class="text-xs" style="color: var(--primary);">{{ t("restore") }}</button>
        </div>
      </div>
    </div>
  </div>
</template>
