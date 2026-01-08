// Database types
export interface DatabaseConnection {
  id: number
  name: string
  dbType: 'postgres' | 'mysql'
  createdAt: string
  updatedAt: string
}

export interface DatabaseConnectionDetail extends DatabaseConnection {
  tables: TableMetadata[]
}

export interface TableMetadata {
  id: number
  tableName: string
  tableType: 'TABLE' | 'VIEW'
  chineseName: string | null
  fields: FieldMetadata[]
}

export interface FieldMetadata {
  id: number
  fieldName: string
  dataType: string
  isNullable: boolean
  columnDefault: string | null
  maxLength: number | null
  chineseName: string | null
}

// Request types
export interface AddDatabaseRequest {
  url: string
}

export interface QueryRequest {
  sql: string
}

export interface NaturalQueryRequest {
  prompt: string
  modelId?: string
}

export interface UpdateFieldRequest {
  chineseName: string
}

// Response types
export interface Column {
  name: string
  type: string
}

export interface QueryResult {
  columns: Column[]
  rows: unknown[][]
  rowCount: number
  executionTime: number
}

export interface NaturalQueryResult {
  sql: string
  explanation: string | null
  modelId: string
}

export interface LlmModel {
  id: string
  name: string
  provider: string
}

export interface ErrorResponse {
  error: string
  message: string
  detail?: string
}
