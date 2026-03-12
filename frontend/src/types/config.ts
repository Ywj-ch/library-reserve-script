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

export interface DatetimeRange {
  start: string
  end: string
}

export interface ReserveConfig {
  send_time: string
  seats: Seat[]
  retry: {
    delay_seconds: number
  }
  datetime_range?: DatetimeRange
}

export interface Config {
  auth: AuthConfig
  reserve: ReserveConfig
}
