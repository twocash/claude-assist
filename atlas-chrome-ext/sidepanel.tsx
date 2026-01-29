import React, { Component, useEffect, useState, useRef } from "react"
import "./style.css"
import { useQueueState } from "~src/lib/hooks"
import { HEARTBEAT_INTERVAL } from "~src/lib/constants"
import { Header } from "~sidepanel/components/Header"
import { CsvImport } from "~sidepanel/components/CsvImport"
import { TaskQueue } from "~sidepanel/components/TaskQueue"
import { ProgressBar } from "~sidepanel/components/ProgressBar"
import { Controls } from "~sidepanel/components/Controls"
import { ModelSelector } from "~sidepanel/components/ModelSelector"
import { ApiKeySetup } from "~sidepanel/components/ApiKeySetup"
import { RunSummary } from "~sidepanel/components/RunSummary"
import { ExportResults } from "~sidepanel/components/ExportResults"
import { DebugLogViewer } from "~sidepanel/components/DebugLogViewer"
import { PostsTab } from "~sidepanel/components/PostsTab"
import { AdHocReply } from "~sidepanel/components/AdHocReply"
import { EnrichmentImport } from "~sidepanel/components/EnrichmentImport"

// --- Error Boundary ---

interface ErrorBoundaryState {
  hasError: boolean
  error: string
}

class ErrorBoundary extends Component<{ children: React.ReactNode }, ErrorBoundaryState> {
  state: ErrorBoundaryState = { hasError: false, error: "" }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error: error.message }
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error("Atlas UI crash:", error, info.componentStack)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
          <div className="text-center space-y-2">
            <div className="text-sm font-medium text-red-600">Atlas UI Error</div>
            <div className="text-xs text-gray-500 max-w-xs break-words">
              {this.state.error}
            </div>
            <button
              onClick={() => this.setState({ hasError: false, error: "" })}
              className="text-xs text-atlas-600 underline"
            >
              Retry
            </button>
          </div>
        </div>
      )
    }
    return this.props.children
  }
}

// --- Main Panel ---

type View = "posts" | "adhoc" | "queue" | "setup" | "settings" | "logs"

function SidePanelInner() {
  const [queue] = useQueueState()
  const [view, setView] = useState<View>("posts")
  const portRef = useRef<chrome.runtime.Port | null>(null)
  const didAutoSwitch = useRef(false)

  // Auto-switch to queue view ONCE on first load if leads exist
  useEffect(() => {
    if (!didAutoSwitch.current && queue && queue.leads.length > 0) {
      didAutoSwitch.current = true
      setView("queue")
    }
  }, [queue?.leads.length])

  // Heartbeat: keep background service worker alive (with reconnect)
  useEffect(() => {
    let interval: ReturnType<typeof setInterval> | null = null
    let alive = true

    function connect() {
      try {
        const port = chrome.runtime.connect({ name: "heartbeat" })
        portRef.current = port

        port.onDisconnect.addListener(() => {
          portRef.current = null
          // Reconnect after a short delay if component is still mounted
          if (alive) setTimeout(connect, 2000)
        })

        interval = setInterval(() => {
          try {
            port.postMessage({ type: "PING" })
          } catch {
            // Port died — onDisconnect will handle reconnect
          }
        }, HEARTBEAT_INTERVAL)
      } catch {
        // Service worker not ready — retry
        if (alive) setTimeout(connect, 2000)
      }
    }

    connect()

    return () => {
      alive = false
      if (interval) clearInterval(interval)
      try { portRef.current?.disconnect() } catch { /* ignore */ }
    }
  }, [])

  const isConnected = queue !== null

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <Header connected={isConnected} />

      {/* Tab bar */}
      <div className="flex border-b border-gray-200 bg-white px-4">
        <TabButton label="Posts" active={view === "posts"} onClick={() => setView("posts")} />
        <TabButton label="Quick Reply" active={view === "adhoc"} onClick={() => setView("adhoc")} />
        <TabButton label="Queue" active={view === "queue"} onClick={() => setView("queue")} />
        <TabButton label="Settings" active={view === "settings"} onClick={() => setView("settings")} />
        <TabButton label="Logs" active={view === "logs"} onClick={() => setView("logs")} />
      </div>

      {/* Content area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {view === "posts" && <PostsTab />}

        {view === "adhoc" && <AdHocReply />}

        {view === "setup" && <CsvImport onImported={() => setView("queue")} />}

        {view === "queue" && queue && (
          <>
            <ProgressBar queue={queue} />
            {queue.status === "completed" && <RunSummary queue={queue} />}
            <TaskQueue queue={queue} />
            <Controls queue={queue} />
            <ExportResults queue={queue} />
          </>
        )}
        {view === "queue" && !queue && (
          <div className="flex-1 flex items-center justify-center p-4">
            <p className="text-xs text-gray-400 text-center">
              No queue loaded. Import a CSV to get started.
            </p>
          </div>
        )}

        {view === "settings" && (
          <div className="flex-1 overflow-y-auto">
            <ModelSelector />
            <div className="border-t border-gray-200" />
            <ApiKeySetup />
            <div className="border-t border-gray-200" />
            <EnrichmentImport onComplete={(count) => console.log(`Enriched ${count} contacts`)} />
          </div>
        )}

        {view === "logs" && <DebugLogViewer />}
      </div>
    </div>
  )
}

function TabButton({
  label,
  active,
  onClick,
}: {
  label: string
  active: boolean
  onClick: () => void
}) {
  return (
    <button
      onClick={onClick}
      className={`px-3 py-2 text-xs font-medium border-b-2 transition-colors ${
        active
          ? "border-atlas-500 text-atlas-700"
          : "border-transparent text-gray-400 hover:text-gray-600"
      }`}
    >
      {label}
    </button>
  )
}

function SidePanel() {
  return (
    <ErrorBoundary>
      <SidePanelInner />
    </ErrorBoundary>
  )
}

export default SidePanel
