import { defineStore } from 'pinia'
import { ref } from 'vue'
import type {
  DatabaseConnection,
  DatabaseConnectionDetail,
  QueryResult,
  LlmModel,
} from '@/services/types'
import { databaseApi, queryApi, naturalQueryApi } from '@/services/api'

export const useDatabaseStore = defineStore('database', () => {
  // State
  const databases = ref<DatabaseConnection[]>([])
  const currentDatabase = ref<DatabaseConnectionDetail | null>(null)
  const queryResult = ref<QueryResult | null>(null)
  const llmModels = ref<LlmModel[]>([])
  const selectedLlmModel = ref<string>('qwen-coder-plus')
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Helper actions
  function setLoading(value: boolean): void {
    isLoading.value = value
  }

  function setError(message: string | null): void {
    error.value = message
  }

  function clearError(): void {
    error.value = null
  }

  // Database actions
  async function fetchDatabases(): Promise<void> {
    setLoading(true)
    clearError()
    try {
      databases.value = await databaseApi.getDatabases()
    } catch (e) {
      setError((e as Error).message)
      throw e
    } finally {
      setLoading(false)
    }
  }

  async function addDatabase(name: string, url: string): Promise<void> {
    setLoading(true)
    clearError()
    try {
      const result = await databaseApi.addDatabase(name, { url })
      // Update databases list
      const existingIndex = databases.value.findIndex((db) => db.name === name)
      if (existingIndex >= 0) {
        databases.value[existingIndex] = result
      } else {
        databases.value.push(result)
      }
      currentDatabase.value = result
    } catch (e) {
      setError((e as Error).message)
      throw e
    } finally {
      setLoading(false)
    }
  }

  async function selectDatabase(name: string): Promise<void> {
    setLoading(true)
    clearError()
    try {
      currentDatabase.value = await databaseApi.getDatabase(name)
    } catch (e) {
      setError((e as Error).message)
      throw e
    } finally {
      setLoading(false)
    }
  }

  async function deleteDatabase(name: string): Promise<void> {
    setLoading(true)
    clearError()
    try {
      await databaseApi.deleteDatabase(name)
      databases.value = databases.value.filter((db) => db.name !== name)
      if (currentDatabase.value?.name === name) {
        currentDatabase.value = null
      }
    } catch (e) {
      setError((e as Error).message)
      throw e
    } finally {
      setLoading(false)
    }
  }

  async function refreshMetadata(name: string): Promise<void> {
    setLoading(true)
    clearError()
    try {
      const result = await databaseApi.refreshMetadata(name)
      if (currentDatabase.value?.name === name) {
        currentDatabase.value = result
      }
    } catch (e) {
      setError((e as Error).message)
      throw e
    } finally {
      setLoading(false)
    }
  }

  // Query actions
  async function executeQuery(sql: string): Promise<QueryResult> {
    if (!currentDatabase.value) {
      throw new Error('请先选择数据库')
    }
    setLoading(true)
    clearError()
    try {
      const result = await queryApi.executeQuery(currentDatabase.value.name, { sql })
      queryResult.value = result
      return result
    } catch (e) {
      setError((e as Error).message)
      throw e
    } finally {
      setLoading(false)
    }
  }

  function clearQueryResult(): void {
    queryResult.value = null
  }

  // LLM actions
  async function fetchLlmModels(): Promise<void> {
    try {
      llmModels.value = await naturalQueryApi.getLlmModels()
      if (llmModels.value.length > 0 && !selectedLlmModel.value) {
        selectedLlmModel.value = llmModels.value[0].id
      }
    } catch (e) {
      console.error('Failed to fetch LLM models:', e)
    }
  }

  function setSelectedLlmModel(modelId: string): void {
    selectedLlmModel.value = modelId
  }

  // Metadata actions
  function updateFieldChineseNameLocal(
    tableName: string,
    fieldName: string,
    chineseName: string
  ): void {
    if (!currentDatabase.value) return
    const table = currentDatabase.value.tables.find((t) => t.tableName === tableName)
    if (!table) return
    const field = table.fields.find((f) => f.fieldName === fieldName)
    if (field) {
      field.chineseName = chineseName
    }
  }

  return {
    // State
    databases,
    currentDatabase,
    queryResult,
    llmModels,
    selectedLlmModel,
    isLoading,
    error,
    // Actions
    setLoading,
    setError,
    clearError,
    fetchDatabases,
    addDatabase,
    selectDatabase,
    deleteDatabase,
    refreshMetadata,
    executeQuery,
    clearQueryResult,
    fetchLlmModels,
    setSelectedLlmModel,
    updateFieldChineseNameLocal,
  }
})
