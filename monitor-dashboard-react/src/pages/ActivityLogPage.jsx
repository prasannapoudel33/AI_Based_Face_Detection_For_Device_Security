import { useEffect, useState } from 'react'
import { getActivity } from '../api'
import ActivityTable from '../components/tables/ActivityTable'

export default function ActivityLogPage({ token }) {
  const [items, setItems] = useState([])
  useEffect(() => { (async () => { const { items } = await getActivity(token, 500); setItems(items) })() }, [token])
  return <section className="card"><h2>Activity Log</h2><ActivityTable items={items} /></section>
}
