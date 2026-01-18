> [Original Source: Edge AI Capability Trajectory 2023 - 2025 A Technical Vision.md]

# Edge AI Capability Trajectory 2023-2025: A Technical Vision

Research Brief
Jim Calhoun
The Grove Foundation
December 2025

**The convergence of model efficiency breakthroughs, quantization advances, and open-source ecosystem velocity has compressed what once took decades of computing democratization into months.** Between GPT-4's March 2023 release and Meta's Llama 3.1 405B achieving benchmark parity in July 2024, frontier AI capabilities migrated to open models in just 16 months. Stanford HAI's 2025 AI Index documents a **280-fold reduction** in inference costs over 18 months—from $20 per million tokens to $0.07 for GPT-3.5-equivalent performance. This paper synthesizes empirical evidence across model efficiency, quantization research, edge deployment infrastructure, and hybrid architectures to establish the technical foundation for enterprise edge AI strategy.

## Model efficiency has achieved 142x parameter compression

The Phi series from Microsoft Research demonstrates the most dramatic efficiency trajectory in foundation model development. Phi-1 (June 2023) achieved **50.6% on HumanEval** with just 1.3B parameters, proving that curated training data ("Textbooks Are All You Need") could substitute for scale. Phi-3-mini (April 2024) reached **68.8% on MMLU** with 3.8B parameters—matching PaLM 540B's benchmark performance while requiring 142 times fewer parameters. The technical report documents this model running natively on iPhone 14's A16 Bionic chip. Phi-4 (December 2024) pushed further, achieving **82.6% on HumanEval** and **80.4% on MATH** with 14B parameters, outperforming Llama-3.3-70B on GPQA reasoning benchmarks.

Meta's Llama family progression established the open-weight paradigm's competitive viability. LLaMA-1 (February 2023) demonstrated that a 13B model could outperform GPT-3 175B on most benchmarks through efficient training on publicly available data. Llama 3.1 405B (July 2024) achieved **87.3% on MMLU** versus GPT-4-Turbo's 86.5%, marking the first open model to match frontier closed-model performance. Llama 3.2's edge-optimized variants (September 2024) brought this capability downward: the 3B model achieves **63.4% MMLU** while running on Qualcomm and MediaTek mobile chips with 128K context windows.

Alibaba's Qwen2.5 family (September 2024) extended this efficiency frontier across seven model sizes from 0.5B to 72B parameters, trained on 18 trillion tokens across 29+ languages. The Qwen2.5-72B achieves **86.1% on MMLU**—results the technical report claims are "comparable to Llama-3-405B using only 1/5 the parameters." This efficiency claim extends to specialized domains: Qwen2.5-Coder-32B-Instruct matches GPT-4o on code generation while Qwen2.5-7B-Base outperforms DeepSeek-Coder-33B across five benchmarks.

## Quantization preserves over 98% of model capabilities

The Red Hat/Neural Magic study represents the most comprehensive quantization analysis published, conducting **over 500,000 individual evaluations** across the Llama 3.1 family at 8B, 70B, and 405B scales. FP8 quantization (W8A8-FP) proved "effectively lossless" across all model scales, while INT4 quantization (W4A16-INT) retained **98.9% of baseline performance** on HumanEval with 3.5x memory compression. The study's most significant finding for edge deployment: 4-bit quantization enables the 405B model to run on 4 GPUs versus 16 for BF16, representing **5-7x cost reduction** with minimal capability degradation.

Three quantization methods have emerged as production standards, each optimized for different deployment scenarios. **GPTQ** (arXiv:2210.17323), published at ICLR 2023, uses approximate second-order Hessian information for one-shot quantization, compressing OPT-175B with perplexity increase from 8.34 to 8.68 (3-bit) and achieving 3.25x speedup on A100 GPUs. **AWQ** (arXiv:2306.00978), winning MLSys 2024 Best Paper, identifies that protecting only 1% of salient weights using activation distributions preserves model quality—achieving 1.45x speedup over GPTQ and enabling 70B Llama-2 deployment on mobile GPUs through the TinyChat implementation. **GGUF** format, introduced by the llama.cpp project in August 2023, provides a self-contained binary format supporting 2-bit to 8-bit quantization with CPU inference and optional GPU offloading, now hosting over 100,000 quantized models on HuggingFace.

The memory footprint relationship follows a deterministic formula: **Memory (GB) = Parameters (billions) × Bytes per parameter × 1.2 overhead factor**. A 7B model requires 14GB at FP16, 7GB at INT8, and 3.5GB at INT4—the latter fitting comfortably within smartphone RAM constraints. The NVIDIA technical blog documents additional KV-cache requirements during inference: for Llama 2 7B at FP16 with 4096 context length, approximately 2GB of cache memory is required beyond model weights.

## Edge deployment infrastructure has reached production scale

The llama.cpp project has accumulated **85,000+ GitHub stars** and established itself as the de facto edge inference runtime. The project supports x86 (AVX through AVX-512), ARM NEON, and RISC-V vector extensions, with GPU backends spanning CUDA, Metal, Vulkan, and SYCL. FlashAttention support (April 2024), multimodal capabilities via libmtmd (April 2025), and Android/ChromeOS GUI acceleration (December 2025) document the rapid feature velocity. The GGUF format the project introduced now dominates edge model distribution.

Ollama's deployment footprint provides empirical evidence of edge AI adoption velocity. Security research from Tenthe AI (April 2025) identified **174,590 internet-exposed Ollama instances** with a 24.18% API accessibility rate—the majority concentrated on AWS, Alibaba Cloud, and Tencent Cloud infrastructure. Model deployment analysis reveals llama3:latest (12,659 unique IPs), deepseek-r1:latest (12,572), and mistral:latest (11,163) as the most deployed models, with 7B-8B parameter Q4 quantizations representing the dominant configuration.

Apple's MLX framework, optimized for unified memory architecture on Apple Silicon, demonstrates the hardware-software co-optimization opportunity. Academic benchmarks document **~230 tokens/second** on M2 Ultra for Qwen 3B models—significantly outperforming PyTorch MPS (7-9 tok/s) and llama.cpp (150 tok/s short-context) on equivalent hardware. The framework's native quantization support and GPU/CPU execution without memory transfer penalties position it as the reference implementation for Apple hardware deployment. Simon Willison's testing of Kimi K2 1T (4-bit) on dual M3 Ultra systems (512GB each) achieved approximately 15 tokens/second, demonstrating that even trillion-parameter models have become accessible on high-end consumer hardware.

Mobile NPU capabilities have reached a critical threshold for on-device inference. While the commonly cited "73 TOPS" figure for Snapdragon 8 Elite could not be verified in official Qualcomm documentation, the confirmed specifications show **45% NPU improvement** over the predecessor with **up to 70 tokens/second** for small language models. The Snapdragon X Elite laptop chips deliver 45 TOPS NPU performance. MediaTek's Dimensity 9400 NPU 890 achieves **50 TOPS** with benchmark scores of 6,773 on AI Benchmark—obliterating Qualcomm Snapdragon 8 Gen 3 (3,633) and Apple A17 Pro (3,428). Samsung's Exynos 2500 (3nm GAA) delivers **59 TOPS** with its 24K MAC NPU architecture.

Google's LiteRT (rebranded from TensorFlow Lite in September 2024) documents deployment across **2.7 billion devices** powering over 100,000 applications. The framework claims up to 25x faster inference versus CPU with NPU acceleration and 5x lower power consumption—critical metrics for always-on edge AI applications.

## The ratchet pattern compresses frontier-to-local lag to under 12 months

The capability transfer timeline from frontier to open models has compressed dramatically. GPT-4's March 2023 release to Llama 3.1 405B's benchmark parity in July 2024 represents **16 months**—but this gap is shrinking. Stanford Alpaca (March 2023) replicated ChatGPT-like capabilities from GPT-3.5 (November 2022) in just **3.5 months** at a total cost under $600: less than $500 for data generation via OpenAI API and less than $100 for 3 hours of fine-tuning on 8× A100 GPUs.

Epoch AI's systematic analysis establishes that "once-frontier AI capabilities are reached by open models with a lag of **about one year**." The UK AI Security Institute's frontier trends report documents the gap narrowing to "between four and eight months" based on external benchmark data. This compression follows predictable economic dynamics: Andreessen Horowitz's "LLMflation" analysis documents **1,000x cost reduction** over three years—from $60 per million tokens for GPT-3 at MMLU 42 (November 2021) to $0.06 for Llama 3.2 3B achieving equivalent performance.

Stanford HAI's 2025 AI Index Report provides the most rigorous analysis of this trajectory. The cost of querying a model achieving GPT-3.5-equivalent performance (64.8% MMLU) dropped from **$20 per million tokens in November 2022 to $0.07 by October 2024**—a 280-fold reduction in 18 months via Gemini-1.5-Flash-8B. The report notes inference prices have fallen "anywhere from 9 to 900 times per year" depending on the task.

HuggingFace's repository growth provides infrastructure-level evidence of this acceleration. The platform reached **1 million public models** in September 2024 after approximately 1,000 days of growth from March 2022. The second million took only **335 days**—a 65% acceleration. By August 2025, models added that year exceeded the entire 2024 total, with **1,000-2,000 new models uploaded daily**. Platform statistics now show 2+ million models, 500,000+ datasets, 1 million+ Spaces, and 113.5 million monthly downloads.

## Hybrid architectures deliver 85-98% cost reduction with maintained quality

FrugalGPT (Stanford, May 2023) established the cascade routing paradigm, achieving **up to 98% cost reduction** on the HEADLINES financial news dataset while matching GPT-4 performance—or improving accuracy by 4% at equivalent cost. The methodology routes queries through cheaper models (GPT-J, J1-L) first, escalating to GPT-4 only when confidence thresholds aren't met. The paper's three optimization strategies—prompt adaptation, LLM approximation via caching, and LLM cascade—have spawned an extensive derivative literature.

RouteLLM (UC Berkeley, June 2024) advances this with learned routing using human preference data. Testing four router architectures—similarity-weighted ranking, matrix factorization, BERT classifier, and causal LLM classifier—the system achieves **over 85% cost reduction on MT-Bench** while maintaining 95% of GPT-4 quality. On MMLU and GSM8K, cost reductions of 45% and 35% respectively were achieved. The open-source implementation outperforms commercial routing services (Unify AI, NotDiamond) while being more than 40% cheaper.

Speculative decoding has emerged as a complementary acceleration technique. The original Google paper (arXiv:2211.17192, ICML 2023) demonstrated 2-3x speedup on T5-XXL using smaller draft models. **EAGLE** (arXiv:2401.15077, ICML 2024) achieves **2.7x-3.5x latency speedup** on LLaMA2-Chat 70B by extrapolating second-to-top-layer feature vectors rather than tokens, with EAGLE-3 (NeurIPS 2025) extending this to 3.0x-6.5x. **Medusa** (arXiv:2401.10774) eliminates the need for a separate draft model by adding extra decoding heads, achieving 2.2-3.6x speedup. **Lookahead Decoding** (arXiv:2402.02057, ICML 2024) uses Jacobi iteration for parallel n-gram generation without any draft model, delivering 1.5x-2.3x speedup on single GPU.

Apple Intelligence architecture exemplifies production hybrid deployment. The system uses a **~3B parameter on-device model** optimized for Apple Silicon with 2-bit quantization-aware training and KV-cache sharing. Complex requests route to Private Cloud Compute running larger models on Apple Silicon servers with cryptographic attestation ensuring data never persists. The AXLearn training framework underlying both is open-sourced.

Semantic caching provides another cost optimization layer. GPTCache achieves **2-10x speedup** when cache is hit using embedding-based similarity search. Academic analysis documents cache hit rates of **61.6-68.8%** with positive hit rates exceeding 97%, reducing API calls by up to 68.8%.

## Domain-specific distillation achieves frontier-matching performance at 10-20x efficiency

Code generation demonstrates the most dramatic distillation results. **DeepSeek-Coder-V2-Instruct** achieves **90.2% on HumanEval**—matching GPT-4o's 91.0%—while DeepSeek-Coder-7B matches CodeLlama-34B, representing 5x parameter efficiency. The efficiency claim extends further: DeepSeek's documentation states that "DeepSeek-Coder-Base-7B reaches the performance of CodeLlama-34B."

**Qwen2.5-Coder-32B-Instruct** has achieved "SOTA open-source code model" status with "code capabilities matching GPT-4o" according to Alibaba's technical reports. The 7B variant achieves **84.8% on HumanEval** while outperforming DeepSeek-Coder-33B-Base across five metrics. **StarCoder2-15B** matches CodeLlama-34B while StarCoder2-3B outperforms the 15B predecessor—a 5x efficiency gain between model generations.

Speech processing distillation shows similar patterns. **Distil-Whisper** (arXiv:2311.00430) achieves **6x faster inference** with 49% fewer parameters while remaining within 1% WER of Whisper-large-v3 on out-of-distribution test sets. The distil-large-v3 variant (0.8B parameters) actually outperforms the full model by 0.1% WER on long-form audio due to reduced hallucinations.

Translation models demonstrate the most extreme efficiency gains. Tencent's **Hunyuan-MT-7B** (September 2025, not December as initially reported) achieved 1st place on WMT25 in **30 of 31 language categories**, surpassing Tower-Plus-72B by 10-58% and outperforming Google Translate by 15-65% depending on language pair. This represents a 10x parameter efficiency achievement for production-grade translation.

## Regulatory frameworks are accelerating edge deployment drivers

The **EU AI Act (Regulation 2024/1689)**, published July 12, 2024, with full application beginning August 2, 2026, creates significant compliance incentives for edge deployment. The risk-based classification system—minimal, limited, high-risk, and prohibited—combined with documentation and transparency requirements is substantially easier to satisfy when data processing occurs on-device. Article 6 high-risk classifications, applying to AI in critical infrastructure, education, employment, and law enforcement, carry specific data governance requirements that edge processing simplifies.

**GDPR Chapter V (Articles 44-50)** establishing international transfer requirements creates a direct compliance benefit for edge architectures. Article 46's "appropriate safeguards" requirements (Standard Contractual Clauses, Binding Corporate Rules) and Article 47's certification pathways become unnecessary when personal data never leaves the device. This is particularly relevant for China's **Personal Information Protection Law (PIPL)**, which mandates CAC Security Assessment for transfers involving over 1 million individuals' data or Critical Information Infrastructure Operators—requirements edge processing bypasses entirely.

The **NIST AI Risk Management Framework (AI RMF 1.0)**, released January 2023, provides voluntary but influential guidance. Its four core functions (GOVERN, MAP, MEASURE, MANAGE) and seven trustworthy AI characteristics (valid/reliable, safe, secure/resilient, accountable/transparent, explainable/interpretable, privacy-enhanced, fair) align naturally with edge deployment's reduced attack surface and data minimization properties.

Economic analysis supports rapid payback for edge investment. Anyscale's batch inference benchmarks document **2.9x cost advantage** versus AWS Bedrock, extending to 6x with shared prefix optimization. Academic analysis of 54 deployment scenarios found small model self-hosting breaks even in under 3 months. Industry guidance suggests the threshold occurs at approximately **2 million tokens per day** or where strict compliance requirements (HIPAA, PCI-DSS) mandate data residency.

## Open-source ecosystem velocity has reached escape velocity

**QLoRA** (arXiv:2305.14314, NeurIPS 2023) fundamentally democratized fine-tuning by enabling **65B parameter model training on a single 48GB GPU** while preserving 16-bit task performance. The technique reduces trainable parameters by 10,000x and GPU memory requirements by 3x through 4-bit NormalFloat quantization, Double Quantization (saving ~3GB on 65B models), and Paged Optimizers. The paper itself fine-tuned over 1,000 models across 8 instruction datasets, with the "Guanaco" model achieving 99.3% of ChatGPT performance on the Vicuna benchmark after just 24 hours of single-GPU training.

HuggingFace's PEFT library now hosts **78,801+ models** implementing LoRA, QLoRA, Prefix Tuning, IA3, and other parameter-efficient methods. The ecosystem velocity is extraordinary: analysis of derivative models shows **90,000+ Qwen derivatives** on HuggingFace—surpassing Llama series to rank first globally. The December 2024 Hugging Face Open LLM Leaderboard analysis found "all of the top ten open-source large models are derivative models trained based on Alibaba's Tongyi Qwen open-source model."

GitHub's 2024 Octoverse report documents **98% year-over-year growth** in generative AI projects with 59% increase in contributions. Python surpassed JavaScript as the top language, with 2.6 million Python contributors (+48% YoY). Jupyter Notebook usage increased 92% (170% since 2022). The 2025 report shows **180 million+ developers** on GitHub with 230 new repositories created per minute, nearly 1 billion commits annually (+25.1% YoY), and 43.2 million pull requests merged monthly.

License analysis reveals Apache 2.0 as the dominant framework at **42% of HuggingFace models with license information**, followed by MIT at 18%. Notably, the Llama Community License represents only 2% despite Meta's market influence—reflecting the OSI's position that the license is "not open source" due to commercial use restrictions.

## Conclusion: The technical trajectory favors distributed intelligence

The evidence synthesized here establishes that edge AI is no longer a compromise architecture but an increasingly optimal deployment pattern. Model efficiency improvements have delivered 142x parameter compression while quantization preserves 98%+ of capabilities at 4-bit precision. Mobile NPUs have reached 50-59 TOPS, sufficient for real-time 7B model inference. Hybrid architectures achieve 85-98% cost reduction while maintaining quality. The frontier-to-local capability transfer lag has compressed to 4-12 months with cost reductions of 280-1,000x over 18-36 month periods.

The implications extend beyond technical architecture. Regulatory frameworks increasingly favor data-local processing. Economic break-even for self-hosting has fallen below 3 months for small models. The open-source ecosystem's 98% annual growth rate and 2,000 daily model uploads suggest the capability distribution curve will continue shifting toward edge deployment.

**The remaining question is not whether edge AI will dominate but how quickly enterprises will restructure around this technical reality.** The organizations building edge-first AI infrastructure today will establish durable competitive advantages as the cost-performance curves documented here continue their exponential trajectories.

---

## Source URLs for Chicago-Style Endnotes

### Model Efficiency Papers and Announcements
1. Microsoft Phi-1 Paper: https://arxiv.org/abs/2306.11644
2. Microsoft Phi-2 Blog: https://www.microsoft.com/en-us/research/blog/phi-2-the-surprising-power-of-small-language-models/
3. Microsoft Phi-3 Technical Report: https://arxiv.org/abs/2404.14219
4. Microsoft Phi-4 Technical Report: https://www.microsoft.com/en-us/research/uploads/prod/2024/12/P4TechReport.pdf
5. Meta LLaMA-1 Paper: https://arxiv.org/abs/2302.13971
6. Meta Llama 3 Paper: https://arxiv.org/abs/2407.21783
7. Meta Llama 3.1 Blog: https://ai.meta.com/blog/meta-llama-3-1/
8. Meta Llama 3.2 Blog: https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/
9. Qwen2.5 Blog: https://qwenlm.github.io/blog/qwen2.5-llm/
10. Qwen2.5 arXiv: https://arxiv.org/abs/2412.15115
11. Mistral 7B Announcement: https://mistral.ai/news/announcing-mistral-7b/
12. Mixtral 8x7B Announcement: https://mistral.ai/news/mixtral-of-experts
13. Mixtral Paper: https://arxiv.org/abs/2401.04088
14. Google Gemma 1 Blog: https://blog.google/technology/developers/gemma-open-models/
15. Gemma 1 Paper: https://arxiv.org/abs/2403.08295
16. Gemma 2 Blog: https://blog.google/technology/developers/google-gemma-2/
17. Gemma 2 Paper: https://arxiv.org/abs/2408.00118

### Quantization Research
18. GPTQ Paper: https://arxiv.org/abs/2210.17323
19. AWQ Paper: https://arxiv.org/abs/2306.00978
20. SqueezeLLM Paper: https://arxiv.org/abs/2306.07629
21. Red Hat 500K Evaluations Study: https://developers.redhat.com/articles/2024/10/17/we-ran-over-half-million-evaluations-quantized-llms
22. Red Hat arXiv Paper: https://arxiv.org/abs/2411.02355
23. GGUF Documentation: https://huggingface.co/docs/hub/en/gguf
24. llama.cpp GitHub: https://github.com/ggml-org/llama.cpp
25. NVIDIA Memory Optimization Guide: https://developer.nvidia.com/blog/mastering-llm-techniques-inference-optimization/

### Edge Deployment Infrastructure
26. Ollama Deployment Study: https://dev.to/realryan/ollamas-global-reach-a-look-at-deployment-trends-and-model-choices-16a4
27. Apple MLX Research: https://machinelearning.apple.com/research/exploring-llms-mlx-m5
28. Qualcomm Snapdragon 8 Elite Product Brief: https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/Snapdragon-8-Elite-Platform-Product-Brief.pdf
29. MediaTek Dimensity 9400: https://www.mediatek.com/products/smartphones/mediatek-dimensity-9400
30. Samsung Exynos 2500: https://semiconductor.samsung.com/processor/mobile-processor/exynos-2500/
31. Google LiteRT Documentation: https://ai.google.dev/edge/litert/overview
32. Google LiteRT Announcement: https://developers.googleblog.com/tensorflow-lite-is-now-litert/

### Ratchet Pattern and Cost Analysis
33. Stanford Alpaca Announcement: https://crfm.stanford.edu/2023/03/13/alpaca.html
34. Stanford HAI AI Index 2025: https://hai.stanford.edu/ai-index/2025-ai-index-report
35. Stanford HAI Full Report PDF: https://hai.stanford.edu/assets/files/hai_ai_index_report_2025.pdf
36. Epoch AI Open Models Analysis: https://epoch.ai/blog/open-models-report
37. UK AISI Frontier AI Trends Report: https://www.aisi.gov.uk/frontier-ai-trends-report
38. a16z LLMflation Analysis: https://a16z.com/llmflation-llm-inference-cost/
39. HuggingFace 1M Models Milestone: https://huggingface.co/posts/fdaudens/300554611911292
40. HuggingFace Hub v1.0 Blog: https://huggingface.co/blog/huggingface-hub-v1

### Hybrid Architecture Papers
41. FrugalGPT Paper: https://arxiv.org/abs/2305.05176
42. RouteLLM Paper: https://arxiv.org/abs/2406.18665
43. RouteLLM GitHub: https://github.com/lm-sys/RouteLLM
44. EAGLE Paper (ICML 2024): https://arxiv.org/abs/2401.15077
45. EAGLE GitHub: https://github.com/SafeAILab/EAGLE
46. Medusa Paper: https://arxiv.org/abs/2401.10774
47. Lookahead Decoding Paper: https://arxiv.org/abs/2402.02057
48. Original Speculative Decoding (Google): https://arxiv.org/abs/2211.17192
49. DeepMind Speculative Sampling: https://arxiv.org/abs/2302.01318
50. Apple Intelligence Technical Details: https://machinelearning.apple.com/research/introducing-apple-foundation-models
51. GPTCache GitHub: https://github.com/zilliztech/GPTCache

### Domain-Specific Distillation
52. DeepSeek-Coder GitHub: https://github.com/deepseek-ai/DeepSeek-Coder
53. DeepSeek-Coder-V2 Paper: https://arxiv.org/abs/2406.11931
54. Qwen2.5-Coder Blog: https://qwenlm.github.io/blog/qwen2.5-coder-family/
55. Qwen2.5-Coder Paper: https://arxiv.org/abs/2409.12186
56. Distil-Whisper Paper: https://arxiv.org/abs/2311.00430
57. Distil-Whisper GitHub: https://github.com/huggingface/distil-whisper
58. StarCoder2 Paper: https://arxiv.org/abs/2402.19173
59. WizardCoder Paper: https://arxiv.org/abs/2306.08568
60. CodeLlama Paper: https://arxiv.org/abs/2308.12950
61. Hunyuan-MT GitHub: https://github.com/Tencent-Hunyuan/Hunyuan-MT
62. Hunyuan-MT Paper: https://arxiv.org/abs/2509.05209
63. NLLB Paper: https://arxiv.org/abs/2207.04672

### Regulatory and Economic Sources
64. EU AI Act (EUR-Lex): https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng
65. GDPR (EUR-Lex): https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng
66. NIST AI RMF 1.0: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf
67. CCPA (CA DOJ): https://oag.ca.gov/privacy/ccpa
68. Anyscale Batch Inference: https://www.anyscale.com/blog/batch-llm-inference-announcement
69. Self-Hosting TCO Analysis: https://arxiv.org/html/2509.18101v1

### Open-Source Ecosystem
70. QLoRA Paper: https://arxiv.org/abs/2305.14314
71. QLoRA GitHub: https://github.com/artidoro/qlora
72. Original LoRA Paper: https://arxiv.org/abs/2106.09685
73. HuggingFace PEFT Documentation: https://huggingface.co/docs/peft/en/index
74. Qwen2.5 HuggingFace Collection: https://huggingface.co/collections/Qwen/qwen25-66e81a666513e518adb90d9e
75. GitHub Octoverse 2024: https://github.blog/news-insights/octoverse/octoverse-2024/
76. GitHub Octoverse 2025: https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/
77. HuggingFace Model Ecosystem Analysis: https://arxiv.org/html/2508.06811v1

---
**PROVENANCE & HISTORY NOTE**
- **Internal GUID:** gen_zcwebo2hb
- **Original Filename:** Edge AI Capability Trajectory 2023 - 2025 A Technical Vision.md
- **Standardized Namespace:** STRAT_Edge_AI_Capability_Trajectory_2023_2025_Technical_Vision
- **Audit Date:** 2025-12-30T17:27:08.061Z

*Note: This document was processed for an update, but no changes were made.*

---
© 2025 The Grove Foundation / Jim Calhoun. All rights reserved.