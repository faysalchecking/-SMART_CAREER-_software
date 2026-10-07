import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import jobsAPI from '../services/jobs'
import Button from '../components/Button'
import Badge from '../components/Badge'

export default function JobDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()

  const { data: job, isLoading, error } = useQuery({
    queryKey: ['job', id],
    queryFn: () => jobsAPI.get(id).then((res) => res.data),
  })

  if (isLoading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>
  }

  if (error || !job) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-red-600">Error loading job</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-6 flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{job.title}</h1>
            <p className="text-gray-600 mt-1">{job.employer.company_name}</p>
            <p className="text-gray-600 text-sm">{job.job_id}</p>
          </div>
          <div className="flex gap-2">
            <Button variant="secondary" onClick={() => navigate(`/jobs/${id}/edit`)}>
              Edit
            </Button>
            <Button variant="ghost" onClick={() => navigate('/jobs')}>
              Back
            </Button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Quick Info */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-lg shadow-md p-4">
            <p className="text-sm text-gray-600">Status</p>
            <Badge className="mt-2">{job.status}</Badge>
          </div>
          <div className="bg-white rounded-lg shadow-md p-4">
            <p className="text-sm text-gray-600">Available Positions</p>
            <p className="text-2xl font-bold text-gray-900 mt-1">
              {job.available_positions}/{job.quantity}
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-md p-4">
            <p className="text-sm text-gray-600">Salary</p>
            <p className="text-lg font-semibold text-gray-900 mt-1">
              {job.currency} {job.salary_max || 'TBD'}
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-md p-4">
            <p className="text-sm text-gray-600">Deadline</p>
            <p className="text-lg font-semibold text-gray-900 mt-1">
              {new Date(job.application_deadline).toLocaleDateString()}
            </p>
          </div>
        </div>

        {/* Sections */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Job Details */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-bold text-gray-900 mb-4">Job Details</h2>
            <div className="space-y-4">
              <div>
                <p className="text-sm text-gray-600">Location</p>
                <p className="text-gray-900 font-semibold">
                  {job.city}, {job.country}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Description</p>
                <p className="text-gray-900 whitespace-pre-wrap">{job.description || '-'}</p>
              </div>
              {job.visa_type && (
                <div>
                  <p className="text-sm text-gray-600">Visa Type</p>
                  <p className="text-gray-900">{job.visa_type}</p>
                </div>
              )}
            </div>
          </div>

          {/* Requirements */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-bold text-gray-900 mb-4">Requirements</h2>
            <div className="space-y-4">
              {job.age_min && (
                <div>
                  <p className="text-sm text-gray-600">Age</p>
                  <p className="text-gray-900">
                    {job.age_min} - {job.age_max || 'Any'} years
                  </p>
                </div>
              )}
              {job.gender !== 'ANY' && (
                <div>
                  <p className="text-sm text-gray-600">Gender</p>
                  <p className="text-gray-900">{job.gender}</p>
                </div>
              )}
              {job.education && (
                <div>
                  <p className="text-sm text-gray-600">Education</p>
                  <p className="text-gray-900">{job.education}</p>
                </div>
              )}
              {job.experience_years && (
                <div>
                  <p className="text-sm text-gray-600">Experience</p>
                  <p className="text-gray-900">{job.experience_years}+ years</p>
                </div>
              )}
              {job.languages && (
                <div>
                  <p className="text-sm text-gray-600">Languages</p>
                  <p className="text-gray-900">{job.languages}</p>
                </div>
              )}
            </div>
          </div>

          {/* Benefits */}
          {(job.accommodation || job.food || job.transportation) && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-lg font-bold text-gray-900 mb-4">Benefits</h2>
              <div className="space-y-4">
                {job.accommodation && (
                  <div>
                    <p className="text-sm text-gray-600">Accommodation</p>
                    <p className="text-gray-900">{job.accommodation}</p>
                  </div>
                )}
                {job.food && (
                  <div>
                    <p className="text-sm text-gray-600">Food</p>
                    <p className="text-gray-900">{job.food}</p>
                  </div>
                )}
                {job.transportation && (
                  <div>
                    <p className="text-sm text-gray-600">Transportation</p>
                    <p className="text-gray-900">{job.transportation}</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Working Conditions */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-bold text-gray-900 mb-4">Working Conditions</h2>
            <div className="space-y-4">
              {job.working_hours && (
                <div>
                  <p className="text-sm text-gray-600">Working Hours</p>
                  <p className="text-gray-900">{job.working_hours}</p>
                </div>
              )}
              <div>
                <p className="text-sm text-gray-600">Overtime</p>
                <p className="text-gray-900">
                  {job.overtime_allowed ? 'Allowed' : 'Not Allowed'}
                </p>
              </div>
              {job.contract_period_months && (
                <div>
                  <p className="text-sm text-gray-600">Contract Period</p>
                  <p className="text-gray-900">{job.contract_period_months} months</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}