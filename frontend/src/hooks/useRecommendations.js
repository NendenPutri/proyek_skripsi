import { useState } from 'react'
import { getRecommendations } from '../services/recommendationService'

function getErrorMessage(error) {
  return error?.message
    ? `Gagal mengambil rekomendasi: ${error.message}`
    : 'Gagal mengambil rekomendasi. Silakan coba lagi.'
}

function useRecommendations() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [lastPayload, setLastPayload] = useState(null)

  async function submitRecommendation(payload) {
    setLoading(true)
    setError('')
    setLastPayload(payload)

    try {
      const response = await getRecommendations(payload)
      setResult(response)
      return response
    } catch (requestError) {
      const message = getErrorMessage(requestError)
      setResult(null)
      setError(message)
      return null
    } finally {
      setLoading(false)
    }
  }

  function resetResult() {
    setResult(null)
    setError('')
    setLoading(false)
    setLastPayload(null)
  }

  return {
    result,
    loading,
    error,
    lastPayload,
    submitRecommendation,
    resetResult,
  }
}

export default useRecommendations
