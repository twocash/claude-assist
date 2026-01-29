import React, { useState, useEffect } from "react"
import { AdHocReply } from "./AdHocReply"

// Mock data to start - in Phase 3 we connect this to the scraper
const MOCK_INBOX_ITEMS = [
  { id: 1, type: "comment", author: "Sarah Chen", preview: "This is a great point about the API limitations...", time: "2m ago" },
  { id: 2, type: "dm", author: "David Miller", preview: "Hey, saw your post about Atlas. Are you free to chat?", time: "1h ago" },
  { id: 3, type: "mention", author: "TechCrunch", preview: "mentioning @Atlas in their latest roundup...", time: "3h ago" }
]

export function Inbox() {
  const [selectedItem, setSelectedItem] = useState<number | null>(null)

  return (
    <div className="h-full flex flex-col bg-white">
      {/* 1. Inbox Header */}
      <div className="p-4 border-b border-gray-100 flex justify-between items-center">
        <h2 className="text-sm font-bold text-gray-900">Inbox</h2>
        <span className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full">3 New</span>
      </div>

      {/* 2. The Split View */}
      <div className="flex-1 overflow-hidden flex flex-col">
        {selectedItem ? (
          // --- WRITE MODE ---
          <div className="flex-1 flex flex-col">
            <div className="p-2 border-b border-gray-100 bg-gray-50 flex items-center gap-2">
              <button
                onClick={() => setSelectedItem(null)}
                className="p-1 hover:bg-gray-200 rounded text-gray-500"
              >
                ← Back
              </button>
              <span className="text-xs font-medium text-gray-600">
                Replying to {MOCK_INBOX_ITEMS.find(i => i.id === selectedItem)?.author}
              </span>
            </div>
            <div className="flex-1 p-2">
              {/* Re-using your AdHocReply component here! */}
              <AdHocReply />
            </div>
          </div>
        ) : (
          // --- LIST MODE ---
          <div className="flex-1 overflow-y-auto">
            {MOCK_INBOX_ITEMS.map((item) => (
              <button
                key={item.id}
                onClick={() => setSelectedItem(item.id)}
                className="w-full p-4 border-b border-gray-50 hover:bg-gray-50 text-left group transition-colors"
              >
                <div className="flex justify-between mb-1">
                  <span className="text-xs font-bold text-gray-800">{item.author}</span>
                  <span className="text-[10px] text-gray-400">{item.time}</span>
                </div>
                <div className="text-xs text-gray-600 line-clamp-2 leading-relaxed">
                  <span className={`inline-block w-2 h-2 rounded-full mr-2 ${item.type === 'comment' ? 'bg-orange-400' : item.type === 'dm' ? 'bg-blue-400' : 'bg-purple-400'
                    }`} />
                  {item.preview}
                </div>
              </button>
            ))}
            <div className="p-8 text-center text-xs text-gray-400">
              <p>All caught up!</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
