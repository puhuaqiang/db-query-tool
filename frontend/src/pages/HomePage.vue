<template>
  <div class="home-page h-full">
    <el-container class="h-full">
      <!-- Left sidebar: Database list -->
      <el-aside width="360px" class="bg-white border-r border-gray-200 p-4 overflow-auto">
        <div class="mb-4 flex justify-between items-center">
          <h2 class="text-lg font-medium">数据库连接</h2>
          <el-button type="primary" size="small" @click="showAddDialog = true">
            <el-icon class="mr-1"><Plus /></el-icon>
            添加
          </el-button>
        </div>

        <div v-if="store.isLoading && !store.currentDatabase" class="text-center py-4">
          <el-icon class="is-loading"><Loading /></el-icon>
        </div>

        <DatabaseList
          v-else
          @select="handleSelectDatabase"
        />

        <!-- Table list when database selected -->
        <div v-if="store.currentDatabase" class="mt-6">
          <div class="flex justify-between items-center mb-3">
            <h3 class="text-md font-medium">表结构</h3>
            <el-button
              size="small"
              :loading="store.isLoading"
              @click="handleRefresh"
            >
              刷新
            </el-button>
          </div>
          <TableList :tables="store.currentDatabase.tables" :db-name="store.currentDatabase.name" />
        </div>

        <!-- Add Database Dialog -->
        <AddDatabaseDialog
          v-model="showAddDialog"
          @success="handleDatabaseAdded"
        />
      </el-aside>

      <!-- Main content area -->
      <el-main class="p-4 bg-gray-50 overflow-auto">
        <div v-if="store.error" class="mb-4">
          <el-alert :title="store.error" type="error" show-icon closable @close="store.clearError" />
        </div>

        <div class="flex flex-col gap-4 h-full">
          <!-- Top row: Natural Query + SQL Editor side by side -->
          <div class="flex gap-4 flex-shrink-0">
            <!-- Natural Query area -->
            <div class="bg-white rounded-lg shadow p-4 flex-1 min-w-0 overflow-hidden">
              <h3 class="text-md font-medium mb-3">自然语言查询</h3>
              <NaturalQueryInput
                :db-name="store.currentDatabase?.name ?? ''"
                :disabled="!store.currentDatabase"
                @apply="handleApplySql"
              />
            </div>

            <!-- SQL Editor area -->
            <div class="bg-white rounded-lg shadow p-4 flex-1 min-w-0 overflow-hidden">
              <h3 class="text-md font-medium mb-3">SQL 查询</h3>
              <SqlEditor
                v-model="sql"
                :disabled="!store.currentDatabase"
                :error="queryError"
                @execute="handleExecuteQuery"
              />
              <div class="mt-3 flex gap-2">
                <el-button
                  type="primary"
                  :disabled="!store.currentDatabase || !sql.trim()"
                  :loading="isExecuting"
                  @click="handleExecuteQuery"
                >
                  执行查询
                </el-button>
                <ExportDialog
                  :db-name="store.currentDatabase?.name ?? ''"
                  :sql="sql"
                  :disabled="!store.queryResult"
                />
              </div>
            </div>
          </div>

          <!-- Query results area - takes remaining space -->
          <div class="bg-white rounded-lg shadow p-4 flex-1 min-h-[400px] overflow-auto">
            <h3 class="text-md font-medium mb-3">查询结果</h3>
            <QueryResult :result="store.queryResult" />
          </div>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElContainer, ElAside, ElMain, ElButton, ElIcon, ElAlert } from 'element-plus'
import { Plus, Loading } from '@element-plus/icons-vue'
import { useDatabaseStore } from '@/stores/database'
import DatabaseList from '@/components/DatabaseList.vue'
import AddDatabaseDialog from '@/components/AddDatabaseDialog.vue'
import TableList from '@/components/TableList.vue'
import SqlEditor from '@/components/SqlEditor.vue'
import QueryResult from '@/components/QueryResult.vue'
import ExportDialog from '@/components/ExportDialog.vue'
import NaturalQueryInput from '@/components/NaturalQueryInput.vue'

const store = useDatabaseStore()
const showAddDialog = ref(false)
const sql = ref('')
const queryError = ref<string | undefined>(undefined)
const isExecuting = ref(false)

onMounted(async () => {
  try {
    await store.fetchDatabases()
  } catch {
    // Error is handled in store
  }
})

async function handleSelectDatabase(name: string): Promise<void> {
  try {
    await store.selectDatabase(name)
    // Clear query state when switching databases
    sql.value = ''
    queryError.value = undefined
    store.clearQueryResult()
  } catch {
    // Error is handled in store
  }
}

function handleDatabaseAdded(): void {
  // Database is already added to store in the dialog
}

async function handleRefresh(): Promise<void> {
  if (!store.currentDatabase) return
  try {
    await store.refreshMetadata(store.currentDatabase.name)
  } catch {
    // Error is handled in store
  }
}

async function handleExecuteQuery(): Promise<void> {
  if (!store.currentDatabase || !sql.value.trim()) return

  isExecuting.value = true
  queryError.value = undefined

  try {
    await store.executeQuery(sql.value)
  } catch (e) {
    queryError.value = (e as Error).message
  } finally {
    isExecuting.value = false
  }
}

function handleApplySql(generatedSql: string): void {
  sql.value = generatedSql
}
</script>

<style scoped>
.home-page {
  height: calc(100vh - 60px);
}

/* Fix Element Plus container layout */
.home-page :deep(.el-container) {
  display: flex;
  flex-direction: row;
}

.home-page :deep(.el-main) {
  flex: 1;
  overflow: auto;
  width: 0; /* Force flex item to respect flex-basis */
}
</style>
