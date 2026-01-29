import type { Lead } from "~src/types/leads"

const SEGMENT_COLORS: Record<string, string> = {
  academic: "bg-purple-100 text-purple-700",
  technical: "bg-blue-100 text-blue-700",
  enterprise: "bg-amber-100 text-amber-700",
  influencer: "bg-pink-100 text-pink-700",
}

const STATUS_ICONS: Record<string, { icon: string; color: string }> = {
  pending: { icon: "\u25CB", color: "text-gray-400" },      // ○
  in_progress: { icon: "\u25D4", color: "text-atlas-500" }, // ◔
  completed: { icon: "\u2713", color: "text-green-600" },   // ✓
  failed: { icon: "\u2717", color: "text-red-500" },        // ✗
  skipped: { icon: "\u2013", color: "text-gray-400" },      // –
}

interface LeadRowProps {
  lead: Lead
  isCurrent: boolean
}

export function LeadRow({ lead, isCurrent }: LeadRowProps) {
  const status = STATUS_ICONS[lead.status] || STATUS_ICONS.pending
  const segmentColor = SEGMENT_COLORS[lead.segment] || "bg-gray-100 text-gray-600"

  return (
    <div
      className={`flex items-center gap-2 px-3 py-1.5 text-xs ${
        isCurrent ? "bg-atlas-50 border-l-2 border-atlas-500" : "border-l-2 border-transparent"
      }`}
    >
      <span className={`text-sm font-mono ${status.color}`}>{status.icon}</span>
      <span className="flex-1 truncate text-gray-800">{lead.name}</span>
      <span className={`px-1.5 py-0.5 rounded text-[10px] font-medium ${segmentColor}`}>
        {lead.segment}
      </span>
    </div>
  )
}
