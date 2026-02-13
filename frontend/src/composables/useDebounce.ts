import { ref } from "vue";

export function useDebounce<T>(delay = 400) {
  const value = ref<T | null>(null);
  let timeout: number | undefined;

  function set(next: T) {
    if (timeout) {
      window.clearTimeout(timeout);
    }

    timeout = window.setTimeout(() => {
      value.value = next;
    }, delay);
  }

  return {
    value,
    set,
  };
}
