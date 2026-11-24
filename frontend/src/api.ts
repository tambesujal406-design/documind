/**
 * Talks to the DocuMind backend.
 * The backend address comes from VITE_API_BASE_URL (see frontend/.env.example).
 * It is never written into the code, so production can point somewhere else (TD-014).
 */

const rawBaseUrl = import.meta.env.VITE_API_BASE_URL

/** The backend address without a trailing slash, or an empty string if it is not set. */
export const API_BASE_URL = rawBaseUrl?.trim().replace(/\/+$/, '') ?? ''

export type HealthResponse = {
  status: string
  service: string
}

export class ApiNotConfiguredError extends Error {
  constructor() {
    super('VITE_API_BASE_URL is not set. Copy frontend/.env.example to frontend/.env.local and restart the dev server.')
    this.name = 'ApiNotConfiguredError'
  }
}

/** Ask the backend whether it is running (GET /health). */
export async function getHealth(signal?: AbortSignal): Promise<HealthResponse> {
  if (!API_BASE_URL) {
    throw new ApiNotConfiguredError()
  }
  const response = await fetch(`${API_BASE_URL}/health`, { signal })
  if (!response.ok) {
    throw new Error(`The backend answered with status ${response.status}`)
  }
  return (await response.json()) as HealthResponse
}