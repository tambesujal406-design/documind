import { useEffect, useState } from 'react'
import { FileText } from 'lucide-react'
import { ApiNotConfiguredError, getHealth } from './api.ts'

/** What the page knows about the backend right now. */
type BackendStatus =
  | { kind: 'checking' }
  | { kind: 'connected'; service: string }
  | { kind: 'not-configured' }
  | { kind: 'unreachable' }

/** Ask the backend once, when the page opens, and report what happened. */
function useBackendStatus(): BackendStatus {
  const [status, setStatus] = useState<BackendStatus>({ kind: 'checking' })

  useEffect(() => {
    const controller = new AbortController()

    getHealth(controller.signal)
      .then((health) => {
        if (controller.signal.aborted) return
        setStatus({ kind: 'connected', service: health.service })
      })
      .catch((error: unknown) => {
        if (controller.signal.aborted) return
        setStatus(
          error instanceof ApiNotConfiguredError
            ? { kind: 'not-configured' }
            : { kind: 'unreachable' },
        )
      })

    // If the page closes (or React re-runs this effect), drop the request and
    // ignore its result so an old answer can never overwrite a newer one.
    return () => controller.abort()
  }, [])

  return status
}

type Badge = {
  label: string
  hint?: string
  pill: string
  dot: string
}

/** How each status looks. Full class names are written out so Tailwind can find them. */
function describe(status: BackendStatus): Badge {
  switch (status.kind) {
    case 'checking':
      return {
        label: 'Checking the backend…',
        pill: 'bg-amber-50 text-amber-800 ring-amber-200',
        dot: 'bg-amber-500 animate-pulse',
      }
    case 'connected':
      return {
        label: `Backend connected (${status.service})`,
        pill: 'bg-emerald-50 text-emerald-800 ring-emerald-200',
        dot: 'bg-emerald-500',
      }
    case 'not-configured':
      return {
        label: 'Backend address not set',
        hint: 'Copy .env.example to .env.local, then restart npm run dev.',
        pill: 'bg-rose-50 text-rose-800 ring-rose-200',
        dot: 'bg-rose-500',
      }
    case 'unreachable':
      return {
        label: 'Backend not reachable',
        hint: 'Start it with: python -m uvicorn app.main:app --reload',
        pill: 'bg-rose-50 text-rose-800 ring-rose-200',
        dot: 'bg-rose-500',
      }
  }
}

function App() {
  const badge = describe(useBackendStatus())

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4 bg-slate-50 px-6 text-center">
      <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-indigo-600 text-white shadow-lg shadow-indigo-200">
        <FileText className="h-8 w-8" aria-hidden="true" />
      </div>
      <h1 className="text-4xl font-bold tracking-tight text-slate-900">DocuMind</h1>
      <p className="max-w-md text-lg text-slate-600">Understand Documents. Discover Intelligence.</p>
      <div
        role="status"
        className={`inline-flex items-center gap-2 rounded-full px-3 py-1 text-sm font-medium ring-1 ring-inset ${badge.pill}`}
      >
        <span aria-hidden="true" className={`h-2 w-2 rounded-full ${badge.dot}`} />
        {badge.label}
      </div>
      {badge.hint && <p className="max-w-md text-sm text-slate-500">{badge.hint}</p>}
    </main>
  )
}

export default App