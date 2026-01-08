<template>
  <el-dropdown trigger="click" @command="handleExport">
    <el-button :disabled="disabled" :loading="loading">
      导出
      <el-icon class="el-icon--right"><ArrowDown /></el-icon>
    </el-button>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item command="csv">
          <el-icon><Document /></el-icon>
          导出为 CSV
        </el-dropdown-item>
        <el-dropdown-item command="json">
          <el-icon><DocumentCopy /></el-icon>
          导出为 JSON
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElDropdown, ElDropdownMenu, ElDropdownItem, ElButton, ElIcon, ElMessage } from 'element-plus'
import { ArrowDown, Document, DocumentCopy } from '@element-plus/icons-vue'
import { queryApi } from '@/services/api'

const props = defineProps<{
  dbName: string
  sql: string
  disabled?: boolean
}>()

const loading = ref(false)

async function handleExport(format: 'csv' | 'json'): Promise<void> {
  if (!props.dbName || !props.sql) {
    ElMessage.warning('请先执行查询')
    return
  }

  loading.value = true
  try {
    const blob = await queryApi.exportQuery(props.dbName, { sql: props.sql }, format)

    // Create download link
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `query_result.${format}`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error((error as Error).message || '导出失败')
  } finally {
    loading.value = false
  }
}
</script>
