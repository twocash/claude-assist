import { useState } from "react"
import { usePostsState } from "~src/lib/posts-hooks"
import { useCommentsState } from "~src/lib/comments-hooks"
import type { PhantomSlot } from "~src/types/posts"
import { PostRow } from "./PostRow"
import { AddPostForm } from "./AddPostForm"
import { CommentQueue } from "./CommentQueue"

type SubView = "posts" | "replies"

export function PostsTab() {
  const [postsState, { addPost, updatePost, removePost, refreshStats }] = usePostsState()
  const [commentsState, { updateComment, removeComment, replaceAllComments, loadMockData }] = useCommentsState()
  const [showAddForm, setShowAddForm] = useState(false)
  const [isRefreshing, setIsRefreshing] = useState(false)
  const [subView, setSubView] = useState<SubView>("posts")

  const needsReplyCount = commentsState.comments.filter((c) => c.status === "needs_reply").length
  const [isSyncing, setIsSyncing] = useState(false)
  const [syncStatus, setSyncStatus] = useState<string | null>(null)

  const handleFullSync = async () => {
    setIsSyncing(true)
    setSyncStatus("PB → Classify → Notion → Replies...")

    try {
      const response = await chrome.runtime.sendMessage({ name: "RUN_FULL_SYNC" })

      if (response?.ok) {
        const r = response.result
        const summary = `${r.newContacts} new • ${r.newEngagements} engagements • ${r.commentsNeedingReply?.length || 0} need reply`
        setSyncStatus(summary)

        // Replace all comments with fresh data from Notion
        await replaceAllComments(r.commentsNeedingReply || [])

        setTimeout(() => setSyncStatus(null), 5000)
      } else {
        setSyncStatus(`Error: ${response?.error || "Unknown error"}`)
        setTimeout(() => setSyncStatus(null), 5000)
      }
    } catch (e) {
      setSyncStatus(`Error: ${e}`)
      setTimeout(() => setSyncStatus(null), 5000)
    } finally {
      setIsSyncing(false)
    }
  }

  const handleTestLeadsAPI = async () => {
    console.log("PostsTab: Test API button clicked")
    try {
      console.log("PostsTab: Sending TEST_LEADS_API message...")
      const response = await chrome.runtime.sendMessage({ name: "TEST_LEADS_API" })
      console.log("PostsTab: Got response:", response)
      alert(JSON.stringify(response, null, 2))
    } catch (e) {
      console.error("PostsTab: Error:", e)
      alert(`Error: ${e}`)
    }
  }

  const handleAddPost = async (url: string, title: string) => {
    const post = await addPost(url, title)
    if (post) {
      setShowAddForm(false)
    }
  }

  const handleMonitor = async (postId: string) => {
    // Update status to running
    await updatePost(postId, { scrapeStatus: "running" })
    // Send message to background to launch PB scrape
    chrome.runtime.sendMessage({ name: "MONITOR_POST", body: { postId } })
  }

  const handleRefresh = async () => {
    setIsRefreshing(true)
    await refreshStats()
    setTimeout(() => setIsRefreshing(false), 2000)
  }

  // Calculate totals
  const totals = postsState.posts.reduce(
    (acc, post) => ({
      impressions: acc.impressions + post.impressions,
      reactions: acc.reactions + post.reactions,
      comments: acc.comments + post.comments,
    }),
    { impressions: 0, reactions: 0, comments: 0 }
  )

  
  // If viewing replies, render the CommentQueue instead
  if (subView === "replies") {
    return (
      <div className="flex flex-col h-full">
        {/* Sub-nav */}
        <div className="px-4 py-2 bg-white border-b border-gray-200 flex items-center gap-2">
          <button
            onClick={() => setSubView("posts")}
            className="text-[10px] text-gray-500 hover:text-gray-700"
          >
            ← Posts
          </button>
          <span className="text-[10px] text-gray-300">|</span>
          <span className="text-[10px] font-medium text-gray-800">Replies</span>
          {commentsState.comments.length === 0 && (
            <button
              onClick={loadMockData}
              className="ml-auto text-[9px] text-atlas-600 hover:text-atlas-700"
            >
              Load test data
            </button>
          )}
        </div>
        <CommentQueue
          comments={commentsState.comments}
          onUpdateComment={updateComment}
          onRemoveComment={removeComment}
          onBulkMarkReplied={() => {}}
        />
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full">
      {/* Header with totals */}
      <div className="px-4 py-3 bg-white border-b border-gray-200">
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-sm font-semibold text-gray-800">Post Analytics</h2>
          <div className="flex gap-2">
            <button
              onClick={() => setSubView("replies")}
              className="text-[10px] text-atlas-600 hover:text-atlas-700 relative"
            >
              Replies
              {needsReplyCount > 0 && (
                <span className="absolute -top-1 -right-2 w-4 h-4 bg-amber-500 text-white text-[8px] rounded-full flex items-center justify-center">
                  {needsReplyCount}
                </span>
              )}
            </button>
            <span className="text-gray-300">|</span>
            <button
              onClick={handleFullSync}
              disabled={isSyncing}
              className="text-[10px] bg-green-600 text-white px-2 py-1 rounded hover:bg-green-700 disabled:opacity-50"
            >
              {isSyncing ? "Syncing..." : "Sync All"}
            </button>
            <button
              onClick={handleTestLeadsAPI}
              className="text-[10px] text-purple-600 hover:text-purple-700"
            >
              Test API
            </button>
            <button
              onClick={() => window.open('https://phantombuster.com/2316148405398457/leads', 'pb_leads')}
              className="text-[10px] text-gray-600 hover:text-gray-700"
            >
              PB Leads →
            </button>
            <button
              onClick={() => setShowAddForm(true)}
              className="text-[10px] bg-atlas-600 text-white px-2 py-1 rounded hover:bg-atlas-700"
            >
              + Add
            </button>
          </div>
        </div>

        {/* Sync status banner */}
        {syncStatus && (
          <div className={`text-[10px] px-2 py-1 rounded mb-2 ${
            syncStatus.includes("Error") ? "bg-red-100 text-red-700" : "bg-green-100 text-green-700"
          }`}>
            {syncStatus}
          </div>
        )}

        {/* Totals row */}
        <div className="grid grid-cols-3 gap-2 text-center">
          <div className="bg-gray-50 rounded p-2">
            <div className="text-lg font-bold text-gray-800">{totals.impressions.toLocaleString()}</div>
            <div className="text-[9px] text-gray-500 uppercase">Impressions</div>
          </div>
          <div className="bg-blue-50 rounded p-2">
            <div className="text-lg font-bold text-blue-600">{totals.reactions.toLocaleString()}</div>
            <div className="text-[9px] text-gray-500 uppercase">Reactions</div>
          </div>
          <div className="bg-green-50 rounded p-2">
            <div className="text-lg font-bold text-green-600">{totals.comments.toLocaleString()}</div>
            <div className="text-[9px] text-gray-500 uppercase">Comments</div>
          </div>
        </div>
      </div>

      {/* Add post form modal */}
      {showAddForm && (
        <AddPostForm
          onAdd={handleAddPost}
          onCancel={() => setShowAddForm(false)}
        />
      )}

      {/* Posts list */}
      <div className="flex-1 overflow-y-auto">
        {postsState.posts.length === 0 ? (
          <div className="flex items-center justify-center h-full p-4">
            <div className="text-center">
              <div className="text-gray-400 text-sm mb-2">No posts monitored yet</div>
              <button
                onClick={() => setShowAddForm(true)}
                className="text-xs text-atlas-600 hover:underline"
              >
                Add your first post
              </button>
            </div>
          </div>
        ) : (
          <div className="divide-y divide-gray-100">
            {postsState.posts.map((post) => (
              <PostRow
                key={post.id}
                post={post}
                onMonitor={() => handleMonitor(post.id)}
                onRemove={() => removePost(post.id)}
                onAssignSlot={(slot) => updatePost(post.id, { phantomSlot: slot })}
              />
            ))}
          </div>
        )}
      </div>

      {/* Last updated footer */}
      {postsState.lastUpdated && (
        <div className="px-4 py-1 bg-gray-50 border-t border-gray-200">
          <span className="text-[9px] text-gray-400">
            Last updated: {new Date(postsState.lastUpdated).toLocaleString()}
          </span>
        </div>
      )}
    </div>
  )
}
