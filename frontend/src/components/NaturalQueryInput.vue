<template>
  <div class="natural-query-input">
    <div class="flex gap-2 mb-3">
      <el-input
        v-model="prompt"
        placeholder="用自然语言描述你的查询需求，如：查询所有用户"
        :disabled="disabled"
        clearable
        @keyup.enter="handleGenerate"
      >
        <template #prepend>
          <LlmModelSelector v-model="selectedModel" :disabled="disabled || loading" />
        </template>
      </el-input>
      <el-button
        type="primary"
        :disabled="disabled || !prompt.trim()"
        :loading="loading"
        @click="handleGenerate"
      >
        生成 SQL
      </el-button>
    </div>

    <!-- Generated SQL preview -->
    <div v-if="generatedSql" class="generated-sql mb-3">
      <div class="flex justify-between items-center mb-2">
        <span class="text-sm text-gray-600">生成的 SQL:</span>
        <div class="flex gap-2">
          <el-button size="small" @click="handleCopy">
            复制
          </el-button>
          <el-button size="small" type="primary" @click="handleApply">
            应用到编辑器
          </el-button>
        </div>
      </div>
      <pre class="bg-gray-100 p-3 rounded text-sm overflow-x-auto"><code>{{ generatedSql }}</code></pre>
      <div v-if="explanation" class="mt-2 text-sm text-gray-500">
        {{ explanation }}
      </div>
    </div>

    <!-- Error message -->
    <div v-if="error" class="error-message text-red-500 text-sm mt-2">
      {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { ElInput, ElButton, ElMessage } from 'element-plus'
import LlmModelSelector from './LlmModelSelector.vue'
import { naturalQueryApi } from '@/services/api'

const props = defineProps<{
  dbName: string
  disabled?: boolean
}>()

const emit = defineEmits<{
  apply: [sql: string]
}>()

const prompt = ref('')
const selectedModel = ref('qwen-coder-plus')
const generatedSql = ref('')
const explanation = ref<string | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

// Clear generated SQL when database changes
watch(() => props.dbName, () => {
  generatedSql.value = ''
  explanation.value = null
  error.value = null
})

async function handleGenerate(): Promise<void> {
  if (!props.dbName || !prompt.value.trim()) return

  loading.value = true
  error.value = null

  try {
    const result = await naturalQueryApi.executeNaturalQuery(props.dbName, {
      prompt: prompt.value,
      modelId: selectedModel.value,
    })
    generatedSql.value = result.sql
    explanation.value = result.explanation
  } catch (e) {
    error.value = (e as Error).message
    generatedSql.value = ''
    explanation.value = null
  } finally {
    loading.value = false
  }
}

function handleCopy(): void {
  navigator.clipboard.writeText(generatedSql.value)
  ElMessage.success('已复制到剪贴板')
}

function handleApply(): void {
  emit('apply', generatedSql.value)
}
</script>

<style scoped>
.generated-sql pre {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
}
</style>
