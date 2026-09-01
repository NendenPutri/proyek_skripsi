function Notification({ message, type = 'success', onClose }) {
  if (!message) {
    return null
  }

  return (
    <div className={`notification notification-${type}`} role="status">
      <p>{message}</p>
      {onClose ? (
        <button aria-label="Tutup notifikasi" onClick={onClose} type="button">
          Tutup
        </button>
      ) : null}
    </div>
  )
}

export default Notification

