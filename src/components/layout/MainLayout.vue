<script setup lang="ts">
import { computed, onMounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useProcessStore, useSettingsStore } from "@/stores";
import { useI18n } from "@/composables/useI18n";

const router = useRouter();
const route = useRoute();
const processStore = useProcessStore();
const settingsStore = useSettingsStore();
const { t } = useI18n();

interface NavItem {
  name: string;
  path: string;
  i18nKey: string;
}

const navItems: NavItem[] = [
  { name: t("dashboard"), path: "/", i18nKey: "dashboard" },
  { name: t("skills"), path: "/skills", i18nKey: "skills" },
  { name: t("models"), path: "/models", i18nKey: "models" },
  { name: t("plugins"), path: "/plugins", i18nKey: "plugins" },
  { name: t("process"), path: "/process", i18nKey: "process" },
  { name: t("sessions"), path: "/sessions", i18nKey: "sessions" },
  { name: t("logs"), path: "/logs", i18nKey: "logs" },
  { name: t("stats"), path: "/stats", i18nKey: "stats" },
  { name: t("config"), path: "/config", i18nKey: "config" },
  { name: t("settings"), path: "/settings", i18nKey: "settings" },
];

const currentTab = computed(() => route.path);
const pageTitle = computed(() => {
  const item = navItems.find(i => i.path === route.path);
  return item ? item.i18nKey : "";
});

const isLight = computed(() => settingsStore.settings.interface.theme === "light");

const navigate = (path: string) => {
  router.push(path);
};

const toggleTheme = () => {
  const newTheme = isLight.value ? "dark" : "light";
  settingsStore.settings.interface.theme = newTheme;
  settingsStore.saveSettings();
};

function applyTheme(theme: string) {
  if (theme === "light") {
    document.documentElement.classList.add("light");
  } else {
    document.documentElement.classList.remove("light");
  }
}

onMounted(async () => {
  await processStore.fetchStatus();
  await settingsStore.fetchSettings();
  applyTheme(settingsStore.settings.interface.theme);
});

watch(() => settingsStore.settings.interface.theme, applyTheme);
</script>

<template>
  <div class="flex flex-col h-screen" style="background-color: var(--bg); color: var(--text);">
    <!-- Title bar -->
    <div
      class="flex items-center shrink-0 py-3 px-5"
      style="background-color: var(--surface); border-bottom: 1px solid var(--border);"
    >
      <!-- Title -->
      <div class="flex items-center">
        <span class="text-2xl font-bold whitespace-nowrap">{{ t("title") }}</span>
      </div>

      <!-- Tabs centered -->
      <div class="flex-1 flex justify-center">
        <div class="flex items-center gap-0.5">
          <button
            v-for="item in navItems"
            :key="item.path"
            @click="navigate(item.path)"
            class="px-3 py-1 text-sm rounded-md transition-colors whitespace-nowrap"
            :style="{
              backgroundColor: currentTab === item.path ? 'var(--primary)' : 'transparent',
              color: currentTab === item.path ? '#ffffff' : 'var(--muted)',
            }"
          >
            {{ t(item.i18nKey) }}
          </button>
        </div>
      </div>

      <!-- Right side -->
      <div class="flex items-center gap-3">
        <button
          @click="toggleTheme"
          class="px-3 py-1 text-xs rounded-md transition-colors"
          style="background-color: var(--border); color: var(--text);"
        >
          {{ isLight ? t("light") : t("dark") }}
        </button>
        <span class="text-xs" style="color: var(--muted);">v1.2</span>
      </div>
    </div>

    <!-- Content -->
    <main class="flex-1 overflow-auto p-4">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Status bar -->
    <div
      class="flex items-center h-6 px-3 shrink-0 text-xs"
      style="background-color: var(--surface); border-top: 1px solid var(--border); color: var(--muted);"
    >
      <span>{{ t(pageTitle) }}</span>
      <div class="flex-1" />
      <span class="mr-4">{{ t("port") }}: {{ processStore.config.port }}</span>
      <span :class="processStore.status.running ? 'text-green-500' : 'text-red-500'">
        {{ processStore.status.running ? t("running") : t("stopped") }}
      </span>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.1s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
