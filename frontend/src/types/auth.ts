export type User = {
  email: string
  full_name: string
  role: string
}

export type LoginResponse = {
  access_token: string
  token_type: string
}
