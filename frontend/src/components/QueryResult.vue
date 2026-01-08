<template>
  <div class="query-result">
    <!-- Result info -->
    <div v-if="result" class="result-info mb-3 flex items-center gap-4 text-sm text-gray-600">
      <span>
        <el-icon><Timer /></el-icon>
        {{ result.executionTime }} ms
      </span>
      <span>
        <el-icon><Document /></el-icon>
        {{ result.rowCount }} 行
      </span>
    </div>

    <!-- Result table -->
    <el-table
      v-if="result && result.columns.length > 0"
      :data="tableData"
      stripe
      border
      max-height="400"
      size="small"
      class="result-table"
    >
      <el-table-column
        v-for="col in result.columns"
        :key="col.name"
        :prop="col.name"
        :label="col.name"
        min-width="120"
        show-overflow-tooltip
      >
        <template #header>
          <div class="flex flex-col">
            <span class="font-medium">{{ col.name }}</span>
            <span class="text-xs text-gray-400">{{ col.type }}</span>
          </div>
        </template>
        <template #default="{ row }">
          <span :class="{ 'text-gray-400 italic': row[col.name] === null }">
            {{ formatValue(row[col.name]) }}
          </span>
        </template>
      </el-table-column>
    </el-table>

    <!-- Empty state -->
    <div
      v-else-if="result && result.columns.length === 0"
      class="empty-result text-center py-8 text-gray-400"
    >
      查询结果为空
    </div>

    <!-- Placeholder -->
    <div
      v-else
      class="placeholder text-center py-8 text-gray-400"
    >
      执行查询后显示结果
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ElTable, ElTableColumn, ElIcon } from 'element-plus'
import { Timer, Document } from '@element-plus/icons-vue'
import type { QueryResult } from '@/services/types'

const props = defineProps<{
  result: QueryResult | null
}>()

// Convert rows array to objects for el-table
const tableData = computed(() => {
  if (!props.result || props.result.columns.length === 0) {
    return []
  }

  const columns = props.result.columns
  return props.result.rows.map((row) => {
    const obj: Record<string, unknown> = {}
    columns.forEach((col, index) => {
      obj[col.name] = row[index]
    })
    return obj
  })
})

function formatValue(value: unknown): string {
  if (value === null || value === undefined) {
    return 'NULL'
  }
  if (typeof value === 'boolean') {
    return value ? 'true' : 'false'
  }
  if (typeof value === 'object') {
    return JSON.stringify(value)
  }
  return String(value)
}
</script>

<style scoped>
.result-table :deep(.el-table__header th) {
  background-color: #f5f7fa;
}
</style>
