import { useCallback, useEffect, useState } from 'react'
import { getAdminLaptopById } from '../services/adminLaptopService'

function useAdminLaptopDetail(laptopId) {
  const [laptop, setLaptop] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const refetch = useCallback(async () => {
    setLoading(true)
    setError('')

    try {
      const data = await getAdminLaptopById(laptopId)
      setLaptop(data)
    } catch (requestError) {
      setLaptop(null)
      setError(requestError?.message || 'Gagal memuat detail laptop admin.')
    } finally {
      setLoading(false)
    }
  }, [laptopId])

  useEffect(() => {
    let isMounted = true

    async function fetchDetail() {
      setLoading(true)
      setError('')

      try {
        const data = await getAdminLaptopById(laptopId)

        if (isMounted) {
          setLaptop(data)
        }
      } catch (requestError) {
        if (isMounted) {
          setLaptop(null)
          setError(requestError?.message || 'Gagal memuat detail laptop admin.')
        }
      } finally {
        if (isMounted) {
          setLoading(false)
        }
      }
    }

    fetchDetail()

    return () => {
      isMounted = false
    }
  }, [laptopId])

  return {
    error,
    laptop,
    loading,
    refetch,
  }
}

export default useAdminLaptopDetail

