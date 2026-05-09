<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useSkillsStore } from "@/stores";
import { useI18n } from "@/composables/useI18n";

const store = useSkillsStore();
const { t } = useI18n();
const fileInput = ref<HTMLInputElement | null>(null);

onMounted(() => store.fetchSkills());

function handleFile(file: File) {
  const reader = new FileReader();
  reader.onload = () => {
    const base64 = (reader.result as string).split(",")[1];
    store.importSkill(base64);
  };
  reader.readAsDataURL(file);
}

const onFileDrop = (e: DragEvent) => {
  e.preventDefault();
  const files = e.dataTransfer?.files;
  if (files) for (const file of files) { if (file.name.endsWith(".zip")) handleFile(file); }
};

const onFileSelect = (e: Event) => {
  const target = e.target as HTMLInputElement;
  if (target.files) for (const file of target.files) handleFile(file);
};
</script>

<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-xl font-bold tracking-tight" style="font-family: 'Syne', sans-serif;">{{ t("skills") }}</h2>
        <p class="text-xs mt-1" style="color: var(--muted);">{{ store.skills.length }} {{ t("total") }} · {{ store.userSkillsCount }} {{ t("user") }} · {{ store.systemSkillsCount }} {{ t("system") }}</p>
      </div>
      <button @click="fileInput?.click()" class="px-3 py-1.5 text-sm rounded-md font-medium" style="background-color: var(--primary); color: #ffffff;">{{ t("importBtn") }}</button>
      <input ref="fileInput" type="file" accept=".zip" multiple class="hidden" @change="onFileSelect" />
    </div>

    <div class="flex gap-2">
      <input v-model="store.searchQuery" :placeholder="t('search')" class="flex-1 px-3 py-1.5 text-sm rounded-md" style="background-color: var(--input-bg); border: 1px solid var(--border); color: var(--text);" />
      <select v-model="store.filterType" class="px-3 py-1.5 text-sm rounded-md" style="background-color: var(--input-bg); border: 1px solid var(--border); color: var(--text);">
        <option value="all">{{ t("all") }}</option>
        <option value="user">{{ t("user") }}</option>
        <option value="system">{{ t("system") }}</option>
      </select>
    </div>

    <div class="rounded-lg overflow-hidden" style="background-color: var(--surface); border: 1px solid var(--border);" @dragover.prevent @drop="onFileDrop">
      <div v-if="store.loading" class="p-8 text-center"><div class="animate-spin rounded-full h-6 w-6 border-b-2 mx-auto" style="border-color: var(--primary);"></div><p class="text-xs mt-2" style="color: var(--muted);">{{ t("loading") }}</p></div>
      <div v-else-if="store.filteredSkills.length === 0" class="p-8 text-center text-sm" style="color: var(--muted);">{{ t("noSkills") }}</div>
      <table v-else class="w-full">
        <thead><tr style="border-bottom: 1px solid var(--border);">
          <th class="px-4 py-2 text-left text-xs uppercase" style="color: var(--muted);">{{ t("name") }}</th>
          <th class="px-4 py-2 text-left text-xs uppercase" style="color: var(--muted);">{{ t("description") }}</th>
          <th class="px-4 py-2 text-left text-xs uppercase" style="color: var(--muted);">{{ t("version") }}</th>
          <th class="px-4 py-2 text-left text-xs uppercase" style="color: var(--muted);">{{ t("location") }}</th>
          <th class="px-4 py-2 text-left text-xs uppercase" style="color: var(--muted);">{{ t("status") }}</th>
          <th class="px-4 py-2 text-left text-xs uppercase" style="color: var(--muted);">{{ t("actions") }}</th>
        </tr></thead>
        <tbody>
          <tr v-for="skill in store.filteredSkills" :key="skill.path" style="border-bottom: 1px solid var(--border);" class="hover:opacity-80">
            <td class="px-4 py-2 text-sm">{{ skill.name }}</td>
            <td class="px-4 py-2 text-sm truncate max-w-xs" style="color: var(--muted);">{{ skill.description }}</td>
            <td class="px-4 py-2 text-xs" style="color: var(--muted);">{{ skill.version }}</td>
            <td class="px-4 py-2"><span class="px-2 py-0.5 text-xs rounded" style="background-color: var(--border); color: var(--muted);">{{ skill.location === 'user' ? t("user") : t("system") }}</span></td>
            <td class="px-4 py-2"><span class="px-2 py-0.5 text-xs rounded" :class="skill.enabled ? 'text-green-400' : 'text-red-400'" style="background-color: var(--border);">{{ skill.enabled ? t("on") : t("off") }}</span></td>
            <td class="px-4 py-2 text-xs space-x-2">
              <button v-if="skill.location === 'user'" @click="store.toggleSkill(skill.path)" style="color: var(--primary);">{{ skill.enabled ? t("off") : t("on") }}</button>
              <button v-if="skill.location === 'user'" @click="store.deleteSkill(skill.path)" class="text-red-400">{{ t("del") }}</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
