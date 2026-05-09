<script setup lang="ts">
import { ref } from "vue";
import SplashScreen from "@/components/SplashScreen.vue";
import MainLayout from "@/components/layout/MainLayout.vue";

const showSplash = ref(true);

const onSplashComplete = () => {
  showSplash.value = false;
};
</script>

<template>
  <SplashScreen v-if="showSplash" @complete="onSplashComplete" />
  <MainLayout v-else />
</template>

<style>
/* Global styles are in main.css */
</style>
