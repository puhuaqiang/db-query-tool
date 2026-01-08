<template>
  <div class="field-editor">
    <el-popover
      v-model:visible="popoverVisible"
      trigger="click"
      placement="right"
      :width="250"
    >
      <template #reference>
        <el-button
          size="small"
          type="primary"
          link
          :icon="Edit"
          @click.stop
        />
      </template>
      <div class="p-2">
        <div class="text-sm text-gray-600 mb-2">
          设置字段中文名称
        </div>
        <el-input
          v-model="editValue"
          placeholder="请输入中文名称"
          size="small"
          @keyup.enter="handleSave"
        />
        <div class="flex justify-end gap-2 mt-3">
          <el-button size="small" @click="handleCancel">取消</el-button>
          <el-button size="small" type="primary" :loading="saving" @click="handleSave">
            保存
          </el-button>
        </div>
      </div>
    </el-popover>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { ElPopover, ElInput, ElButton, ElMessage } from 'element-plus'
import { Edit } from '@element-plus/icons-vue'
import { databaseApi } from '@/services/api'

const props = defineProps<{
  dbName: string
  tableName: string
  fieldName: string
  chineseName: string | null
}>()

const emit = defineEmits<{
  updated: [chineseName: string]
}>()

const popoverVisible = ref(false)
const editValue = ref(props.chineseName ?? '')
const saving = ref(false)

watch(() => props.chineseName, (newValue) => {
  editValue.value = newValue ?? ''
})

watch(popoverVisible, (visible) => {
  if (visible) {
    editValue.value = props.chineseName ?? ''
  }
})

async function handleSave(): Promise<void> {
  if (!editValue.value.trim()) {
    ElMessage.warning('请输入中文名称')
    return
  }

  saving.value = true
  try {
    await databaseApi.updateFieldChineseName(
      props.dbName,
      props.tableName,
      props.fieldName,
      { chineseName: editValue.value.trim() }
    )
    emit('updated', editValue.value.trim())
    popoverVisible.value = false
    ElMessage.success('更新成功')
  } catch (e) {
    ElMessage.error((e as Error).message || '更新失败')
  } finally {
    saving.value = false
  }
}

function handleCancel(): void {
  popoverVisible.value = false
  editValue.value = props.chineseName ?? ''
}
</script>
