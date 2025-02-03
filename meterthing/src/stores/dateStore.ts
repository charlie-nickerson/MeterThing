// src/stores/dateStore.ts
import { writable } from "svelte/store";

export const dateRange = writable({
    start: new Date().toISOString().split("T")[0], // Today as default
    end: new Date().toISOString().split("T")[0],
});