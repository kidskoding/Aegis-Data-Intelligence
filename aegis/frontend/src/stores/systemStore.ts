import { create } from "zustand";
import type { Stats } from "../api/types";
import { getStats, getStatus } from "../api/endpoints";

interface SystemState {
  stats: Stats | null;
  llmEnabled: boolean | null;
  loading: boolean;
  fetchStats: () => Promise<void>;
  fetchStatus: () => Promise<void>;
}

export const useSystemStore = create<SystemState>((set) => ({
  stats: null,
  llmEnabled: null,
  loading: false,

  fetchStats: async () => {
    set({ loading: true });
    try {
      const data = await getStats();
      set({ stats: data });
    } finally {
      set({ loading: false });
    }
  },

  fetchStatus: async () => {
    try {
      const data = await getStatus();
      set({ llmEnabled: data.llm_enabled });
    } catch {
      // Non-fatal — banner simply won't show if status is unreachable
    }
  },
}));
