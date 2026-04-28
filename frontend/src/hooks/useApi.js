import { useState, useEffect } from 'react'
import axios from 'axios'

const BASE = '/api'

export function useGet(endpoint) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    axios.get(`${BASE}${endpoint}`)
      .then(r => setData(r.data))
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [endpoint])

  return { data, loading, error, refetch: () => {} }
}

export async function post(endpoint, body) {
  const r = await axios.post(`${BASE}${endpoint}`, body)
  return r.data
}

export async function del(endpoint) {
  const r = await axios.delete(`${BASE}${endpoint}`)
  return r.data
}