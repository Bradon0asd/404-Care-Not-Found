// The backend answers every call with { success, data } or { success, error }.
// Everything here unwraps that envelope so callers only ever see the payload.

const BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? '').replace(/\/$/, '')

export class ApiError extends Error {
  code: string
  status: number
  details: unknown

  constructor(code: string, message: string, status: number, details?: unknown) {
    super(message)
    this.name = 'ApiError'
    this.code = code
    this.status = status
    this.details = details
  }
}

type ApiEnvelope<T> =
  | { success: true; data: T }
  | { success: false; error: { code: string; message: string; details?: unknown } }

export async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const isFormData = init.body instanceof FormData
  let response: Response
  try {
    response = await fetch(`${BASE_URL}${path}`, {
      ...init,
      // The session lives in a cookie the backend sets, so it has to travel cross-origin.
      credentials: 'include',
      headers: {
        ...(isFormData ? {} : { 'Content-Type': 'application/json' }),
        // Free ngrok tunnels answer browser requests with a warning page without this.
        'ngrok-skip-browser-warning': 'true',
        ...init.headers,
      },
    })
  } catch {
    throw new ApiError('NETWORK_ERROR', '連不到伺服器', 0)
  }

  let body: ApiEnvelope<T> | null = null
  try {
    body = (await response.json()) as ApiEnvelope<T>
  } catch {
    body = null
  }

  if (!response.ok || !body || body.success === false) {
    const error = body && body.success === false ? body.error : null
    throw new ApiError(
      error?.code ?? 'UNEXPECTED_ERROR',
      error?.message ?? response.statusText,
      response.status,
      error?.details,
    )
  }

  return body.data
}

export function post<T>(path: string, payload?: unknown) {
  return request<T>(path, {
    method: 'POST',
    body: payload === undefined ? undefined : JSON.stringify(payload),
  })
}

export function postForm<T>(path: string, formData: FormData) {
  return request<T>(path, {
    method: 'POST',
    body: formData,
  })
}

export function get<T>(path: string) {
  return request<T>(path)
}

export function patch<T>(path: string, payload: unknown) {
  return request<T>(path, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  })
}

export function del<T>(path: string) {
  return request<T>(path, {
    method: 'DELETE',
  })
}
