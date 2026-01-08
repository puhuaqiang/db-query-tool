<template>
  <el-select
    :model-value="modelValue"
    placeholder="选择模型"
    :disabled="disabled || loading"
    :loading="loading"
    size="small"
    style="width: 180px"
    @update:model-value="handleChange"
  >
    <el-option
      v-for="model in models"
      :key="model.id"
      :label="model.name"
      :value="model.id"
    >
      <div class="flex items-center justify-between">
        <span>{{ model.name }}</span>
        <span class="text-xs text-gray-400 ml-2">{{ model.provider }}</span>
      </div>
    </el-option>
  </el-select>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElSelect, ElOption } from 'element-plus'
import type { LlmModel } from '@/services/types'
import { naturalQueryApi } from '@/services/api'

const props = defineProps<{
  modelValue: string
  disabled?: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const models = ref<LlmModel[]>([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    models.value = await naturalQueryApi.getLlmModels()
    // Set default model if current value is empty and models are available
    if (!props.modelValue && models.value.length > 0) {
      emit('update:modelValue', models.value[0].id)
    }
  } catch (error) {
    console.error('Failed to load LLM models:', error)
  } finally {
    loading.value = false
  }
})

function handleChange(value: string): void {
  emit('update:modelValue', value)
}
</script>
