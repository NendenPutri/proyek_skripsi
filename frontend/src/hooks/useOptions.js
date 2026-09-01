import { useCallback, useEffect, useState } from 'react'
import { getOptions } from '../services/optionsService'

function getErrorMessage(error) {
  return error?.message
    ? `Gagal memuat pilihan form: ${error.message}`
    : 'Gagal memuat pilihan form. Pastikan layanan aplikasi sedang aktif.'
}

function useOptions() {
  const [options, setOptions] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const refetch = useCallback(async () => {
    setLoading(true)
    setError('')

    try {
      const response = await getOptions()
      setOptions(response?.data ?? response ?? null)
    } catch (requestError) {
      setOptions(null)
      setError(getErrorMessage(requestError))
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    let isMounted = true

    async function fetchInitialOptions() {
      try {
        const response = await getOptions()

        if (isMounted) {
          setOptions(response?.data ?? response ?? null)
          setError('')
        }
      } catch (requestError) {
        if (isMounted) {
          setOptions(null)
          setError(getErrorMessage(requestError))
        }
      } finally {
        if (isMounted) {
          setLoading(false)
        }
      }
    }

    fetchInitialOptions()

    return () => {
      isMounted = false
    }
  }, [])

  return {
    options,
    loading,
    error,
    refetch,
  }
}

export default useOptions
