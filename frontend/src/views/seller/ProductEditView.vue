<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { AxiosError } from "axios";

import UiButton from "../../components/ui/UiButton.vue";
import UiInput from "../../components/ui/UiInput.vue";
import UiSkeleton from "../../components/ui/UiSkeleton.vue";
import { useUiStore } from "../../app/stores/ui";
import { api } from "../../shared/api/client";
import { endpoints } from "../../shared/api/endpoints";
import type { Product } from "../../shared/types/product";
import { buildSellerProductPayload } from "../../features/seller/product-form";
import { uploadSellerImages } from "../../features/seller/upload";

const route = useRoute();
const router = useRouter();
const ui = useUiStore();

const productId = Number(route.params.id);

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
const productStatus = ref<string>("DRAFT");
const isLoading = ref(true);
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
  return "Не удалось обновить товар";
}

async function loadProduct() {
  if (!Number.isFinite(productId)) {
    ui.pushToast("error", "Некорректный id товара");
    router.replace("/seller/products");
    return;
  }

  isLoading.value = true;
  try {
    const response = await api.get<Product>(`${endpoints.seller.products}/${productId}`);
    const product = response.data;

    form.title = product.title;
    form.description = product.description;
    form.price = String(product.price);
    form.stock = product.stock === null ? "" : String(product.stock);
    form.tags = product.tags.join(", ");
    form.materials = product.materials.join(", ");
    form.categoryId = product.category_id ? String(product.category_id) : "";

    uploadedImageUrls.value = product.images.map((image) => image.image_url);
    productStatus.value = product.status;
  } catch {
    ui.pushToast("error", "Не удалось загрузить товар");
    router.replace("/seller/products");
  } finally {
    isLoading.value = false;
  }
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

async function save(submitForModeration = false) {
  isSubmitting.value = true;
  try {
    await uploadSelectedFiles();

    const payload = buildSellerProductPayload(form, uploadedImageUrls.value);
    const response = await api.put<Product>(`${endpoints.seller.products}/${productId}`, payload);
    productStatus.value = response.data.status;

    if (submitForModeration) {
      await api.post(`${endpoints.seller.products}/${productId}/submit`);
      productStatus.value = "PENDING";
      ui.pushToast("success", "Товар обновлён и отправлен на модерацию");
    } else {
      ui.pushToast("success", "Товар обновлён");
    }

    router.push("/seller/products");
  } catch (error) {
    ui.pushToast("error", extractApiError(error));
  } finally {
    isSubmitting.value = false;
  }
}

onMounted(loadProduct);
</script>

<template>
  <section class="space-y-4">
    <UiSkeleton v-if="isLoading" :rows="5" />

    <template v-else>
      <div class="flex flex-wrap items-center justify-between gap-3">
        <h1 class="font-display text-2xl font-bold text-primary-dark">Редактирование товара</h1>
        <span class="rounded-full bg-brand-100 px-3 py-1 text-sm font-semibold text-primary-dark">
          Статус: {{ productStatus }}
        </span>
      </div>

      <form class="space-y-3" @submit.prevent="save(false)">
        <UiInput v-model="form.title" label="Название" />

        <label class="flex flex-col gap-1 text-[1.03rem] font-semibold text-primary-dark">
          <span>Описание</span>
          <textarea
            v-model="form.description"
            rows="4"
            class="brand-textarea px-3 py-2.5 text-[1.03rem] outline-none"
          />
        </label>

        <div class="grid gap-3 md:grid-cols-2">
          <UiInput v-model="form.price" type="number" label="Цена" />
          <UiInput v-model="form.stock" type="number" label="Остаток (опционально)" />
        </div>

        <div class="grid gap-3 md:grid-cols-2">
          <UiInput v-model="form.tags" label="Теги (через запятую)" />
          <UiInput v-model="form.materials" label="Материалы (через запятую)" />
        </div>

        <UiInput v-model="form.categoryId" type="number" label="ID категории (опционально)" />

        <label class="flex flex-col gap-1 text-[1.03rem] font-semibold text-primary-dark">
          <span>Добавить фото с компьютера</span>
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
          <p class="text-sm font-semibold text-primary-dark">Фото товара</p>
          <div class="space-y-2">
            <div v-for="url in uploadedImageUrls" :key="url" class="flex items-center justify-between gap-2 rounded bg-white px-3 py-2 text-sm">
              <span class="truncate">{{ url }}</span>
              <button type="button" class="text-red-600" @click="removeImage(url)">Удалить</button>
            </div>
          </div>
        </div>

        <div class="flex flex-wrap gap-2">
          <UiButton type="button" variant="secondary" :disabled="isSubmitting || isUploading" @click="save(false)">Сохранить</UiButton>
          <UiButton
            v-if="productStatus === 'DRAFT' || productStatus === 'REJECTED'"
            type="button"
            :disabled="isSubmitting || isUploading"
            @click="save(true)"
          >
            Сохранить и отправить на модерацию
          </UiButton>
        </div>
      </form>
    </template>
  </section>
</template>
