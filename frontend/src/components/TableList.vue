<template>
  <div class="table-list">
    <el-tree
      v-if="tables.length > 0"
      :data="treeData"
      :props="{ label: 'label', children: 'children' }"
      default-expand-all
      highlight-current
      @node-click="handleNodeClick"
    >
      <template #default="{ node, data }">
        <div class="flex items-center gap-2 text-sm w-full">
          <el-icon v-if="data.type === 'table'" :size="14">
            <Grid />
          </el-icon>
          <el-icon v-else-if="data.type === 'field'" :size="14">
            <Document />
          </el-icon>
          <span>{{ node.label }}</span>
          <el-tag v-if="data.dataType" size="small" type="info" class="ml-1">
            {{ data.dataType }}
          </el-tag>
          <span v-if="data.chineseName" class="text-gray-400 text-xs">
            ({{ data.chineseName }})
          </span>
          <div v-if="data.type === 'field' && dbName" class="ml-auto">
            <FieldEditor
              :db-name="dbName"
              :table-name="data.tableName"
              :field-name="data.fieldName"
              :chinese-name="data.chineseName"
              @updated="(name) => handleFieldUpdated(data.tableName, data.fieldName, name)"
            />
          </div>
        </div>
      </template>
    </el-tree>
    <div v-else class="text-gray-400 text-sm text-center py-4">
      暂无表信息
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ElTree, ElIcon, ElTag } from 'element-plus'
import { Grid, Document } from '@element-plus/icons-vue'
import type { TableMetadata } from '@/services/types'
import { useDatabaseStore } from '@/stores/database'
import FieldEditor from './FieldEditor.vue'

interface TreeNode {
  label: string
  type: 'table' | 'field'
  tableName?: string
  fieldName?: string
  dataType?: string
  chineseName?: string | null
  children?: TreeNode[]
}

const props = defineProps<{
  tables: TableMetadata[]
  dbName?: string
}>()

const store = useDatabaseStore()

const emit = defineEmits<{
  selectField: [tableName: string, fieldName: string]
}>()

const treeData = computed<TreeNode[]>(() => {
  return props.tables.map((table) => ({
    label: `${table.tableName} (${table.tableType})`,
    type: 'table' as const,
    tableName: table.tableName,
    children: table.fields.map((field) => ({
      label: field.fieldName,
      type: 'field' as const,
      tableName: table.tableName,
      fieldName: field.fieldName,
      dataType: field.dataType,
      chineseName: field.chineseName,
    })),
  }))
})

function handleNodeClick(data: TreeNode): void {
  if (data.type === 'field' && data.tableName && data.fieldName) {
    emit('selectField', data.tableName, data.fieldName)
  }
}

function handleFieldUpdated(tableName: string, fieldName: string, chineseName: string): void {
  store.updateFieldChineseNameLocal(tableName, fieldName, chineseName)
}
</script>

<style scoped>
.table-list :deep(.el-tree-node__content) {
  height: 32px;
}
</style>
