import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import candidatesAPI from '../services/candidates'
import Button from '../components/Button'
import Badge from '../components/Badge'

export default function CandidateDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()

  const { data: candidate, isLoading, error } = useQuery({
    queryKey: ['candidate', id],
    queryFn: () => candidatesAPI.get(id).then((res) => res.data),
  })

  if (isLoading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>
  }

  if (error || !candidate) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-red-600">Error loading candidate</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-6 flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{candidate.full_name}</h1>
            <p className="text-gray-600 mt-1">{candidate.candidate_id}</p>
          </div>
          <div className="flex gap-2">
            <Button variant="secondary" onClick={() => navigate(`/candidates/${id}/edit`)}>
              Edit
            </Button>
            <Button variant="ghost" onClick={() => navigate('/candidates')}>
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
            <Badge className="mt-2">{candidate.current_status}</Badge>
          </div>
          <div className="bg-white rounded-lg shadow-md p-4">
            <p className="text-sm text-gray-600">Age</p>
            <p className="text-2xl font-bold text-gray-900 mt-1">{candidate.age}</p>
          </div>
          <div className="bg-white rounded-lg shadow-md p-4">
            <p className="text-sm text-gray-600">Nationality</p>
            <p className="text-lg font-semibold text-gray-900 mt-1">{candidate.nationality}</p>
          </div>
          <div className="bg-white rounded-lg shadow-md p-4">
            <p className="text-sm text-gray-600">Passport</p>
            <p className="text-lg font-semibold text-gray-900 mt-1">
              {candidate.passport_validity_days >= 0 ? (
                <Badge variant="success">{candidate.passport_validity_days} days</Badge>
              ) : (
                <Badge variant="danger">Expired</Badge>
              )}
            </p>
          </div>
        </div>

        {/* Sections */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Personal Information */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-bold text-gray-900 mb-4">Personal Information</h2>
            <div className="space-y-4">
              <div>
                <p className="text-sm text-gray-600">Full Name</p>
                <p className="text-gray-900 font-semibold">{candidate.full_name}</p>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-600">Surname</p>
                  <p className="text-gray-900">{candidate.surname}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Given Name</p>
                  <p className="text-gray-900">{candidate.given_name}</p>
                </div>
              </div>
              <div>
                <p className="text-sm text-gray-600">Date of Birth</p>
                <p className="text-gray-900">{candidate.date_of_birth}</p>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-600">Gender</p>
                  <p className="text-gray-900">{candidate.gender}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Nationality</p>
                  <p className="text-gray-900">{candidate.nationality}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Contact Information */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-bold text-gray-900 mb-4">Contact Information</h2>
            <div className="space-y-4">
              <div>
                <p className="text-sm text-gray-600">Mobile</p>
                <p className="text-gray-900 font-semibold">{candidate.mobile}</p>
              </div>
              {candidate.alternative_mobile && (
                <div>
                  <p className="text-sm text-gray-600">Alternative Mobile</p>
                  <p className="text-gray-900">{candidate.alternative_mobile}</p>
                </div>
              )}
              {candidate.email && (
                <div>
                  <p className="text-sm text-gray-600">Email</p>
                  <p className="text-gray-900">{candidate.email}</p>
                </div>
              )}
              {candidate.address && (
                <div>
                  <p className="text-sm text-gray-600">Address</p>
                  <p className="text-gray-900">{candidate.address}</p>
                </div>
              )}
            </div>
          </div>

          {/* Passport Information */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-bold text-gray-900 mb-4">Passport Information</h2>
            <div className="space-y-4">
              <div>
                <p className="text-sm text-gray-600">Passport Number</p>
                <p className="text-gray-900 font-semibold">{candidate.passport_number}</p>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-600">Issue Date</p>
                  <p className="text-gray-900">{candidate.passport_issue_date}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Expiry Date</p>
                  <p className="text-gray-900">{candidate.passport_expiry_date}</p>
                </div>
              </div>
              <div>
                <p className="text-sm text-gray-600">Issuing Country</p>
                <p className="text-gray-900">{candidate.passport_issuing_country}</p>
              </div>
            </div>
          </div>

          {/* Qualifications */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-bold text-gray-900 mb-4">Qualifications</h2>
            <div className="space-y-4">
              {candidate.education && (
                <div>
                  <p className="text-sm text-gray-600">Education</p>
                  <p className="text-gray-900">{candidate.education}</p>
                </div>
              )}
              {candidate.experience && (
                <div>
                  <p className="text-sm text-gray-600">Experience</p>
                  <p className="text-gray-900">{candidate.experience}</p>
                </div>
              )}
              {candidate.skills && (
                <div>
                  <p className="text-sm text-gray-600">Skills</p>
                  <p className="text-gray-900">{candidate.skills}</p>
                </div>
              )}
              {candidate.languages && (
                <div>
                  <p className="text-sm text-gray-600">Languages</p>
                  <p className="text-gray-900">{candidate.languages}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}