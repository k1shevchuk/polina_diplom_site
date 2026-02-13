import { onBeforeUnmount, onMounted } from "vue";

export function usePolling(callback: () => void | Promise<void>, intervalMs: number) {
  let intervalId: number | null = null;

  const run = async () => {
    if (document.hidden) return;
    await callback();
  };

  onMounted(() => {
    intervalId = window.setInterval(run, intervalMs);
  });

  onBeforeUnmount(() => {
    if (intervalId !== null) {
      window.clearInterval(intervalId);
    }
  });
}
