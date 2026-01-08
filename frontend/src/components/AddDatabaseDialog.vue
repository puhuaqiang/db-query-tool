<template>
  <el-dialog
    v-model="visible"
    title="添加数据库连接"
    width="500px"
    :close-on-click-modal="false"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="100px"
      label-position="left"
    >
      <el-form-item label="连接名称" prop="name">
        <el-input
          v-model="form.name"
          placeholder="请输入连接名称，如 my-postgres"
        />
      </el-form-item>
      <el-form-item label="连接字符串" prop="url">
        <el-input
          v-model="form.url"
          type="textarea"
          :rows="3"
          placeholder="postgres://user:password@host:5432/database"
        />
      </el-form-item>
      <div class="text-xs text-gray-500 mt-2">
        <p>支持的格式:</p>
        <ul class="list-disc list-inside ml-2">
          <li>PostgreSQL: postgres://user:pass@host:5432/dbname</li>
          <li>MySQL: mysql://user:pass@host:3306/dbname</li>
        </ul>
      </div>
    </el-form>
    <template #footer>
      <el-button @click="handleClose">取消</el-button>
      <el-button type="primary" :loading="loading" @click="handleSubmit">
        连接
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElDialog, ElForm, ElFormItem, ElInput, ElButton, ElMessage } from 'element-plus'
import { useDatabaseStore } from '@/stores/database'

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  success: []
}>()

const store = useDatabaseStore()
const formRef = ref<FormInstance>()
const loading = ref(false)

const visible = ref(props.modelValue)

watch(
  () => props.modelValue,
  (val) => {
    visible.value = val
  }
)

watch(visible, (val) => {
  emit('update:modelValue', val)
  if (!val) {
    resetForm()
  }
})

const form = reactive({
  name: '',
  url: '',
})

const rules: FormRules = {
  name: [
    { required: true, message: '请输入连接名称', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9_-]+$/, message: '只允许字母、数字、下划线和中划线', trigger: 'blur' },
  ],
  url: [
    { required: true, message: '请输入连接字符串', trigger: 'blur' },
    {
      pattern: /^(postgres|postgresql|mysql):\/\/.+/,
      message: '请输入有效的数据库连接字符串',
      trigger: 'blur',
    },
  ],
}

function resetForm(): void {
  form.name = ''
  form.url = ''
  formRef.value?.resetFields()
}

function handleClose(): void {
  visible.value = false
}

async function handleSubmit(): Promise<void> {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  try {
    await store.addDatabase(form.name, form.url)
    ElMessage.success('数据库连接成功')
    emit('success')
    handleClose()
  } catch (error) {
    ElMessage.error((error as Error).message || '连接失败')
  } finally {
    loading.value = false
  }
}
</script>
