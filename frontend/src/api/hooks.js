import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import api from './client'

export function useSales() {
  return useQuery({
    queryKey: ['sales'],
    queryFn: () => api.get('/sales').then((r) => r.data),
  })
}

export function useSale(saleId) {
  return useQuery({
    queryKey: ['sales', saleId],
    queryFn: () => api.get(`/sales/${saleId}`).then((r) => r.data),
    enabled: !!saleId,
  })
}

export function useCreateSale() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload) => api.post('/sales', payload).then((r) => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['sales'] }),
  })
}

export function useUpdateSale() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, ...payload }) => api.put(`/sales/${id}`, payload).then((r) => r.data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['sales'] })
      qc.invalidateQueries({ queryKey: ['stats'] })
    },
  })
}

export function useDeleteSale() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id) => api.delete(`/sales/${id}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['sales'] })
      qc.invalidateQueries({ queryKey: ['stats'] })
    },
  })
}

export function useAgencies() {
  return useQuery({
    queryKey: ['agencies'],
    queryFn: () => api.get('/agencies').then((r) => r.data),
  })
}

export function useAgency(agencyId) {
  return useQuery({
    queryKey: ['agencies', agencyId],
    queryFn: () => api.get(`/agencies/${agencyId}`).then((r) => r.data),
    enabled: !!agencyId,
  })
}

export function useCreateAgency() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload) => api.post('/agencies', payload).then((r) => r.data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['agencies'] })
      qc.invalidateQueries({ queryKey: ['stats'] })
    },
  })
}

export function useUpdateAgency() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, ...payload }) => api.put(`/agencies/${id}`, payload).then((r) => r.data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['agencies'] })
      qc.invalidateQueries({ queryKey: ['stats'] })
    },
  })
}

export function useDeleteAgency() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id) => api.delete(`/agencies/${id}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['agencies'] })
      qc.invalidateQueries({ queryKey: ['stats'] })
    },
  })
}

export function useTrackRecords() {
  return useQuery({
    queryKey: ['track-records'],
    queryFn: () => api.get('/track-records').then((r) => r.data),
  })
}

export function useCreateTrackRecord() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (payload) => api.post('/track-records', payload).then((r) => r.data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['track-records'] })
      qc.invalidateQueries({ queryKey: ['stats'] })
    },
  })
}

export function useUpdateTrackRecord() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, ...payload }) => api.put(`/track-records/${id}`, payload).then((r) => r.data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['track-records'] })
      qc.invalidateQueries({ queryKey: ['stats'] })
    },
  })
}

export function useDeleteTrackRecord() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id) => api.delete(`/track-records/${id}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['track-records'] })
      qc.invalidateQueries({ queryKey: ['stats'] })
    },
  })
}

export function useStats() {
  return useQuery({
    queryKey: ['stats'],
    queryFn: () => api.get('/stats').then((r) => r.data),
  })
}
