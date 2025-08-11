import { ArcElement, Chart as ChartJS, Legend, Tooltip } from 'chart.js'
import { Doughnut } from 'react-chartjs-2'
ChartJS.register(ArcElement, Tooltip, Legend)

export default function DonutEvents({ counts }) {
  const data = {
    labels: ['Prasanna', 'Random', 'Screen Off'],
    datasets: [{
      data: [counts.prasanna || 0, counts.random || 0, counts.screenOff || 0],
      backgroundColor: ['#7ADFFF', '#FF97AD', '#F9E27D'],
      borderColor: '#1e2a52',
      borderWidth: 2
    }]
  }
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { position: 'bottom' } },
    cutout: '65%'
  }
  return (
    <div style={{ height: 300 }}>
      <Doughnut data={data} options={options} />
    </div>
  )
}
