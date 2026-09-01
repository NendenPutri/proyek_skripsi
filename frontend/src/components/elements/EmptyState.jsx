function EmptyState({ title, description, action }) {
  return (
    <div className="state-card">
      <p className="text-lg font-semibold text-slate-950">{title || 'Data tidak tersedia'}</p>
      {description ? <p className="mx-auto mt-2 max-w-xl text-slate-600">{description}</p> : null}
      {action ? <div className="mt-5">{action}</div> : null}
    </div>
  )
}

export default EmptyState
