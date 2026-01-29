/**
 * MissionReport - Post-processing summary
 * Shows results + "Close the Loop" action to update Notion
 */

import { useState } from "react"
import type { TaskQueueState } from "~src/types/leads"
import { RunSummary } from "./RunSummary"
import { ExportResults } from "./ExportResults"

interface MissionReportProps {
  queue: TaskQueueState
  onClose: () => void
}

export function MissionReport({ queue, onClose }: MissionReportProps) {
  const [isSyncing, setIsSyncing] = useState(false)
  const [synced, setSynced] = useState(false)

  const succeeded = queue.leads.filter((l) => l.status === "completed")
  const failed = queue.leads.filter((l) => l.status === "failed")

  const handleSyncToNotion = async () => {
    setIsSyncing(true)

    try {
      // Update Notion: mark all succeeded contacts as "Following"
      const response = await chrome.runtime.sendMessage({
        name: "UPDATE_PROCESSED_CONTACTS",
        body: {
          contactPageIds: succeeded
            .map((l) => l.notionPageId)
            .filter(Boolean),
        },
      })

      if (response?.ok) {
        setSynced(true)
      }
    } catch (e) {
      console.error("Failed to sync to Notion:", e)
    } finally {
      setIsSyncing(false)
    }
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="px-4 py-4 bg-gradient-to-r from-green-50 to-blue-50 border-b border-gray-200">
        <div className="text-center">
          <div className="text-4xl mb-2">
            {failed.length === 0 ? "🎉" : succeeded.length > failed.length ? "✅" : "⚠️"}
          </div>
          <h2 className="text-lg font-bold text-gray-900 mb-1">Session Complete</h2>
          <div className="text-sm text-gray-600">
            {succeeded.length}/{queue.leads.length} Successful
          </div>
        </div>
      </div>

      {/* Stats summary */}
      <div className="px-4 py-4">
        <RunSummary queue={queue} />
      </div>

      {/* Actions */}
      <div className="px-4 py-4 border-t border-gray-200 bg-gray-50 space-y-3">
        {!synced ? (
          <button
            onClick={handleSyncToNotion}
            disabled={isSyncing || succeeded.length === 0}
            className="w-full bg-green-600 text-white py-3 rounded-lg font-bold shadow-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSyncing ? "Syncing to Notion..." : `Update ${succeeded.length} Contacts in Notion`}
          </button>
        ) : (
          <div className="text-center py-3 text-sm text-green-700 bg-green-100 rounded-lg font-medium">
            ✓ Notion updated successfully
          </div>
        )}

        <ExportResults queue={queue} />

        <button
          onClick={onClose}
          className="w-full bg-white border border-gray-300 text-gray-700 py-2 rounded-lg hover:bg-gray-50"
        >
          Return to Segments
        </button>
      </div>

      {/* Failed contacts (if any) */}
      {failed.length > 0 && (
        <div className="px-4 pb-4">
          <details className="bg-red-50 border border-red-200 rounded-lg">
            <summary className="px-3 py-2 cursor-pointer text-xs font-medium text-red-800">
              {failed.length} Failed Contacts
            </summary>
            <div className="px-3 pb-2 space-y-1">
              {failed.map((lead) => (
                <div key={lead.id} className="text-xs text-gray-700">
                  • {lead.name}
                  {lead.result?.error && (
                    <span className="text-red-600 ml-2">({lead.result.error})</span>
                  )}
                </div>
              ))}
            </div>
          </details>
        </div>
      )}
    </div>
  )
}
