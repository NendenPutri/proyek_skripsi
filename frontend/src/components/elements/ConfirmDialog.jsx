import * as AlertDialog from '@radix-ui/react-alert-dialog'
import Button from './Button'

function ConfirmDialog({
  title,
  description,
  confirmLabel = 'Konfirmasi',
  cancelLabel = 'Batal',
  loading = false,
  onCancel,
  onConfirm,
}) {
  function handleOpenChange(nextOpen) {
    if (!nextOpen && !loading) {
      onCancel?.()
    }
  }

  return (
    <AlertDialog.Root onOpenChange={handleOpenChange} open>
      <AlertDialog.Portal>
        <AlertDialog.Overlay className="dialog-backdrop" />
        <AlertDialog.Content className="confirm-dialog">
          <AlertDialog.Title>{title}</AlertDialog.Title>
          <AlertDialog.Description>{description}</AlertDialog.Description>
          <div className="confirm-dialog-actions">
            <AlertDialog.Cancel asChild>
              <Button disabled={loading} onClick={onCancel} variant="ghost">
                {cancelLabel}
              </Button>
            </AlertDialog.Cancel>
            <Button disabled={loading} onClick={onConfirm} variant="primary">
              {loading ? 'Memproses...' : confirmLabel}
            </Button>
          </div>
        </AlertDialog.Content>
      </AlertDialog.Portal>
    </AlertDialog.Root>
  )
}

export default ConfirmDialog
