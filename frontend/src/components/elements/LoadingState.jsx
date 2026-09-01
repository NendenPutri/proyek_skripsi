function LoadingState({ message = 'Memuat data...' }) {
  return (
    <div className="state-card" role="status">
      <div className="skeleton mx-auto h-10 w-10 rounded-full" />
      <p className="mt-4 text-sm font-medium text-slate-600">{message}</p>
    </div>
  )
}

export default LoadingState
