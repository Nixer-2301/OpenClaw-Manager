<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";

const emit = defineEmits<{
  complete: [];
}>();

interface LoadItem {
  name: string;
  loaded: boolean;
}

const loadItems = ref<LoadItem[]>([
  { name: "API", loaded: false },
  { name: "Skills", loaded: false },
  { name: "Config", loaded: false },
  { name: "Models", loaded: false },
  { name: "Process", loaded: false },
  { name: "Sessions", loaded: false },
  { name: "Logs", loaded: false },
  { name: "Stats", loaded: false },
]);

const isExiting = ref(false);
const currentIndex = ref(0);
let interval: number | null = null;

onMounted(() => {
  setTimeout(() => {
    interval = window.setInterval(() => {
      if (currentIndex.value < loadItems.value.length) {
        loadItems.value[currentIndex.value].loaded = true;
        currentIndex.value++;
      } else {
        if (interval) clearInterval(interval);
        setTimeout(() => {
          isExiting.value = true;
          setTimeout(() => emit("complete"), 300);
        }, 200);
      }
    }, 60);
  }, 700);
});

onUnmounted(() => {
  if (interval) clearInterval(interval);
});
</script>

<template>
  <div
    class="fixed inset-0 z-50 flex items-center justify-center transition-opacity duration-300"
    :style="{ backgroundColor: 'var(--bg)', opacity: isExiting ? 0 : 1 }"
  >
    <!-- Center: Title -->
    <div class="flex flex-col items-center select-none">
      <h1 class="text-5xl font-bold tracking-tight" style="color: var(--text);">
        OpenClaw Manager
      </h1>
      <div class="mt-3 h-px w-40" style="background: linear-gradient(90deg, transparent, var(--primary), transparent);" />
    </div>

    <!-- Bottom left: Loading items -->
    <div class="absolute bottom-10 left-10 space-y-1.5">
      <div
        v-for="item in loadItems"
        :key="item.name"
        class="flex items-center gap-2 text-xs font-mono transition-all duration-200"
        :class="item.loaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2'"
      >
        <span class="w-16" style="color: var(--muted);">{{ item.name }}</span>
        <span
          class="text-[10px]"
          :style="{ color: item.loaded ? '#4ade80' : 'var(--muted)' }"
        >
          {{ item.loaded ? "loaded" : "..." }}
        </span>
      </div>
    </div>

    <!-- Bottom right: Version -->
    <div class="absolute bottom-10 right-10">
      <span class="text-xs" style="color: var(--muted);">v1.2</span>
    </div>
  </div>
</template>
