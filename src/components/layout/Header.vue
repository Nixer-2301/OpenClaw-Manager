<script setup lang="ts">
import { ref, computed } from "vue";
import { useRoute } from "vue-router";

const emit = defineEmits<{
  "toggle-sidebar": [];
}>();

const route = useRoute();
const searchQuery = ref("");
const isDarkMode = ref(document.documentElement.classList.contains("dark"));

const pageTitle = computed(() => {
  return (route.meta?.title as string) || "OpenClaw Manager";
});

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value;
  document.documentElement.classList.toggle("dark", isDarkMode.value);
  localStorage.setItem("theme", isDarkMode.value ? "dark" : "light");
};
</script>

<template>
  <header
    class="h-16 bg-white dark:bg-dark-card border-b border-gray-200 dark:border-dark-border flex items-center justify-between px-6"
  >
    <!-- Left: Toggle & Title -->
    <div class="flex items-center space-x-4">
      <button
        @click="emit('toggle-sidebar')"
        class="p-2 rounded-lg text-gray-500 dark:text-dark-muted hover:bg-gray-100 dark:hover:bg-dark-hover hover:text-gray-700 dark:hover:text-dark-text transition-colors lg:hidden"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="w-5 h-5"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
          />
        </svg>
      </button>
      <h1 class="text-xl font-semibold text-gray-800 dark:text-dark-text">
        {{ pageTitle }}
      </h1>
    </div>

    <!-- Center: Search -->
    <div class="flex-1 max-w-md mx-8">
      <div class="relative">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 dark:text-dark-muted"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"
          />
        </svg>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索... (Ctrl+K)"
          class="w-full pl-10 pr-4 py-2 bg-gray-100 dark:bg-dark-bg border-0 rounded-lg text-sm text-gray-700 dark:text-dark-text placeholder-gray-400 dark:placeholder-dark-muted focus:outline-none focus:ring-2 focus:ring-primary-500"
        />
      </div>
    </div>

    <!-- Right: Actions -->
    <div class="flex items-center space-x-3">
      <!-- Theme toggle -->
      <button
        @click="toggleDarkMode"
        class="p-2 rounded-lg text-gray-500 dark:text-dark-muted hover:bg-gray-100 dark:hover:bg-dark-hover hover:text-gray-700 dark:hover:text-dark-text transition-colors"
        :title="isDarkMode ? '切换到浅色模式' : '切换到深色模式'"
      >
        <svg
          v-if="isDarkMode"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="w-5 h-5"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z"
          />
        </svg>
        <svg
          v-else
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="w-5 h-5"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z"
          />
        </svg>
      </button>

      <!-- Notifications -->
      <button
        class="p-2 rounded-lg text-gray-500 dark:text-dark-muted hover:bg-gray-100 dark:hover:bg-dark-hover hover:text-gray-700 dark:hover:text-dark-text transition-colors relative"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="w-5 h-5"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0"
          />
        </svg>
        <span class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
      </button>

      <!-- Command palette hint -->
      <div
        class="hidden md:flex items-center px-3 py-1.5 bg-gray-100 dark:bg-dark-bg rounded-lg text-xs text-gray-400 dark:text-dark-muted"
      >
        <span>Ctrl+Shift+P</span>
      </div>
    </div>
  </header>
</template>
