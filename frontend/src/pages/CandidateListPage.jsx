import { useState, useMemo } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import candidatesAPI from '../services/candidates'
import Button from '../components/Button'
import Input from '../components/Input'
import Table from '../components/Table'
import Badge from '../components/Badge'

export default function CandidateListPage() {
  const navigate = useNavigate()
  const [search, setSearch] = useState('')
  const [status, setStatus] = useState('')
  const [page, setPage] = useState(1)

  // Fetch candidates
  const { data, isLoading, error } = useQuery({
    queryKey: ['candidates', { search, status, page }],
    queryFn: async () => {
      const response = await candidatesAPI.list({
        search,
        current_status: status,
        page,
      })
      return response.data
    },
  })

  const candidates = data?.results || []
  const totalPages = data?.count ? Math.ceil(data.count / 20) : 1

  const columns = [
    { key: 'candidate_id', label: 'ID' },
    { key: 'full_name', label: 'Name' },
    { key: 'mobile', label: 'Mobile' },
    {
      key: 'passport_number',
      label: 'Passport',
      render: (val) => val || '-',
    },
    {
      key: 'age',
      label: 'Age',
      render: (val) => val || '-',
    },
    {
      key: 'current_status',
      label: 'Status',
      render: (val) => <Badge variant="default">{val}</Badge>,
    },
    {
      key: 'passport_validity_days',
      label: 'Passport',
      render: (val, row) => {
        if (row.is_passport_expired) {
          return <Badge variant="danger">Expired</Badge>
        }
        if (val >= 0 && val <= 90) {
          return <Badge variant="warning">{val} days</Badge>
        }
        return <Badge variant="success">{val} days</Badge>
      },
    },
  ]

  const handleSearch = (value) => {
    setSearch(value)
    setPage(1)
  }

  const handleStatusChange = (value) => {
    setStatus(value)
    setPage(1)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">Candidates</h1>
            <Button onClick={() => navigate('/candidates/new')}>
              + New Candidate
            </Button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Filters */}
        <div className="bg-white rounded-lg shadow-md p-4 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Input
              label="Search"
              placeholder="Name, mobile, passport..."
              value={search}
              onChange={(e) => handleSearch(e.target.value)}
            />
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Status
              </label>
              <select
                value={status}
                onChange={(e) => handleStatusChange(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Statuses</option>
                <option value="AVAILABLE">Available</option>
                <option value="APPLIED">Applied</option>
                <option value="SHORTLISTED">Shortlisted</option>
                <option value="SELECTED">Selected</option>
                <option value="PROCESSING">Processing</option>
                <option value="DEPLOYED">Deployed</option>
              </select>
            </div>
          </div>
        </div>

        {/* Table */}
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <Table
            columns={columns}
            data={candidates}
            loading={isLoading}
            onRowClick={(row) => navigate(`/candidates/${row.id}`)}
          />
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="mt-6 flex justify-center gap-2">
            <Button
              variant="secondary"
              disabled={page === 1}
              onClick={() => setPage(page - 1)}
            >
              Previous
            </Button>
            <span className="px-4 py-2 text-gray-700">
              Page {page} of {totalPages}
            </span>
            <Button
              variant="secondary"
              disabled={page === totalPages}
              onClick={() => setPage(page + 1)}
            >
              Next
            </Button>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-700">Error loading candidates. Please try again.</p>
          </div>
        )}
      </div>
    </div>
  )
}