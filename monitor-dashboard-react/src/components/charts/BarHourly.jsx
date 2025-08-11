import {
    BarElement,
    CategoryScale,
    Chart as ChartJS,
    Legend,
    LinearScale,
    Tooltip
} from 'chart.js'
import { Bar } from 'react-chartjs-2'
ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend)

export default function BarHourly({ bucket }) {
  const labels = Object.keys(bucket).sort().slice(-12)
  const data = {
    labels,
    datasets: [
      {
        label: 'Prasanna',
        data: labels.map(l => bucket[l]?.prasanna ?? 0),
        backgroundColor: 'rgba(122,223,255,.4)',
        borderColor: '#7ADFFF',
        borderWidth: 1,
        borderRadius: 6
      },
      {
        label: 'Random',
        data: labels.map(l => bucket[l]?.random ?? 0),
        backgroundColor: 'rgba(255,151,173,.4)',
        borderColor: '#FF97AD',
        borderWidth: 1,
        borderRadius: 6
      }
    ]
  }
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { position: 'bottom' } },
    scales: {
      x: { stacked: true, grid: { color: 'rgba(255,255,255,0.06)' } },
      y: { stacked: true, beginAtZero: true, grid: { color: 'rgba(255,255,255,0.06)' } }
    }
  }
  return (
    <div style={{ height: 280 }}>
      <Bar data={data} options={options} />
    </div>
  )
}
