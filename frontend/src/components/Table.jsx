import clsx from 'clsx'

export default function Table({
  columns,
  data,
  loading = false,
  onRowClick,
  className,
}) {
  if (loading) {
    return (
      <div className="w-full p-8 text-center">
        <p className="text-gray-500">Loading...</p>
      </div>
    )
  }

  if (!data || data.length === 0) {
    return (
      <div className="w-full p-8 text-center">
        <p className="text-gray-500">No data found</p>
      </div>
    )
  }

  return (
    <div className={clsx('w-full overflow-x-auto', className)}>
      <table className="w-full border-collapse">
        <thead>
          <tr className="bg-gray-50 border-b border-gray-200">
            {columns.map((col) => (
              <th
                key={col.key}
                className="px-4 py-3 text-left text-sm font-semibold text-gray-700"
              >
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, idx) => (
            <tr
              key={row.id}
              onClick={() => onRowClick?.(row)}
              className={clsx(
                'border-b border-gray-200 hover:bg-gray-50 transition-colors',
                onRowClick && 'cursor-pointer'
              )}
            >
              {columns.map((col) => (
                <td key={col.key} className="px-4 py-3 text-sm text-gray-900">
                  {col.render ? col.render(row[col.key], row) : row[col.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}