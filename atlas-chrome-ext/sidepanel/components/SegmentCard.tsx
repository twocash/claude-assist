/**
 * SegmentCard - "Job Card" for segment selection
 */

interface SegmentCardProps {
  segment: {
    id: string
    name: string
    icon: string
    salesNavStatus: string
    listName: string
  }
  pendingCount: number
  onClick: () => void
}

export function SegmentCard({ segment, pendingCount, onClick }: SegmentCardProps) {
  const priorityColor = pendingCount > 10 ? 'text-red-600' : pendingCount > 5 ? 'text-amber-600' : 'text-gray-600'

  return (
    <button
      onClick={onClick}
      disabled={pendingCount === 0}
      className="w-full p-4 bg-white border-2 border-gray-200 rounded-xl hover:border-blue-400 hover:shadow-md transition-all text-left disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:border-gray-200 disabled:hover:shadow-none"
    >
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <span className="text-2xl">{segment.icon}</span>
          <span className="font-bold text-gray-900">{segment.name}</span>
        </div>
        {pendingCount > 0 && (
          <span className={`text-sm font-bold ${priorityColor}`}>
            {pendingCount} pending
          </span>
        )}
      </div>

      <div className="text-xs text-gray-500">
        → {segment.listName} list
      </div>

      {pendingCount === 0 && (
        <div className="mt-2 text-xs text-gray-400 italic">
          All contacts processed ✓
        </div>
      )}
    </button>
  )
}
