<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { AxiosError } from "axios";

import UiButton from "../../components/ui/UiButton.vue";
import UiInput from "../../components/ui/UiInput.vue";
import UiModal from "../../components/ui/UiModal.vue";
import UiSkeleton from "../../components/ui/UiSkeleton.vue";
import { useUiStore } from "../../app/stores/ui";
import { api } from "../../shared/api/client";
import { endpoints } from "../../shared/api/endpoints";
import type { Product } from "../../shared/types/product";
import { splitCsv } from "../../features/seller/product-form";

const ui = useUiStore();
const products = ref<Product[]>([]);
const search = ref("");
const isLoading = ref(false);
const isSaving = ref(false);

const isModalOpen = ref(false);
const editingProductId = ref<number | null>(null);
const editForm = reactive({
  title: "",
  description: "",
  price: "",
  stock: "",
  tags: "",
  materials: "",
});

const filteredProducts = computed(() => {
  const q = search.value.trim().toLowerCase();
  if (!q) return products.value;
  return products.value.filter((item) => item.title.toLowerCase().includes(q));
});

function extractApiError(error: unknown): string {
  if (error instanceof AxiosError) {
    const detail = error.response?.data?.detail;
    if (Array.isArray(detail) && detail.length > 0) {
      return detail.map((item: { msg?: string }) => item.msg || "Validation error").join("; ");
    }
    if (typeof detail === "string") {
      return detail;
    }
  }
  return "Не удалось выполнить действие";
}

async function load() {
  isLoading.value = true;
  try {
    const response = await api.get<{ items: Product[] }>(endpoints.admin.products);
    products.value = response.data.items;
  } catch (error) {
    products.value = [];
    ui.pushToast("error", extractApiError(error));
  } finally {
    isLoading.value = false;
  }
}

function openEdit(product: Product) {
  editingProductId.value = product.id;
  editForm.title = product.title;
  editForm.description = product.description;
  editForm.price = String(product.price);
  editForm.stock = product.stock === null ? "" : String(product.stock);
  editForm.tags = product.tags.join(", ");
  editForm.materials = product.materials.join(", ");
  isModalOpen.value = true;
}

function closeEdit() {
  isModalOpen.value = false;
  editingProductId.value = null;
}

async function saveEdit() {
  if (!editingProductId.value) return;

  isSaving.value = true;
  try {
    await api.put(`${endpoints.admin.products}/${editingProductId.value}`, {
      title: editForm.title.trim(),
      description: editForm.description.trim(),
      price: Number(editForm.price),
      stock: editForm.stock.trim() === "" ? null : Number(editForm.stock),
      tags: splitCsv(editForm.tags),
      materials: splitCsv(editForm.materials),
    });

    ui.pushToast("success", "Товар обновлён администратором");
    closeEdit();
    await load();
  } catch (error) {
    ui.pushToast("error", extractApiError(error));
  } finally {
    isSaving.value = false;
  }
}

function hideProduct(product: Product) {
  ui.askConfirm({
    title: "Скрыть товар",
    message: `Товар "${product.title}" будет переведён в архив.`,
    onConfirm: async () => {
      try {
        await api.delete(`${endpoints.admin.products}/${product.id}`);
        ui.pushToast("success", "Товар скрыт");
        await load();
      } catch (error) {
        ui.pushToast("error", extractApiError(error));
      }
    },
  });
}

function deleteProduct(product: Product) {
  ui.askConfirm({
    title: "Удалить товар",
    message: `Товар "${product.title}" будет удалён безвозвратно.`,
    onConfirm: async () => {
      try {
        await api.delete(`${endpoints.admin.products}/${product.id}?hard_delete=true`);
        ui.pushToast("success", "Товар удалён");
        await load();
      } catch (error) {
        ui.pushToast("error", extractApiError(error));
      }
    },
  });
}

onMounted(load);
</script>

<template>
  <section class="space-y-4">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <h1 class="font-display text-2xl font-bold text-primary-dark">Товары</h1>
      <div class="w-full max-w-sm">
        <UiInput v-model="search" label="Поиск по названию" placeholder="Название товара" />
      </div>
    </div>

    <UiSkeleton v-if="isLoading" :rows="4" />

    <div v-else class="space-y-3">
      <article v-for="product in filteredProducts" :key="product.id" class="brand-card border border-brand-100 p-4">
        <div class="flex flex-wrap items-start justify-between gap-3">
          <div class="space-y-1">
            <h2 class="text-xl font-semibold text-primary-dark">{{ product.title }}</h2>
            <p class="text-sm text-muted">ID: {{ product.id }} · Seller: {{ product.seller_id }} · Status: {{ product.status }}</p>
            <p class="line-clamp-2 text-sm text-muted">{{ product.description }}</p>
          </div>

          <div class="flex flex-wrap gap-2">
            <UiButton variant="secondary" @click="openEdit(product)">Редактировать</UiButton>
            <UiButton variant="ghost" @click="hideProduct(product)">Скрыть</UiButton>
            <UiButton variant="danger" @click="deleteProduct(product)">Удалить</UiButton>
          </div>
        </div>
      </article>
    </div>

    <UiModal :open="isModalOpen" title="Редактирование товара" @close="closeEdit">
      <form class="space-y-3" @submit.prevent="saveEdit">
        <UiInput v-model="editForm.title" label="Название" />

        <label class="flex flex-col gap-1 text-[1.03rem] font-semibold text-primary-dark">
          <span>Описание</span>
          <textarea v-model="editForm.description" rows="4" class="brand-textarea px-3 py-2.5 text-[1.03rem] outline-none" />
        </label>

        <div class="grid gap-3 md:grid-cols-2">
          <UiInput v-model="editForm.price" type="number" label="Цена" />
          <UiInput v-model="editForm.stock" type="number" label="Остаток" />
        </div>

        <div class="grid gap-3 md:grid-cols-2">
          <UiInput v-model="editForm.tags" label="Теги" />
          <UiInput v-model="editForm.materials" label="Материалы" />
        </div>

        <div class="flex justify-end gap-2">
          <UiButton variant="ghost" type="button" @click="closeEdit">Отмена</UiButton>
          <UiButton type="submit" :disabled="isSaving">Сохранить</UiButton>
        </div>
      </form>
    </UiModal>
  </section>
</template>
