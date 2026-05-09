import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    name: "dashboard",
    component: () => import("@/views/Dashboard.vue"),
    meta: { title: "仪表盘", icon: "home" },
  },
  {
    path: "/skills",
    name: "skills",
    component: () => import("@/views/Skills.vue"),
    meta: { title: "Skills管理", icon: "puzzle" },
  },
  {
    path: "/models",
    name: "models",
    component: () => import("@/views/Models.vue"),
    meta: { title: "模型管理", icon: "cpu" },
  },
  {
    path: "/plugins",
    name: "plugins",
    component: () => import("@/views/Plugins.vue"),
    meta: { title: "插件管理", icon: "box" },
  },
  {
    path: "/process",
    name: "process",
    component: () => import("@/views/Process.vue"),
    meta: { title: "进程管理", icon: "activity" },
  },
  {
    path: "/sessions",
    name: "sessions",
    component: () => import("@/views/Sessions.vue"),
    meta: { title: "会话监控", icon: "message-circle" },
  },
  {
    path: "/logs",
    name: "logs",
    component: () => import("@/views/Logs.vue"),
    meta: { title: "日志查看", icon: "file-text" },
  },
  {
    path: "/stats",
    name: "stats",
    component: () => import("@/views/Stats.vue"),
    meta: { title: "数据统计", icon: "bar-chart" },
  },
  {
    path: "/config",
    name: "config",
    component: () => import("@/views/Config.vue"),
    meta: { title: "配置文件", icon: "settings" },
  },
  {
    path: "/settings",
    name: "settings",
    component: () => import("@/views/Settings.vue"),
    meta: { title: "设置", icon: "sliders" },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
