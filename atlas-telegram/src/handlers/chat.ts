/**
 * Atlas Telegram Bot - Chat Handler
 *
 * Handles chat intent: conversational, unclear, general chat
 */

import type { Context } from "grammy";
import type { IntentDetectionResult } from "../types";
import { generateResponse, generateResponseWithTools } from "../claude";
import { logger } from "../logger";
import { audit } from "../audit";

// Simple conversation history per user (in-memory)
const conversationHistory = new Map<number, Array<{ role: "user" | "assistant"; content: string }>>();

/**
 * Handle chat intent - conversational response
 */
export async function handleChatIntent(
  ctx: Context,
  _intentResult: IntentDetectionResult
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
    // Get conversation history
    const history = conversationHistory.get(userId) || [];

    // Detect if this might need tools (looks like a data query)
    const mightNeedTools = /\b(inbox|queue|work|status|tasks?|items?|what'?s|show|list|urgent|p0|priority|focus|should|blocked|atlas|how'?s)\b/i.test(text);

    // Use tool-aware response if message hints at needing data
    const response = mightNeedTools
      ? await generateResponseWithTools(text, history)
      : await generateResponse(text, history);

    // Update history
    history.push({ role: "user", content: text });
    history.push({ role: "assistant", content: response });

    // Keep only last 10 exchanges
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

/**
 * Get quick response for common messages
 */
function getQuickResponse(text: string): string | null {
  const lowerText = text.toLowerCase().trim();

  // Greetings
  if (/^(hey|hi|hello|yo|sup)!?$/.test(lowerText)) {
    return "Hey. What's up?";
  }

  // Thanks
  if (/^(thanks|thank you|thx|ty)!?$/.test(lowerText)) {
    return "Got it.";
  }

  // Acknowledgments
  if (/^(ok|okay|cool|nice|good|great|perfect)!?$/.test(lowerText)) {
    return "Anything else?";
  }

  // Help
  if (/^(help|help me|\?)$/.test(lowerText)) {
    return `I can help with:
- Share a URL to capture
- "what's in my inbox?" to see items
- "status" for overview
- "find [term]" to search
- "mark [item] as done" to update`;
  }

  return null;
}

/**
 * Clear conversation history for a user
 */
export function clearConversationHistory(userId: number): void {
  conversationHistory.delete(userId);
  logger.debug("Cleared conversation history", { userId });
}
