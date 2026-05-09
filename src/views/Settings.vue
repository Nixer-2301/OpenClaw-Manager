<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useSettingsStore } from "@/stores";
import { useI18n } from "@/composables/useI18n";
import { call } from "@/bridge";

const store = useSettingsStore();
const { t, locale, setLocale } = useI18n();
const message = ref("");

onMounted(() => {
  store.fetchSettings();
});

const browseDir = async (key: string, currentPath: string) => {
  try {
    const path = await call("dialog.selectDir", { title: key, dir: currentPath }) as string;
    if (path) {
      if (key === "openclaw") store.settings.paths.openclaw_dir = path;
      else if (key === "skills") store.settings.paths.user_skills_dir = path;
      else if (key === "backup") store.settings.paths.backup_dir = path;
    }
  } catch {}
};

const handleSave = async () => {
  try {
    await store.saveSettings();
    message.value = "OK";
    setTimeout(() => message.value = "", 1500);
  } catch (e) {
    message.value = "Err";
    setTimeout(() => message.value = "", 1500);
  }
};

const handleReset = async () => {
  await store.resetSettings();
  message.value = "OK";
  setTimeout(() => message.value = "", 1500);
};

const onThemeChange = (e: Event) => {
  const theme = (e.target as HTMLSelectElement).value;
  store.settings.interface.theme = theme;
  if (theme === "light") {
    document.documentElement.classList.add("light");
  } else {
    document.documentElement.classList.remove("light");
  }
};

const onLangChange = (e: Event) => {
  const lang = (e.target as HTMLSelectElement).value;
  setLocale(lang);
};
</script>

<template>
  <div class="space-y-4">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-bold tracking-tight" style="font-family: 'Syne', sans-serif;">{{ t("settings") }}</h2>
      <div class="flex items-center gap-2">
        <span v-if="message" class="text-xs" style="color: var(--primary);">{{ message }}</span>
        <button @click="handleReset" class="px-3 py-1.5 text-xs rounded-md" style="background-color: var(--border); color: var(--muted);">{{ t("reset") }}</button>
        <button @click="handleSave" class="px-3 py-1.5 text-xs rounded-md font-medium" style="background-color: var(--primary); color: #ffffff;">{{ t("save") }}</button>
      </div>
    </div>

    <!-- Appearance -->
    <div class="rounded-lg p-4" style="background-color: var(--surface); border: 1px solid var(--border);">
      <div class="text-xs uppercase mb-3 font-semibold" style="color: var(--muted);">{{ t("appearance") }}</div>
      <div class="space-y-3">
        <div class="flex items-center justify-between">
          <span class="text-sm">{{ t("theme") }}</span>
          <select
            :value="store.settings.interface.theme"
            @change="onThemeChange"
            class="px-2 py-1 text-sm rounded-md"
            style="background-color: var(--input-bg); border: 1px solid var(--border); color: var(--text);"
          >
            <option value="dark">{{ t("dark") }}</option>
            <option value="light">{{ t("light") }}</option>
          </select>
        </div>
        <div class="flex items-center justify-between">
          <span class="text-sm">{{ t("language") }}</span>
          <select
            :value="locale"
            @change="onLangChange"
            class="px-2 py-1 text-sm rounded-md"
            style="background-color: var(--input-bg); border: 1px solid var(--border); color: var(--text);"
          >
            <option value="zh">中文</option>
            <option value="en">English</option>
          </select>
        </div>
      </div>
    </div>

    <!-- General -->
    <div class="rounded-lg p-4" style="background-color: var(--surface); border: 1px solid var(--border);">
      <div class="text-xs uppercase mb-3 font-semibold" style="color: var(--muted);">{{ t("general") }}</div>
      <div class="space-y-3">
        <!-- Auto Refresh -->
        <div class="flex items-center justify-between">
          <div>
            <div class="text-sm">{{ t("autoRefresh") }}</div>
            <div class="text-xs mt-0.5" style="color: var(--muted);">{{ t("autoRefreshDesc") }}</div>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input v-model="store.settings.general.auto_refresh" type="checkbox" class="sr-only peer" />
            <div class="toggle-switch" style="--toggle-bg: var(--border);"></div>
          </label>
        </div>
        <!-- Confirm Delete -->
        <div class="flex items-center justify-between">
          <div>
            <div class="text-sm">{{ t("confirmDelete") }}</div>
            <div class="text-xs mt-0.5" style="color: var(--muted);">{{ t("confirmDeleteDesc") }}</div>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input v-model="store.settings.general.confirm_delete" type="checkbox" class="sr-only peer" />
            <div class="toggle-switch" style="--toggle-bg: var(--border);"></div>
          </label>
        </div>
        <!-- Confirm Batch -->
        <div class="flex items-center justify-between">
          <div>
            <div class="text-sm">{{ t("confirmBatch") }}</div>
            <div class="text-xs mt-0.5" style="color: var(--muted);">{{ t("confirmBatchDesc") }}</div>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input v-model="store.settings.general.confirm_batch" type="checkbox" class="sr-only peer" />
            <div class="toggle-switch" style="--toggle-bg: var(--border);"></div>
          </label>
        </div>
      </div>
    </div>

    <!-- Paths -->
    <div class="rounded-lg p-4" style="background-color: var(--surface); border: 1px solid var(--border);">
      <div class="text-xs uppercase mb-3 font-semibold" style="color: var(--muted);">{{ t("paths") }}</div>
      <div class="space-y-3">
        <div class="flex items-center justify-between gap-3">
          <span class="text-sm flex-shrink-0">{{ t("openclawDir") }}</span>
          <div class="flex items-center gap-1 flex-1">
            <input v-model="store.settings.paths.openclaw_dir" type="text" class="flex-1 px-2 py-1 text-xs font-mono rounded-md" style="background-color: var(--input-bg); border: 1px solid var(--border); color: var(--text);" />
            <button @click="browseDir('openclaw', store.settings.paths.openclaw_dir)" class="px-2 py-1 text-xs rounded-md" style="background-color: var(--border); color: var(--text);">{{ t("browse") }}</button>
          </div>
        </div>
        <div class="flex items-center justify-between gap-3">
          <span class="text-sm flex-shrink-0">{{ t("skillsDir") }}</span>
          <div class="flex items-center gap-1 flex-1">
            <input v-model="store.settings.paths.user_skills_dir" type="text" class="flex-1 px-2 py-1 text-xs font-mono rounded-md" style="background-color: var(--input-bg); border: 1px solid var(--border); color: var(--text);" />
            <button @click="browseDir('skills', store.settings.paths.user_skills_dir)" class="px-2 py-1 text-xs rounded-md" style="background-color: var(--border); color: var(--text);">{{ t("browse") }}</button>
          </div>
        </div>
        <div class="flex items-center justify-between gap-3">
          <span class="text-sm flex-shrink-0">{{ t("backupDir") }}</span>
          <div class="flex items-center gap-1 flex-1">
            <input v-model="store.settings.paths.backup_dir" type="text" class="flex-1 px-2 py-1 text-xs font-mono rounded-md" style="background-color: var(--input-bg); border: 1px solid var(--border); color: var(--text);" />
            <button @click="browseDir('backup', store.settings.paths.backup_dir)" class="px-2 py-1 text-xs rounded-md" style="background-color: var(--border); color: var(--text);">{{ t("browse") }}</button>
          </div>
        </div>
        <div class="flex items-center justify-between">
          <span class="text-sm">{{ t("maxBackups") }}</span>
          <input
            v-model.number="store.settings.paths.max_backups"
            type="number" min="1" max="100"
            class="w-20 px-2 py-1 text-sm rounded-md text-right"
            style="background-color: var(--input-bg); border: 1px solid var(--border); color: var(--text);"
          />
        </div>
      </div>
    </div>

    <!-- File Watcher -->
    <div class="rounded-lg p-4" style="background-color: var(--surface); border: 1px solid var(--border);">
      <div class="text-xs uppercase mb-3 font-semibold" style="color: var(--muted);">{{ t("fileWatcher") }}</div>
      <div class="space-y-3">
        <div class="flex items-center justify-between">
          <span class="text-sm">{{ t("watcherEnabled") }}</span>
          <label class="relative inline-flex items-center cursor-pointer">
            <input v-model="store.settings.file_watcher.enabled" type="checkbox" class="sr-only peer" />
            <div class="toggle-switch" style="--toggle-bg: var(--border);"></div>
          </label>
        </div>
        <div>
          <div class="flex items-center justify-between mb-1">
            <span class="text-sm">{{ t("watcherInterval") }}</span>
            <span class="text-xs font-mono" style="color: var(--primary);">{{ store.settings.file_watcher.refresh_interval }}{{ t("watcherIntervalSuffix") }}</span>
          </div>
          <input
            v-model.number="store.settings.file_watcher.refresh_interval"
            type="range" min="1" max="60" :disabled="!store.settings.file_watcher.enabled"
            class="w-full h-1.5 rounded-full appearance-none cursor-pointer"
            style="accent-color: var(--primary);"
          />
          <div class="flex justify-between text-[10px] mt-0.5" style="color: var(--muted);">
            <span>1s</span><span>60s</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.toggle-switch {
  width: 36px;
  height: 20px;
  background-color: var(--toggle-bg);
  border-radius: 999px;
  position: relative;
  transition: background-color 0.2s;
}

.toggle-switch::after {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 16px;
  height: 16px;
  background: white;
  border-radius: 50%;
  transition: transform 0.2s;
}

:deep(.peer:checked) + .toggle-switch {
  background-color: var(--primary);
}

:deep(.peer:checked) + .toggle-switch::after {
  transform: translateX(16px);
}
</style>
