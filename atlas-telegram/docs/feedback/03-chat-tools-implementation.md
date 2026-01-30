# Chat Handler with Tool Access

## Problem

When intent detection routes to "chat", Claude has no tools. Conversational queries like:

- "what should I focus on today?"
- "anything urgent?"
- "how's the inbox looking?"

...get empty responses because Claude can't look anything up.

## Solution

Add `generateResponseWithTools()` to `src/claude.ts` that gives Claude access to query tools.

## Implementation

### Add to `src/claude.ts`

```typescript
/**
 * Generate response with tool access (for conversational queries)
 */
export async function generateResponseWithTools(
  message: string,
  conversationHistory: Array<{ role: "user" | "assistant"; content: string }>
): Promise<string> {
  logger.debug("Generating response with tools", { message: message.substring(0, 100) });

  const tools: Anthropic.Tool[] = [
    {
      name: "query_inbox",
      description: "Get items from the inbox. Returns recent sparks/captures.",
      input_schema: {
        type: "object" as const,
        properties: {
          pillar: { 
            type: "string", 
            enum: ["The Grove", "Personal", "Consulting", "Home"],
            description: "Filter by pillar (optional)"
          },
          limit: { type: "number", description: "Max items to return (default 5)" }
        },
        required: []
      }
    },
    {
      name: "query_work_queue", 
      description: "Get items from the work queue. Returns active tasks.",
      input_schema: {
        type: "object" as const,
        properties: {
          status: {
            type: "string",
            enum: ["Queued", "In Progress", "Blocked", "Done"],
            description: "Filter by status (optional)"
          },
          limit: { type: "number", description: "Max items to return (default 5)" }
        },
        required: []
      }
    },
    {
      name: "get_status",
      description: "Get a summary of inbox and work queue counts, including P0 items.",
      input_schema: {
        type: "object" as const,
        properties: {},
        required: []
      }
    },
    {
      name: "get_atlas_state",
      description: "Get Atlas's current state, pending tasks, and recent activity.",
      input_schema: {
        type: "object" as const,
        properties: {},
        required: []
      }
    }
  ];

  const systemPrompt = `${atlasIdentity}

You are chatting with Jim via Telegram. You have tools to look up his inbox, work queue, and Atlas state.

RULES:
- If Jim asks about inbox, queue, tasks, status, or priorities — USE THE TOOLS
- Don't guess or make up items — look them up
- Be concise. This is mobile. No walls of text.
- Lead with what matters. Skip pleasantries.
- If something is urgent (P0, blocked), mention it first.

VOICE:
- Direct, efficient, zero-bullshit
- Like a sharp exec assistant, not a chatbot
- No "Great question!" or "I'd be happy to help"
- Just answer.

EXAMPLES:
- "3 items in your inbox. 2 Grove, 1 Consulting."
- "Queue's clear. Nothing blocking."
- "Found 2 P0s that need attention."
`;

  try {
    const messages: Anthropic.MessageParam[] = [
      ...conversationHistory.map(m => ({
        role: m.role as "user" | "assistant",
        content: m.content,
      })),
      { role: "user" as const, content: message },
    ];

    let response = await anthropic.messages.create({
      model: "claude-sonnet-4-20250514",
      max_tokens: 500,
      system: systemPrompt,
      messages,
      tools,
    });

    // Handle tool use loop (max 3 iterations to prevent runaway)
    let iterations = 0;
    while (response.stop_reason === "tool_use" && iterations < 3) {
      iterations++;
      
      const toolUseBlock = response.content.find(block => block.type === "tool_use");
      if (!toolUseBlock || toolUseBlock.type !== "tool_use") break;

      logger.debug("Tool call", { tool: toolUseBlock.name, input: toolUseBlock.input });
      
      const toolResult = await executeToolCall(toolUseBlock.name, toolUseBlock.input);

      messages.push({ role: "assistant", content: response.content });
      messages.push({
        role: "user",
        content: [{
          type: "tool_result",
          tool_use_id: toolUseBlock.id,
          content: JSON.stringify(toolResult)
        }]
      });

      response = await anthropic.messages.create({
        model: "claude-sonnet-4-20250514",
        max_tokens: 500,
        system: systemPrompt,
        messages,
        tools,
      });
    }

    const textContent = response.content.find(block => block.type === "text");
    return textContent?.type === "text" ? textContent.text.trim() : "I'm here. What do you need?";

  } catch (error) {
    logger.error("Response with tools failed", { error });
    return "Something went wrong. Try again?";
  }
}

/**
 * Execute a tool call and return results
 */
async function executeToolCall(toolName: string, input: unknown): Promise<unknown> {
  const { queryInbox, queryWorkQueue, getStatusSummary } = await import("./notion");
  const { getState, getTasks, getHeartbeat } = await import("./atlas-system");
  
  switch (toolName) {
    case "query_inbox": {
      const params = input as { pillar?: string; limit?: number };
      const result = await queryInbox({ 
        pillar: params.pillar as any, 
        limit: params.limit || 5 
      });
      return result.items.map(i => ({ 
        title: i.title, 
        pillar: i.pillar, 
        status: i.status 
      }));
    }
    
    case "query_work_queue": {
      const params = input as { status?: string; limit?: number };
      const result = await queryWorkQueue({ 
        status: params.status as any,
        limit: params.limit || 5 
      });
      return result.items.map(i => ({ 
        title: i.title, 
        status: i.status, 
        priority: i.priority 
      }));
    }
    
    case "get_status": {
      return await getStatusSummary();
    }
    
    case "get_atlas_state": {
      const state = getState();
      const tasks = getTasks();
      const heartbeat = getHeartbeat();
      return {
        status: heartbeat.status,
        lastActive: state.lastActive,
        pendingTasks: tasks.queue.length,
        stats: state.stats
      };
    }
    
    default:
      return { error: "Unknown tool" };
  }
}
```

### Update `src/handlers/chat.ts`

```typescript
import { generateResponse, generateResponseWithTools } from "../claude";

export async function handleChatIntent(
  ctx: Context,
  intentResult: IntentDetectionResult
): Promise<void> {
  const userId = ctx.from!.id;
  const text = ctx.message?.text || "";

  logger.info("Processing chat intent", { userId, text: text.substring(0, 100) });

  await ctx.replyWithChatAction("typing");

  // Check for quick responses first
  const quickResponse = getQuickResponse(text);
  if (quickResponse) {
    await ctx.reply(quickResponse);
    audit.logResponse(userId, quickResponse);
    return;
  }

  try {
    const history = conversationHistory.get(userId) || [];

    // Detect if this might need tools (looks like a data query)
    const mightNeedTools = /\b(inbox|queue|work|status|tasks?|items?|what'?s|show|list|urgent|p0|priority|focus|should|blocked)\b/i.test(text);

    // Use tool-aware response if message hints at needing data
    const response = mightNeedTools 
      ? await generateResponseWithTools(text, history)
      : await generateResponse(text, history);

    // Update history
    history.push({ role: "user", content: text });
    history.push({ role: "assistant", content: response });

    if (history.length > 20) {
      history.splice(0, history.length - 20);
    }
    conversationHistory.set(userId, history);

    await ctx.reply(response);
    audit.logResponse(userId, response);
  } catch (error) {
    logger.error("Chat response failed", { error });
    await ctx.reply("I'm here. What do you need?");
  }
}
```

## Testing

After implementation, test these queries:

| Query | Expected Behavior |
|-------|-------------------|
| "what's in my inbox?" | Uses `query_inbox` tool, returns items |
| "anything urgent?" | Uses `get_status`, highlights P0s |
| "what should I focus on?" | Uses both `get_status` and `query_work_queue`, reasons about priority |
| "how's Atlas doing?" | Uses `get_atlas_state`, reports health |
| "hey" | Quick response, no tools |
| "thanks" | Quick response, no tools |

## Cost Considerations

Tool-aware responses use more tokens (~2x a simple chat response). The `mightNeedTools` regex limits this to queries that actually need data. Simple greetings and acknowledgments still use the fast path.
