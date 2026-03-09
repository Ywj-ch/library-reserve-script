export interface SeatAttempt {
  seat_id: string
  status_code: number
  response_text: string
  success: boolean
}

export interface LogEntry {
  timestamp: string
  level: string
  message: string
  seat?: string
  status?: 'success' | 'failure' | 'pending'
}

export interface AggregatedLogEntry {
  session_id: string
  timestamp: string
  start_time?: string
  end_time?: string
  status: 'success' | 'failure' | 'pending'
  seats: SeatAttempt[]
  details: string[]
  success_seat?: string
  total_attempts: number
  message: string
}

export interface LogPagination {
  total: number
  page: number
  limit: number
}

export interface LogListResponse {
  logs: AggregatedLogEntry[]
  pagination: LogPagination
}

export interface LogStats {
  total_requests: number
  success_count: number
  failure_count: number
  success_rate: number
  last_success?: string
}
