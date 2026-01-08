import axios, { type AxiosInstance, type AxiosError } from 'axios'
import type {
  DatabaseConnection,
  DatabaseConnectionDetail,
  AddDatabaseRequest,
  QueryRequest,
  QueryResult,
  NaturalQueryRequest,
  NaturalQueryResult,
  LlmModel,
  UpdateFieldRequest,
  FieldMetadata,
} from './types'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1'

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
})

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<{ message?: string; error?: string; detail?: string }>) => {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.response?.data?.error ||
      error.message ||
      '请求失败'
    return Promise.reject(new Error(message))
  }
)

// Database API
export const databaseApi = {
  // Get all databases
  async getDatabases(): Promise<DatabaseConnection[]> {
    const response = await apiClient.get<DatabaseConnection[]>('/dbs')
    return response.data
  },

  // Add database
  async addDatabase(name: string, request: AddDatabaseRequest): Promise<DatabaseConnectionDetail> {
    const response = await apiClient.put<DatabaseConnectionDetail>(`/dbs/${name}`, request)
    return response.data
  },

  // Get database with metadata
  async getDatabase(name: string): Promise<DatabaseConnectionDetail> {
    const response = await apiClient.get<DatabaseConnectionDetail>(`/dbs/${name}`)
    return response.data
  },

  // Delete database
  async deleteDatabase(name: string): Promise<void> {
    await apiClient.delete(`/dbs/${name}`)
  },

  // Refresh metadata
  async refreshMetadata(name: string): Promise<DatabaseConnectionDetail> {
    const response = await apiClient.post<DatabaseConnectionDetail>(`/dbs/${name}/refresh`)
    return response.data
  },

  // Update field chinese name
  async updateFieldChineseName(
    dbName: string,
    tableName: string,
    fieldName: string,
    request: UpdateFieldRequest
  ): Promise<FieldMetadata> {
    const response = await apiClient.patch<FieldMetadata>(
      `/dbs/${dbName}/tables/${tableName}/fields/${fieldName}`,
      request
    )
    return response.data
  },
}

// Query API (to be implemented in US2)
export const queryApi = {
  async executeQuery(dbName: string, request: QueryRequest): Promise<QueryResult> {
    const response = await apiClient.post<QueryResult>(`/dbs/${dbName}/query`, request)
    return response.data
  },

  async exportQuery(dbName: string, request: QueryRequest, format: 'csv' | 'json'): Promise<Blob> {
    const response = await apiClient.post(`/dbs/${dbName}/query/export`, request, {
      params: { format },
      responseType: 'blob',
    })
    return response.data
  },
}

// Natural query API (to be implemented in US3)
export const naturalQueryApi = {
  async executeNaturalQuery(
    dbName: string,
    request: NaturalQueryRequest
  ): Promise<NaturalQueryResult> {
    const response = await apiClient.post<NaturalQueryResult>(
      `/dbs/${dbName}/query/natural`,
      request
    )
    return response.data
  },

  async getLlmModels(): Promise<LlmModel[]> {
    const response = await apiClient.get<LlmModel[]>('/llm/models')
    return response.data
  },
}

export { apiClient }
export default apiClient
