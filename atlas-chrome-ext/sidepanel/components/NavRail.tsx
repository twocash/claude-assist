import React from "react"

export type ViewId = "inbox" | "outreach" | "studio" | "data" | "settings"

interface NavRailProps {
  activeView: ViewId
  onSelect: (view: ViewId) => void
  hasActiveTask: boolean
  inboxCount?: number
}

export function NavRail({ activeView, onSelect, hasActiveTask, inboxCount = 3 }: NavRailProps) {
  return (
    <div className="w-14 flex flex-col items-center py-4 bg-gray-50 border-r border-gray-200 gap-6 flex-shrink-0">

      {/* 1. Inbox (Top Priority) */}
      <NavButton
        id="inbox"
        label="Inbox"
        active={activeView === "inbox"}
        onClick={() => onSelect("inbox")}
        badge={inboxCount > 0}
        badgeCount={inboxCount}
      >
        {/* Inbox Icon */}
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
        </svg>
      </NavButton>

      {/* 2. Outreach (The "Work" Mode) */}
      <NavButton
        id="outreach"
        label="Outreach"
        active={activeView === "outreach"}
        onClick={() => onSelect("outreach")}
        badge={hasActiveTask} // Green pulsing dot if scraper is running
      >
        {/* Icon: Rocket/List */}
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
      </NavButton>

{/* 3. Studio (The "Creative" Mode) */}
      <NavButton
        id="studio"
        label="Studio"
        active={activeView === "studio"}
        onClick={() => onSelect("studio")}
      >
        {/* Icon: Pencil/Edit */}
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
        </svg>
      </NavButton>

      {/* 4. Data (Passive Tasks) */}
      <NavButton
        id="data"
        label="Data"
        active={activeView === "data"}
        onClick={() => onSelect("data")}
      >
        {/* Icon: Database/Storage */}
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
        </svg>
      </NavButton>

      {/* 5. Settings (Bottom Config) */}
      <div className="mt-auto">
        <NavButton
          id="settings"
          label="Settings"
          active={activeView === "settings"}
          onClick={() => onSelect("settings")}
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </NavButton>
      </div>
    </div>
  )
}

interface NavButtonProps {
  id: string
  label: string
  active: boolean
  onClick: () => void
  children: React.ReactNode
  badge?: boolean
  badgeCount?: number
}

function NavButton({ id, label, active, onClick, children, badge, badgeCount }: NavButtonProps) {
  return (
    <button
      onClick={onClick}
      className={`group relative p-2 rounded-xl transition-all duration-200 ${
        active
          ? "bg-blue-100 text-blue-600 shadow-sm"
          : "text-gray-400 hover:bg-gray-100 hover:text-gray-600"
      }`}
      title={label}
    >
      {children}
      {active && <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-blue-600 rounded-r-full -ml-2" />}
      {badge && (
        <>
          {badgeCount && badgeCount > 0 ? (
            <span className="absolute -top-1 -right-1 min-w-[18px] h-[18px] bg-blue-500 text-white text-[9px] font-bold rounded-full flex items-center justify-center px-1">
              {badgeCount > 99 ? '99+' : badgeCount}
            </span>
          ) : (
            <span className="absolute top-1 right-1 w-2.5 h-2.5 bg-green-500 border-2 border-white rounded-full">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
            </span>
          )}
        </>
      )}
    </button>
  )
}
