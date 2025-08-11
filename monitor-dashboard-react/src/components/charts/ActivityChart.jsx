import {
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Title, Tooltip
} from 'chart.js'
import { Line } from 'react-chartjs-2'
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

const COLORS = {
  prasanna: '#7ADFFF',   // cyan
  random:   '#FF97AD'    // pink
}

export default function ActivityChart({ bucket }) {
  const labels = Object.keys(bucket).sort()
  const data = {
    labels,
    datasets: [
      {
        label: 'Prasanna',
        data: labels.map(l => bucket[l]?.prasanna ?? 0),
        borderColor: COLORS.prasanna,
        backgroundColor: 'rgba(122,223,255,.2)',
        pointRadius: 2,
        tension: 0.35
      },
      {
        label: 'Random',
        data: labels.map(l => bucket[l]?.random ?? 0),
        borderColor: COLORS.random,
        backgroundColor: 'rgba(255,151,173,.2)',
        pointRadius: 2,
        tension: 0.35
      }
    ]
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,            // allow fixed height
    plugins: { legend: { position: 'bottom' } },
    scales: {
      x: { grid: { color: 'rgba(255,255,255,0.06)' } },
      y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.06)' } }
    }
  }

  return (
    <div style={{ height: 280 }}>
      <Line data={data} options={options} />
    </div>
  )
}
