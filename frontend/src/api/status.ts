import api from './index'
import type { ApiResponse, SystemStatus } from '@/types/api'

export const statusApi = {
  async getStatus(): Promise<ApiResponse<SystemStatus>> {
    return api.get('/status')
  },

  async healthCheck(): Promise<{ status: string; timestamp: string }> {
    return api.get('/status/health')
  },
}
