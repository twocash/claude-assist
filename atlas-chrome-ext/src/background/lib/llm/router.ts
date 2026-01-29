import { SecureStorage } from "@plasmohq/storage/secure"
import { Storage } from "@plasmohq/storage"
import { STORAGE_KEYS } from "~src/lib/storage"
import { MODEL_OPTIONS } from "~src/types/llm"
import type { LlmRequest, LlmResponse } from "~src/types/llm"
import { callAnthropic } from "./anthropic"
import { callOpenRouter } from "./openrouter"

const storage = new Storage({ area: "local" })
const secureStorage = new SecureStorage({ area: "local" })
const STORAGE_PASSWORD = "atlas-ext-v1"

/**
 * Route an LLM request to the correct provider based on the provided model
 * or the user's selected model in storage.
 */
export async function routeLlmRequest(request: LlmRequest & { model?: string }): Promise<LlmResponse> {
  // Get model - prefer request.model, fall back to storage selection
  const requestedModel = request.model
  const selectedModelId = requestedModel || await storage.get<string>(STORAGE_KEYS.SELECTED_MODEL)
  const modelConfig = MODEL_OPTIONS.find((m) => m.model === selectedModelId || m.id === selectedModelId) || MODEL_OPTIONS[0]!

  // Get API key for the provider
  await secureStorage.setPassword(STORAGE_PASSWORD)

  if (modelConfig.provider === "anthropic") {
    const apiKey = await secureStorage.get(STORAGE_KEYS.ANTHROPIC_KEY).catch(() => "")
    if (!apiKey) {
      return { text: "", model: modelConfig.model, error: "Anthropic API key not set" }
    }
    return callAnthropic(apiKey as string, modelConfig.model, request)
  }

  if (modelConfig.provider === "openrouter") {
    const apiKey = await secureStorage.get(STORAGE_KEYS.OPENROUTER_KEY).catch(() => "")
    if (!apiKey) {
      return { text: "", model: modelConfig.model, error: "OpenRouter API key not set" }
    }
    return callOpenRouter(apiKey as string, modelConfig.model, request)
  }

  return { text: "", model: "", error: `Unknown provider: ${modelConfig.provider}` }
}
