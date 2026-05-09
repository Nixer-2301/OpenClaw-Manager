<script setup lang="ts">
import { computed } from "vue";
import { useRouter, useRoute } from "vue-router";

defineProps<{
  collapsed: boolean;
}>();

const emit = defineEmits<{
  toggle: [];
}>();

const router = useRouter();
const route = useRoute();

interface NavItem {
  name: string;
  path: string;
  icon: string;
  category?: string;
}

const navItems: NavItem[] = [
  { name: "仪表盘", path: "/", icon: "home", category: "概览" },
  { name: "Skills管理", path: "/skills", icon: "puzzle", category: "资源" },
  { name: "模型管理", path: "/models", icon: "cpu", category: "资源" },
  { name: "插件管理", path: "/plugins", icon: "box", category: "资源" },
  { name: "进程管理", path: "/process", icon: "activity", category: "监控" },
  { name: "会话监控", path: "/sessions", icon: "message-circle", category: "监控" },
  { name: "日志查看", path: "/logs", icon: "file-text", category: "监控" },
  { name: "数据统计", path: "/stats", icon: "bar-chart", category: "监控" },
  { name: "配置文件", path: "/config", icon: "settings", category: "配置" },
  { name: "设置", path: "/settings", icon: "sliders", category: "配置" },
];

const categories = computed(() => {
  const cats: Record<string, NavItem[]> = {};
  navItems.forEach((item) => {
    const cat = item.category || "其他";
    if (!cats[cat]) cats[cat] = [];
    cats[cat].push(item);
  });
  return cats;
});

const isActive = (path: string) => {
  return route.path === path;
};

const navigate = (path: string) => {
  router.push(path);
};
</script>

<template>
  <aside
    :class="[
      'flex flex-col bg-white dark:bg-dark-card border-r border-gray-200 dark:border-dark-border transition-all duration-300',
      collapsed ? 'w-16' : 'w-64',
    ]"
  >
    <!-- Logo -->
    <div class="flex items-center h-16 px-4 border-b border-gray-200 dark:border-dark-border">
      <div class="flex items-center space-x-3">
        <div class="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
          <span class="text-white font-bold text-sm">OC</span>
        </div>
        <span v-if="!collapsed" class="text-lg font-semibold text-gray-800 dark:text-dark-text">
          OpenClaw Manager
        </span>
      </div>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 overflow-y-auto py-4">
      <div v-for="(items, category) in categories" :key="category" class="mb-4">
        <div
          v-if="!collapsed"
          class="px-4 mb-2 text-xs font-semibold text-gray-400 dark:text-dark-muted uppercase tracking-wider"
        >
          {{ category }}
        </div>
        <div v-for="item in items" :key="item.path" class="px-2">
          <button
            @click="navigate(item.path)"
            :class="[
              'flex items-center w-full px-3 py-2.5 rounded-lg transition-all duration-200 group',
              isActive(item.path)
                ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400'
                : 'text-gray-600 dark:text-dark-muted hover:bg-gray-100 dark:hover:bg-dark-hover hover:text-gray-900 dark:hover:text-dark-text',
            ]"
          >
            <div
              :class="[
                'w-5 h-5 flex-shrink-0',
                isActive(item.path)
                  ? 'text-primary-500'
                  : 'text-gray-400 dark:text-dark-muted group-hover:text-gray-600 dark:group-hover:text-dark-text',
              ]"
            >
              <!-- Icon placeholder - will use Heroicons -->
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z"
                />
              </svg>
            </div>
            <span v-if="!collapsed" class="ml-3 text-sm font-medium truncate">
              {{ item.name }}
            </span>
          </button>
        </div>
      </div>
    </nav>

    <!-- Collapse button -->
    <div class="p-4 border-t border-gray-200 dark:border-dark-border">
      <button
        @click="emit('toggle')"
        class="flex items-center justify-center w-full px-3 py-2 text-sm text-gray-500 dark:text-dark-muted hover:text-gray-700 dark:hover:text-dark-text hover:bg-gray-100 dark:hover:bg-dark-hover rounded-lg transition-colors"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          :class="['w-5 h-5 transition-transform', collapsed ? 'rotate-180' : '']"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M18.75 19.5l-7.5-7.5 7.5-7.5m-6 15L5.25 12l7.5-7.5"
          />
        </svg>
        <span v-if="!collapsed" class="ml-2">收起侧边栏</span>
      </button>
    </div>
  </aside>
</template>
