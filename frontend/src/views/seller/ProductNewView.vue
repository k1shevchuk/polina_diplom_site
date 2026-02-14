<script setup lang="ts">
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { AxiosError } from "axios";

import UiButton from "../../components/ui/UiButton.vue";
import UiInput from "../../components/ui/UiInput.vue";
import { useUiStore } from "../../app/stores/ui";
import { api } from "../../shared/api/client";
import { endpoints } from "../../shared/api/endpoints";
import type { Product } from "../../shared/types/product";
import { buildSellerProductPayload } from "../../features/seller/product-form";
import { uploadSellerImages } from "../../features/seller/upload";

const ui = useUiStore();
const router = useRouter();

const form = reactive({
  title: "",
  description: "",
  price: "",
  stock: "",
  tags: "",
  materials: "",
  categoryId: "",
});

const selectedFiles = ref<File[]>([]);
const uploadedImageUrls = ref<string[]>([]);
const isSubmitting = ref(false);
const isUploading = ref(false);

function onFilesSelected(event: Event) {
  const input = event.target as HTMLInputElement;
  selectedFiles.value = Array.from(input.files ?? []);
}

function removeImage(url: string) {
  uploadedImageUrls.value = uploadedImageUrls.value.filter((item) => item !== url);
}

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
  return "Не удалось сохранить товар";
}

async function uploadSelectedFiles() {
  if (selectedFiles.value.length === 0) {
    return;
  }

  isUploading.value = true;
  try {
    const uploaded = await uploadSellerImages(api, endpoints.seller.uploadImage, selectedFiles.value);
    uploadedImageUrls.value.push(...uploaded);
    selectedFiles.value = [];
    ui.pushToast("success", "Изображения загружены");
  } finally {
    isUploading.value = false;
  }
}

async function createProduct(submitForModeration: boolean) {
  isSubmitting.value = true;
  try {
    await uploadSelectedFiles();

    const payload = buildSellerProductPayload(form, uploadedImageUrls.value);
    const response = await api.post<Product>(endpoints.seller.products, payload);

    if (submitForModeration) {
      await api.post(`${endpoints.seller.products}/${response.data.id}/submit`);
      ui.pushToast("success", "Товар создан и отправлен на модерацию");
    } else {
      ui.pushToast("success", "Черновик товара сохранён");
    }

    router.push("/seller/products");
  } catch (error) {
    ui.pushToast("error", extractApiError(error));
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <section class="space-y-4">
    <h1 class="font-display text-2xl font-bold text-primary-dark">Новый товар</h1>

    <form class="space-y-3" @submit.prevent="createProduct(false)">
      <UiInput v-model="form.title" label="Название" placeholder="Например: Нежный шарф #1" />

      <label class="flex flex-col gap-1 text-[1.03rem] font-semibold text-primary-dark">
        <span>Описание</span>
        <textarea
          v-model="form.description"
          rows="4"
          class="brand-textarea px-3 py-2.5 text-[1.03rem] outline-none"
          placeholder="Подробно опишите изделие, материалы и уход"
        />
      </label>

      <div class="grid gap-3 md:grid-cols-2">
        <UiInput v-model="form.price" type="number" label="Цена" />
        <UiInput v-model="form.stock" type="number" label="Остаток (опционально)" />
      </div>

      <div class="grid gap-3 md:grid-cols-2">
        <UiInput v-model="form.tags" label="Теги (через запятую)" placeholder="шарф, зима, подарок" />
        <UiInput v-model="form.materials" label="Материалы (через запятую)" placeholder="шерсть, хлопок" />
      </div>

      <UiInput v-model="form.categoryId" type="number" label="ID категории (опционально)" />

      <label class="flex flex-col gap-1 text-[1.03rem] font-semibold text-primary-dark">
        <span>Фото с компьютера</span>
        <input
          type="file"
          accept="image/*"
          multiple
          class="brand-input px-3 py-2.5 text-[1.03rem] outline-none"
          @change="onFilesSelected"
        />
      </label>

      <div v-if="selectedFiles.length > 0" class="rounded-xl border border-brand-200 bg-brand-50 p-3 text-sm text-primary-dark">
        Выбрано файлов: {{ selectedFiles.length }}
      </div>

      <div v-if="uploadedImageUrls.length > 0" class="space-y-2 rounded-xl border border-brand-200 bg-brand-50 p-3">
        <p class="text-sm font-semibold text-primary-dark">Загруженные фото</p>
        <div class="space-y-2">
          <div v-for="url in uploadedImageUrls" :key="url" class="flex items-center justify-between gap-2 rounded bg-white px-3 py-2 text-sm">
            <span class="truncate">{{ url }}</span>
            <button type="button" class="text-red-600" @click="removeImage(url)">Удалить</button>
          </div>
        </div>
      </div>

      <div class="flex flex-wrap gap-2">
        <UiButton type="button" variant="secondary" :disabled="isSubmitting || isUploading" @click="createProduct(false)">
          Сохранить черновик
        </UiButton>
        <UiButton type="button" :disabled="isSubmitting || isUploading" @click="createProduct(true)">
          Сохранить и отправить на модерацию
        </UiButton>
      </div>
    </form>
  </section>
</template>
