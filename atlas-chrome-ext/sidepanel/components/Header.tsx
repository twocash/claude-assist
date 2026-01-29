import { useState } from "react"

interface HeaderProps {
  connected: boolean
}

export function Header({ connected }: HeaderProps) {
  const [isSyncing, setIsSyncing] = useState(false)

  const handleGlobalSync = async () => {
    setIsSyncing(true)
    try {
      const response = await chrome.runtime.sendMessage({ name: "RUN_FULL_SYNC" })
      console.log("Global sync result:", response)
    } catch (e) {
      console.error("Sync failed:", e)
    } finally {
      // Show spinner for at least 1 second for feedback
      setTimeout(() => setIsSyncing(false), 1000)
    }
  }

  return (
    <div className="flex items-center gap-2 px-4 py-3 border-b border-gray-200 bg-white">
      <div className="w-7 h-7 rounded-lg bg-atlas-600 flex items-center justify-center flex-shrink-0">
        <span className="text-white font-bold text-xs">A</span>
      </div>
      <div className="flex-1 min-w-0">
        <h1 className="text-sm font-semibold text-gray-900 leading-tight">Atlas</h1>
        <p className="text-[10px] text-gray-400 leading-tight">Sales Nav Assistant</p>
      </div>
      <div className="flex items-center gap-3">
        {/* GLOBAL SYNC BUTTON (Always Visible) */}
        <button
          onClick={handleGlobalSync}
          disabled={isSyncing}
          className={`p-1.5 rounded-md hover:bg-gray-100 text-gray-400 hover:text-gray-600 transition-all ${isSyncing ? 'animate-spin text-blue-500' : ''}`}
          title="Sync All (Notion + Phantoms)"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>

        {/* Status Badge */}
        <div className="flex items-center gap-1.5">
          <div
            className={`w-2 h-2 rounded-full ${connected ? "bg-green-500" : "bg-gray-300"}`}
          />
          <span className="text-[10px] text-gray-400">
            {connected ? "Ready" : "Idle"}
          </span>
        </div>
      </div>
    </div>
  )
}
