export interface Seat {
  id: string
  name: string
  enabled: boolean
}

export interface AuthConfig {
  cookie: string
  code: string
  last_update: string
  days_remaining: number
}

export interface ReserveConfig {
  send_time: string
  seats: Seat[]
  retry: {
    max_attempts: number
    delay_seconds: number
  }
}

export interface Config {
  auth: AuthConfig
  reserve: ReserveConfig
}
