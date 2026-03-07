export interface ApiResponse<T = any> {
  success: boolean
  data: T
  message?: string
}

export interface SystemStatus {
  status: string
  config_valid: boolean
  days_remaining: number
  next_run: string
  last_run?: string
  last_result: string
  uptime_info: {
    total_requests: number
    success_rate: number
  }
}
