import { FileText } from 'lucide-react'

function App() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-3 bg-slate-50 p-6 text-center text-slate-900">
      <div className="flex size-14 items-center justify-center rounded-2xl bg-indigo-600 text-white shadow-lg">
        <FileText size={28} strokeWidth={2} aria-hidden="true" />
      </div>
      <h1 className="text-4xl font-bold tracking-tight">DocuMind</h1>
      <p className="text-lg text-slate-600">Understand Documents. Discover Intelligence.</p>
      <p className="rounded-full bg-indigo-100 px-3 py-1 text-sm font-medium text-indigo-700">
        Frontend scaffold running
      </p>
    </main>
  )
}

export default App