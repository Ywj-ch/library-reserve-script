import api from './index'
import type { ApiResponse } from '@/types/api'

export interface ReserveResult {
  session_id: string
  status: 'success' | 'failure' | 'pending'
  success_seat: string | null
  total_attempts: number
  details: string[]
  seats: Array<{
    seat_id: string
    status_code: number
    response_text: string
    success: boolean
  }>
}

export const reserveApi = {
  async runReserve(): Promise<ApiResponse<ReserveResult>> {
    return api.post('/reserve/run')
  },
}
