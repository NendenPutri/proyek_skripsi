import { useCallback, useEffect, useState } from 'react'
import { getAdminLaptops } from '../services/adminLaptopService'

function useAdminLaptops(params) {
  const [items, setItems] = useState([])
  const [pagination, setPagination] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const fetchLaptops = useCallback(async () => {
    setLoading(true)
    setError('')

    try {
      const data = await getAdminLaptops(params)
      setItems(data?.items || [])
      setPagination(data?.pagination || null)
    } catch (requestError) {
      setItems([])
      setPagination(null)
      setError(requestError?.message || 'Gagal memuat data laptop admin.')
    } finally {
      setLoading(false)
    }
  }, [params])

  useEffect(() => {
    let isMounted = true

    async function fetchInitialData() {
      setLoading(true)
      setError('')

      try {
        const data = await getAdminLaptops(params)

        if (isMounted) {
          setItems(data?.items || [])
          setPagination(data?.pagination || null)
        }
      } catch (requestError) {
        if (isMounted) {
          setItems([])
          setPagination(null)
          setError(requestError?.message || 'Gagal memuat data laptop admin.')
        }
      } finally {
        if (isMounted) {
          setLoading(false)
        }
      }
    }

    fetchInitialData()

    return () => {
      isMounted = false
    }
  }, [params])

  return {
    error,
    items,
    loading,
    pagination,
    refetch: fetchLaptops,
  }
}

export default useAdminLaptops

