import api from './index'
import type { ApiResponse } from '@/types/api'
import type { AuthConfig, ReserveConfig, Config } from '@/types/config'

export const configApi = {
  async getFullConfig(): Promise<ApiResponse<Config>> {
    return api.get('/config')
  },

  async getAuthConfig(): Promise<ApiResponse<AuthConfig>> {
    return api.get('/config/auth')
  },

  async updateAuthConfig(data: { cookie: string; code: string }): Promise<ApiResponse<AuthConfig>> {
    return api.put('/config/auth', data)
  },

  async getReserveConfig(): Promise<ApiResponse<ReserveConfig>> {
    return api.get('/config/reserve')
  },

  async updateReserveConfig(data: Partial<ReserveConfig>): Promise<ApiResponse<ReserveConfig>> {
    return api.put('/config/reserve', data)
  },

  async testConfig(): Promise<ApiResponse<{ valid: boolean; message: string }>> {
    return api.post('/config/test')
  },
}
