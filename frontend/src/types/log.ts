export interface LogEntry {
  timestamp: string
  level: string
  message: string
  seat?: string
  status?: 'success' | 'failure' | 'pending'
}

export interface LogPagination {
  total: number
  page: number
  limit: number
}

export interface LogListResponse {
  logs: LogEntry[]
  pagination: LogPagination
}

export interface LogStats {
  total_requests: number
  success_count: number
  failure_count: number
  success_rate: number
  last_success?: string
}
