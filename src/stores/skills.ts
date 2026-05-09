import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { call } from "@/bridge";

export interface Skill {
  name: string;
  description: string;
  version: string;
  location: string;
  path: string;
  base_dir: string;
  enabled: boolean;
  user_invocable: boolean;
  argument_hint: string;
  allowed_tools: string;
  license: string;
  author: string;
}

export const useSkillsStore = defineStore("skills", () => {
  const skills = ref<Skill[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const searchQuery = ref("");
  const filterType = ref<"all" | "user" | "system">("all");

  const filteredSkills = computed(() => {
    let result = skills.value;
    if (filterType.value === "user") result = result.filter((s) => s.location === "user");
    else if (filterType.value === "system") result = result.filter((s) => s.location === "system");
    if (searchQuery.value) {
      const q = searchQuery.value.toLowerCase();
      result = result.filter((s) => s.name.toLowerCase().includes(q) || s.description.toLowerCase().includes(q));
    }
    return result;
  });

  const userSkillsCount = computed(() => skills.value.filter((s) => s.location === "user").length);
  const systemSkillsCount = computed(() => skills.value.filter((s) => s.location === "system").length);

  async function fetchSkills() {
    loading.value = true; error.value = null;
    try { skills.value = (await call("skills.getAll")) as Skill[]; }
    catch { skills.value = []; }
    finally { loading.value = false; }
  }

  async function toggleSkill(path: string) {
    try { skills.value = (await call("skills.toggle", { path })) as Skill[]; }
    catch (e) { error.value = (e as Error).message; throw e; }
  }

  async function deleteSkill(path: string) {
    try { skills.value = (await call("skills.delete", { path })) as Skill[]; }
    catch (e) { error.value = (e as Error).message; throw e; }
  }

  async function importSkill(zipPath: string) {
    try { skills.value = (await call("skills.import", { zip_path: zipPath })) as Skill[]; }
    catch (e) { error.value = (e as Error).message; throw e; }
  }

  return { skills, loading, error, searchQuery, filterType, filteredSkills, userSkillsCount, systemSkillsCount, fetchSkills, toggleSkill, deleteSkill, importSkill };
});
