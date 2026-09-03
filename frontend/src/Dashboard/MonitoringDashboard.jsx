import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  Activity,
  AlertTriangle,
  CheckCircle2,
  Clock3,
  RefreshCw,
  Server,
  ShieldCheck,
  TriangleAlert,
} from 'lucide-react'

const metricValue = (metrics, keys) => {
  for (const key of keys) {
    if (metrics?.[key] !== undefined && metrics?.[key] !== null) return metrics[key]
  }
  return null
}

const formatNumber = (value) => {
  if (value === null || value === undefined) return '—'
  return Number(value).toLocaleString('fr-FR', { maximumFractionDigits: 1 })
}

const formatPercent = (value) => {
  if (value === null || value === undefined) return '—'
  const percent = Number(value) <= 1 ? Number(value) * 100 : Number(value)
  return `${percent.toLocaleString('fr-FR', { maximumFractionDigits: 1 })} %`
}

const formatLatency = (value) => {
  if (value === null || value === undefined) return '—'
  return `${Number(value).toLocaleString('fr-FR', { maximumFractionDigits: 0 })} ms`
}

function MetricCard({ title, value, hint, icon, tone = 'green' }) {
  const tones = {
    green: 'bg-green-50 text-green-700 border-green-100',
    amber: 'bg-amber-50 text-amber-700 border-amber-100',
    blue: 'bg-blue-50 text-blue-700 border-blue-100',
    rose: 'bg-rose-50 text-rose-700 border-rose-100',
  }

  return (
    <article className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-sm font-medium text-gray-500">{title}</p>
          <p className="mt-2 text-3xl font-bold text-gray-900">{value}</p>
        </div>
        <div className={`rounded-xl border p-3 ${tones[tone]}`}>{icon}</div>
      </div>
      <p className="mt-3 text-xs text-gray-500">{hint}</p>
    </article>
  )
}

export default function MonitoringDashboard() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [lastUpdated, setLastUpdated] = useState(null)

  const loadMonitoring = useCallback(async () => {
    setLoading(true)
    setError('')

    try {
      const response = await fetch('/stats/monitoring')
      if (!response.ok) throw new Error(`Le service a répondu ${response.status}`)
      const payload = await response.json()
      setData(payload)
      setLastUpdated(new Date())
    } catch (requestError) {
      setError(requestError.message || 'Impossible de récupérer les métriques.')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadMonitoring()
  }, [loadMonitoring])

  const application = data?.application ?? data?.metrics?.application ?? data?.metrics ?? {}
  const model = data?.model ?? data?.metrics?.model ?? {}
  const alerts = Array.isArray(data?.alerts) ? data.alerts : []
  const status = String(data?.monitoring_status ?? data?.status ?? 'ok').toLowerCase()
  const isAlert = status === 'alert' || alerts.length > 0

  const requests = metricValue(application, ['request_count', 'total_requests', 'requests', 'total'])
  const errors = metricValue(application, ['error_rate', 'error_rate_percent', 'failure_rate', 'errors_rate'])
  const latency = metricValue(application, ['average_latency_ms', 'avg_latency_ms', 'average_duration_ms', 'avg_duration_ms'])
  const uncertainty = metricValue(model, ['uncertain_prediction_rate', 'uncertainty_rate', 'uncertain_rate', 'uncertain_predictions_rate', 'low_confidence_rate'])

  return (
    <main className="min-h-screen bg-slate-50 font-sans text-gray-800">
      <header className="border-b border-gray-200 bg-white">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-6 py-5">
          <div>
            <p className="text-sm font-semibold text-ecoGreen">ECO-TRI IA · C20</p>
            <h1 className="text-2xl font-bold text-gray-900">Monitoring applicatif</h1>
            <p className="mt-1 text-sm text-gray-500">Suivi technique local du service de prédiction.</p>
          </div>
          <div className="flex items-center gap-3">
            <Link to="/scan" className="rounded-lg border border-gray-200 px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-50">
              Retour au scanner
            </Link>
            <button
              type="button"
              onClick={loadMonitoring}
              disabled={loading}
              className="inline-flex items-center gap-2 rounded-lg bg-ecoGreen px-4 py-2 text-sm font-semibold text-white transition hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
              <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
              Actualiser
            </button>
          </div>
        </div>
      </header>

      <section className="mx-auto max-w-6xl px-6 py-8">
        <div className={`mb-6 flex items-center gap-3 rounded-2xl border p-4 ${isAlert ? 'border-amber-200 bg-amber-50' : 'border-green-200 bg-green-50'}`}>
          {isAlert ? <TriangleAlert className="h-6 w-6 text-amber-600" /> : <CheckCircle2 className="h-6 w-6 text-green-600" />}
          <div>
            <p className={`font-bold ${isAlert ? 'text-amber-900' : 'text-green-900'}`}>
              Statut : {isAlert ? 'ALERTE' : 'OK'}
            </p>
            <p className={`text-sm ${isAlert ? 'text-amber-800' : 'text-green-800'}`}>
              {isAlert ? 'Une métrique a dépassé un seuil de surveillance.' : 'Les métriques sont sous les seuils d’alerte configurés.'}
            </p>
          </div>
        </div>

        {error && (
          <div className="mb-6 flex items-center gap-3 rounded-xl border border-rose-200 bg-rose-50 p-4 text-rose-800">
            <AlertTriangle className="h-5 w-5" />
            <p>Erreur de récupération : {error}</p>
          </div>
        )}

        <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
          <MetricCard title="Requêtes" value={formatNumber(requests)} hint="Volume de demandes traitées" icon={<Server className="h-6 w-6" />} tone="blue" />
          <MetricCard title="Taux d’erreurs" value={formatPercent(errors)} hint="Alerte à partir de 5 %" icon={<AlertTriangle className="h-6 w-6" />} tone="rose" />
          <MetricCard title="Latence moyenne" value={formatLatency(latency)} hint="Alerte à partir de 2 000 ms" icon={<Clock3 className="h-6 w-6" />} tone="amber" />
          <MetricCard title="Prédictions incertaines" value={formatPercent(uncertainty)} hint="Alerte à partir de 20 %" icon={<Activity className="h-6 w-6" />} tone="green" />
        </div>

        <div className="mt-6 grid gap-6 lg:grid-cols-[1.3fr_0.7fr]">
          <section className="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm">
            <h2 className="flex items-center gap-2 text-lg font-bold text-gray-900">
              <AlertTriangle className="h-5 w-5 text-amber-500" />
              Alertes actives
            </h2>
            {alerts.length === 0 ? (
              <p className="mt-4 rounded-xl bg-green-50 p-4 text-sm text-green-800">Aucune alerte active : le service est dans les seuils configurés.</p>
            ) : (
              <ul className="mt-4 space-y-3">
                {alerts.map((alert, index) => (
                  <li key={index} className="rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900">
                    {typeof alert === 'string' ? alert : alert.message ?? alert.metric ?? JSON.stringify(alert)}
                  </li>
                ))}
              </ul>
            )}
          </section>

          <aside className="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm">
            <h2 className="flex items-center gap-2 text-lg font-bold text-gray-900">
              <ShieldCheck className="h-5 w-5 text-ecoGreen" />
              Seuils configurés
            </h2>
            <dl className="mt-4 space-y-3 text-sm">
              <div className="flex justify-between gap-4 border-b border-gray-100 pb-3"><dt className="text-gray-500">Erreurs</dt><dd className="font-semibold text-gray-900">≥ 5 %</dd></div>
              <div className="flex justify-between gap-4 border-b border-gray-100 pb-3"><dt className="text-gray-500">Latence moyenne</dt><dd className="font-semibold text-gray-900">≥ 2 000 ms</dd></div>
              <div className="flex justify-between gap-4"><dt className="text-gray-500">Incertitude</dt><dd className="font-semibold text-gray-900">≥ 20 %</dd></div>
            </dl>
            <p className="mt-5 text-xs text-gray-500">
              {lastUpdated ? `Dernière mise à jour : ${lastUpdated.toLocaleTimeString('fr-FR')}` : 'Pas encore de mise à jour.'}
            </p>
          </aside>
        </div>
      </section>
    </main>
  )
}