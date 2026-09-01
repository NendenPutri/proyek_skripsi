import Button from './Button'

function ErrorState({ message, onRetry }) {
  return (
    <div className="state-card-error">
      <p className="text-sm font-semibold text-red-700">Terjadi kesalahan</p>
      <p className="mt-2 text-slate-700">{message || 'Request gagal diproses.'}</p>
      {onRetry ? (
        <Button className="mt-5" onClick={onRetry} variant="secondary">
          Coba lagi
        </Button>
      ) : null}
    </div>
  )
}

export default ErrorState
