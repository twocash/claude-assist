---
author: Jim Calhoun
date: '2025-12-17'
domain: research
last_synced: '2026-01-19T22:55:55.412922'
local_file: 251217-v-research-the-training-ratchet.md--FINAL.md
notion_id: 2ed780a7-8eef-8103-ad94-ff897214dd1e
notion_url: https://www.notion.so/The-Training-Ratchet-2ed780a78eef8103ad94ff897214dd1e
status: final
title: The Training Ratchet
type: vision
---

## When Distributed AI Training Reaches Frontier Scale

*Grove Foundation Technical Research*

## Executive Summary

Distributed AI training compute has grown 600,000-fold since 2020, doubling every 2.8 months—twice as fast as centralized frontier training.¹ At current trajectories, distributed training will close the 1,000× compute gap with frontier systems by 2030-2031, fundamentally shifting who can train powerful AI models.
The strategic implications align directly with Grove's exploration architecture thesis. Universities and research institutions face a choice: depend on corporate AI gatekeepers or build sovereign infrastructure for discovery. Projects like Prime Intellect's INTELLECT-1—the first 10 billion parameter model trained across three continents by 30 independent compute providers—demonstrate that globally distributed training achieves 83-96% compute utilization despite consumer-grade internet connections.² As participation thresholds drop and algorithmic efficiency improves, edge nodes currently limited to inference will evolve into training-capable contributors, enabling epistemic independence from hyperscaler infrastructure.

## Current State: A 1,000× Gap That's Narrowing Fast

EPOCH AI's analysis confirms dramatic acceleration in distributed training capabilities. Since 2020, the largest distributed training runs have grown from approximately 10¹⁷-10¹⁸ FLOP to 6×10²³ FLOP—a 600,000× increase representing roughly 20×/year growth.¹ This substantially outpaces frontier centralized training's 5×/year growth rate over the same period.
The current compute gap tells a story of rapid convergence. In 2020, distributed training lagged frontier systems by roughly 100,000×. By late 2025, that gap has compressed to approximately 1,000×, with top distributed runs reaching ~10²³ FLOP against frontier training at ~5×10²⁶ FLOP. EPOCH calculates that if both trends persist, distributed training would reach parity in approximately 5.5 years—though they note that growth will likely decelerate as the ecosystem encounters structural ceilings.
Three mathematical models frame this trajectory:

| Model | Current Value | Projection |
|---|---|---|
| Training Compute Propagation | 2.8 months doubling (distributed) vs. 5.2 months (centralized) | Gap closes 2030-2031 at median rates |
| Participation Threshold | 24GB VRAM for meaningful contribution | 16GB viable by 2027-2028 |
| Coordination Cost | 4-17% overhead vs. centralized | Converging toward ~5% with advances |

## DiLoCo: The Algorithm That Makes Internet Training Possible

Google DeepMind's DiLoCo (Distributed Low-Communication) represents the critical algorithmic breakthrough enabling training across poorly-connected devices.³ Traditional data-parallel training requires gradient synchronization at every step, demanding 100-400 Gbit/s interconnects—impossible over the internet. DiLoCo inverts this constraint through a bi-level optimization approach.
The algorithm operates through inner and outer optimization loops. Each worker independently trains for H local steps (typically 500) using AdamW, accumulating parameter changes without any inter-worker communication. Only after completing these inner steps do workers synchronize, computing "pseudo-gradients" and performing a Nesterov momentum update on the global model.⁴ This reduces communication frequency by 500× compared to standard training.
Combined with int8 quantization of pseudo-gradients, DiLoCo achieves 400-2,000× total bandwidth reduction. Where standard data-parallel training requires 100+ Gbit/s interconnects, DiLoCo operates effectively at 1-5 Gbit/s—achievable over consumer internet connections.⁵ Recent research demonstrates that DiLoCo with M=2 workers outperforms data-parallel training for models above several billion parameters.⁶

## INTELLECT-1: Proof of Concept at Scale

Prime Intellect's INTELLECT-1 project trained a 10 billion parameter model across five countries and three continents using DiLoCo, achieving:⁷
- 83-96% compute utilization (96% US-only, 83% globally)
- Synchronization every 38-40 minutes (100 inner steps)
- All-reduce communication taking 1-7 minutes per sync
- Communication overhead of just 4-17% versus centralized baselines
This wasn't a demonstration with cherry-picked conditions. INTELLECT-1 involved 30 independent compute providers dynamically joining and leaving over 42 days, with nodes ranging from major cloud providers to individual contributors.⁸

## Participation Thresholds Are Dropping Toward Consumer Hardware

The hardware requirements for distributed training participation have begun their descent toward prosumer accessibility.⁹ Today's thresholds reveal a tiered participation landscape:
**Tier 4 (Datacenter nodes):** 8×H100 configurations remain optimal for foundation model pretraining. Cost: ~$300K+ per DGX system or $2-4/GPU-hour cloud rental.
**Tier 3 (Professional: A100/H100):** Single A100-80GB or H100 nodes enable meaningful training contribution for models up to 70B parameters. Cloud pricing: $1.49-3.90/GPU-hour.
**Tier 2 (Prosumer: RTX 4090):** The RTX 4090 with 24GB VRAM represents a critical threshold at ~$0.34/hour rental, achieving 1.7× better cost-effectiveness than A100 for single-GPU workloads.¹⁰
**Tier 1 (Consumer gaming):** Hardware with 8-16GB VRAM cannot yet contribute meaningfully to pretraining. However, INTELLECT-2 demonstrated these devices can serve as inference workers in distributed RL training, generating rollouts while more powerful nodes handle gradient computation.
The trajectory suggests 16GB consumer GPUs will become pretraining-capable by 2027-2028 as compression techniques mature and participation protocols evolve.¹⁴

## Universities Face a 1,000:1 Compute Gap

The university landscape reveals both severe structural barriers and emerging workarounds. Stanford HAI's assessment is stark: "These large foundation models have outgrown what universities can do."¹¹ While Microsoft targets 1.8 million H100 GPUs and Meta acquired 350,000, Princeton's investment of 300 H100s represents a 1,000:1 compute gap that no individual institution can bridge.¹²
The response has been collaborative infrastructure. BigScience/BLOOM demonstrated the most ambitious academic coordination to date—1,000+ researchers from 250+ institutions across 60 countries training a 176B parameter multilingual model. The $7 million in publicly-funded compute produced a model supporting 46 languages and 13 programming languages.¹³
For Grove's university partnership strategy, this dynamic is central. Distributed training infrastructure enables consortiums of institutions to achieve frontier-scale capabilities while maintaining epistemic independence from corporate gatekeepers.

## Risks That Could Break the 20×/Year Trajectory

The growth trend faces several plausible disruption scenarios. Export controls create the most immediate regulatory risk. The January 2025 "AI Diffusion Rule" established comprehensive restrictions on GPU exports to 140+ countries, subsequently revoked with replacement regulations pending.
Critical batch size constraints impose fundamental limits on data parallelism. Recent research demonstrates that optimal batch size scales with dataset size rather than model size—and beyond the critical batch size, additional data parallelism yields diminishing returns.
EPOCH's assessment: "At the current rate of growth, we won't see distributed training runs catch up to the frontier of training in scale this decade." The 20×/year growth rate is likely unsustainable; 10×/year represents a more realistic long-term trajectory. However, raw compute gap ≠ capability gap—hardware efficiency gains and algorithmic improvements may enable competitive models at lower compute scales.

## Conclusion: Distributed Training Capability Is a Ratchet That Advances

The distributed training infrastructure demonstrates characteristics parallel to Grove's inference capability propagation thesis. Capability propagates outward from frontier labs through algorithmic advances, open-source implementations, and declining participation thresholds—creating a ratchet effect where each generation of techniques enables broader participation.
The 2.8-month doubling time for distributed training compute substantially outpaces both centralized training (5.2 months) and inference efficiency gains (7 months). While the ~1,000× gap with frontier systems remains significant, the trajectory points toward meaningful convergence by decade's end.
The strategic implication for exploration architecture is clear: organizations investing in edge node infrastructure should design for eventual training capability, not just inference. The coordination mechanisms exist. The economic models are emerging. The participation thresholds are dropping. Distributed training is no longer theoretical—it is operational reality advancing on a predictable trajectory toward frontier-competitive scale.
For universities and research institutions committed to epistemic independence, the Training Ratchet represents infrastructure becoming available just as the need becomes critical.
