interface HeaderProps {
  connected: boolean
}

export function Header({ connected }: HeaderProps) {
  return (
    <div className="flex items-center gap-2 px-4 py-3 border-b border-gray-200 bg-white">
      <div className="w-7 h-7 rounded-lg bg-atlas-600 flex items-center justify-center flex-shrink-0">
        <span className="text-white font-bold text-xs">A</span>
      </div>
      <div className="flex-1 min-w-0">
        <h1 className="text-sm font-semibold text-gray-900 leading-tight">Atlas</h1>
        <p className="text-[10px] text-gray-400 leading-tight">Sales Nav Assistant</p>
      </div>
      <div className="flex items-center gap-1.5">
        <div
          className={`w-2 h-2 rounded-full ${connected ? "bg-green-500" : "bg-gray-300"}`}
        />
        <span className="text-[10px] text-gray-400">
          {connected ? "Ready" : "Idle"}
        </span>
      </div>
    </div>
  )
}
