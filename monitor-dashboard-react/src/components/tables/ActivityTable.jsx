export default function ActivityTable({ items }) {
  return (
    <div className="table-wrap">
      <table className="table">
        <thead><tr><th>Time (UTC)</th><th>User</th><th>Event</th><th>Conf.</th></tr></thead>
        <tbody>
          {items.map((it, i) => (
            <tr key={it._id || `${it.ts}-${i}`}>
              <td>{new Date(it.ts).toISOString()}</td>
              <td>{it.user}</td>
              <td>{it.event}</td>
              <td>{it.confidence ?? ''}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
