import api from './index'
import type { ApiResponse } from '@/types/api'
import type { LogListResponse, LogStats } from '@/types/log'

export const logsApi = {
  async getLogs(params?: {
    page?: number
    limit?: number
    date?: string
    status?: string
  }): Promise<ApiResponse<LogListResponse>> {
    return api.get('/logs', { params })
  },

  async getStats(): Promise<ApiResponse<LogStats>> {
    return api.get('/logs/stats')
  },
}
