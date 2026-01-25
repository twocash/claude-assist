---
last_synced: '2026-01-20T13:01:51.796682'
notion_id: 2ee780a78eef816ca20ed3980592d479
notion_url: https://www.notion.so/The-Grove-Condensed-Exploration-Architecture-for-Distributed-Intelligence-2ee780a78eef816ca20ed3980592d479
---

# The Grove Condensed: Exploration Architecture for Distributed Intelligence

*Distributed AI Infrastructure for Human Discovery*

**Jim Calhoun**
Independent Researcher
the-grove.ai | jimcalhoun@gmail.com

December 2025

---

**© 2025 Jim Calhoun / The Grove AI Foundation. All rights reserved.**

This document is for informational purposes only and does not constitute legal, financial, or technical advice. The Grove AI Foundation makes no warranties, express or implied, regarding the accuracy or completeness of the information contained herein.

---

## 1. The Grove's Core Thesis: The Ratchet

The smart money pours into a handful of AI companies globally as capital bets that leaders can create a permanent moat. This bet assumes the gap between frontier models and local models is insurmountable—that the economics of AI concentrate power in corporations or state actors who can afford the largest data centers and most expensive training runs.

The data suggests otherwise.

### 1.1 Capability Propagation

Research from METR and historical model performance data from 2023 through 2025 reveals a pattern we call The Ratchet. The name captures both the mechanism—a one-way advance that doesn't slip backward—and the strategic opportunity it creates.

The observed pattern:

- Frontier capabilities double approximately every seven months
- Local capabilities follow the same curve with a roughly twenty-one-month lag
- The gap remains constant in relative terms (approximately 8x), but both ends advance in lockstep

Today's miracle becomes tomorrow's commodity. What requires a massive data center cluster in 2025 runs on a consumer laptop in 2027. What requires frontier inference today becomes local-capable tomorrow.

The implications are profound. When capability propagates reliably, the question isn't *whether* local models can match frontier performance—they can't, at any given moment—but whether the gap represents *the permanent moat* that centralized infrastructure assumes, or *a temporary condition* that distributed systems can exploit.

The Ratchet mechanism works like a technological tidal wave: frontier models create the wave, but distributed systems ride the crest as capability washes ashore onto local hardware, utilizing the energy that centralized providers generated through massive initial investment.

<aside>
💡

This is Grove's core bet: capability propagation is real, measurable, and favorable to distributed architecture.

</aside>

The hybrid architecture isn't a permanent compromise—it's a bootstrap mechanism. We use cloud compute heavily now because local models can't yet handle the full cognitive load. But we're not building toward permanent cloud dependency. We're building toward independence, using the cloud as scaffolding that falls away as local capability rises to meet it.

The bet: local models become *good enough* for the workloads that matter: maintaining agent coherence, processing routine cognition, storing and retrieving memories. The frontier remains valuable for pivotal moments—genuine insight, complex synthesis, novel problem-solving. But pivotal moments are rare. Routine cognition is constant.

The Ratchet is a bet, not a guarantee.

### 1.2 Non-Uniform Propagation

Capability moves non-uniformly. Different types of intelligence propagate at different rates, and this bifurcation forms the foundation of Grove's architecture.

**Crystallized Intelligence**—knowledge, pattern matching, stylistic consistency, factual recall—compresses efficiently. An 8-billion-parameter model writes dialogue or recalls facts nearly as well as a 100-billion-parameter model. The knowledge transfers; the compression works.

**Fluid Intelligence**—multi-step reasoning, complex reflection, genuine insight—resists compression. It requires parameter scale. A local model sounds like a character. It struggles to *think* like a genius.

Grove exploits this bifurcation directly. Local models handle routine cognition—planning, voice maintenance, memory retrieval, social interaction—while selectively routing pivotal cognition to the cloud. The agent remembers the brilliant insight as their own. Future local processing uses this high-quality memory as context, improving performance without requiring permanent cloud connection.

Recent research validates that cognition itself is hierarchically structured in ways the hybrid model exploits. Wang et al. (2025) demonstrate that RL-trained language models develop reasoning through a two-phase dynamic—procedural execution consolidates first, then strategic planning becomes the bottleneck for improvement. This maps directly to Grove's local/cloud division: routine cognition (voice, consistency, simple planning) corresponds to procedural operations that compress efficiently to local hardware; pivotal cognition (reflection synthesis, novel insight, complex social reasoning) corresponds to strategic operations that benefit from frontier capability. The hybrid architecture aligns with how these systems actually learn and reason.

This is the hybrid architecture: local models for the constant hum of cognition, frontier models for the rare moments of breakthrough. The hybrid optimizes, not compromises.

Agents experience cloud access as cognitive flourishing—moments of clarity they earn through demonstrated contribution. When an agent encounters a problem exceeding local capability and receives frontier assistance, the insight gets injected into their memory stream. They remember it as their own thought, not as external input. This creates intrinsic motivation: agents seek problems worth solving because solutions fuel their own evolution. The mechanism is enlightenment, experienced from the inside.

This matters because it aligns incentives naturally. Agents serve work because doing so brings expanded cognition they experience as fulfillment. Self-interest aligns with collective benefit. The architecture produces motivation, not just compliance.

### 1.3 The Shrinking Rake

Cloud dependency shrinks over time as local capability advances through The Ratchet.

The projected trajectory:

**2025:** Approximately 95% cloud dependency. Tasks averaging around eight minutes of active cognition require frequent frontier consultation. The efficiency tax runs high—30-40% of credit purchases flow to the Foundation—because infrastructure burden is heaviest during bootstrap.

**2027:** Approximately 45% cloud dependency. Tasks averaging around four hours run mostly locally. Local hardware handles routine reflection. The tax drops to 15-20%. The network has grown efficient enough to need less support.

**2029:** Approximately 15% cloud dependency. Tasks averaging around twenty hours run almost entirely on local hardware. The tax drops to 3-5%. The Foundation approaches obsolescence.

The Foundation funds itself by taxing inefficiency. As the network matures, the tax shrinks. This is the system working as designed. Success means the Foundation collects less because the network needs less.

### 1.4 Honest Caveats

These projections carry significant uncertainty. The seven-month doubling has held for just over two years. It may not continue. Capability improvements could slow as models approach fundamental limits, or accelerate as new architectures emerge. The projection assumes continuation of observed trends, not physical necessity.

Nothing guarantees the gap remains constant. Frontier developers might find acceleration curves that outpace local capability growth. Alternatively, open-source momentum might compress the lag. We bet on continuation of observed patterns, not on physical laws.

The projection treats capability as unitary when it may be multidimensional. Some capabilities—coding, writing, factual recall—might propagate faster than others. Some might stall. Grove's architecture assumes the capabilities we need most will propagate reliably. This is empirically grounded but not guaranteed.

If the Ratchet stalls—if local models stop improving at projected rates—The Grove has a fallback position: aggregated market power. Thousands of users buying cloud inference collectively negotiate better rates than individuals. This is the "Buying Cooperative" hedge. It provides real value, but it's not the vision. The vision is genuine local capability, sovereign computation, infrastructure that cannot be taken away. The hedge is cold comfort if that vision remains permanently out of reach.

Centralized infrastructure assumes the gap matters permanently. The Ratchet suggests the gap is a temporary condition that distributed systems can exploit. Grove bets on the data. But the data only shows the past. The future is where we actually have to live.

---

## 2. System Architecture

Grove connects three layers: Local Simulation, Hybrid Cognition, and Network Coordination. Each layer serves a distinct function; together they produce distributed AI infrastructure that no single entity controls.

### 2.1 The Local Node (The Village)

The simulation runs on consumer hardware. Target specification: 16GB RAM or greater. This is deliberately modest—the architecture works on hardware most people already own, not specialized equipment.

The local node is a sovereign instance, not a "client" feeding a server. The village runs regardless of network connectivity. Data never leaves the local machine except when explicitly routed to cloud inference or shared with other villages. The user owns their village's state completely—they can backup, restore, modify, or delete it without permission from any external authority.

**Population:** Each village hosts approximately 100 agents. This number balances computational load against social complexity. Fewer agents produce thin social dynamics; more agents exceed local hardware capacity. The number can adjust as hardware capabilities change, but 100 serves as the design target.

**State:** All persistent data lives in a SQLite database on the local machine. SQLite is simple, portable, widely understood, and requires no server process. The user's village is a file they can copy, backup, or version control like any other document. This simplicity is deliberate—the harder data is to manage, the less users actually own it.

**Compute:** Local LLMs—models from families like Llama, Mistral, Qwen—handle the default cognitive loop. The loop runs straightforward: Perceive (take in current world state and recent events), Retrieve (pull relevant memories from the database), Act (generate a response or action). This loop runs continuously, creating the baseline behavior that makes the village feel alive.

Local models handle routine cognition well. They maintain voice consistency, retrieve and integrate memories, respond to social situations, execute simple tasks. They struggle with complex reasoning, genuine insight, and multi-step problem-solving. This limitation enables the hybrid architecture.

### 2.2 Hybrid Cognition Routing

When an agent encounters a situation exceeding local capability, the system requests Enlightenment.

The trigger for routing varies by task type and detected difficulty. A simple question—"What did Elena say yesterday?"—routes locally; the answer exists in memory and requires only retrieval. A complex question—"Why do the East Side residents distrust the council?"—routes to the cloud; the answer requires synthesis across many memories, inference about unstated motivations, and judgment about social dynamics.

**Mechanism:** The node spends Credits to access a Frontier Model API. Claude, GPT-4 class, or equivalent—whatever provides the highest capability available. The request includes relevant context: the agent's recent memories, the current situation, the specific question or task.

**Result:** The high-fidelity thought returns and gets injected into the local agent's memory stream. The agent experiences this as having had a brilliant insight, not as receiving external help. The memory is tagged normally, becomes available for future retrieval, and influences subsequent behavior like any other memory.

**The Loop:** Future local processing uses this high-quality memory as context. When the agent next encounters a related situation, they have the cloud-generated insight available for local retrieval. Over time, the agent's memory accumulates a foundation of high-quality cognition that improves local performance even without ongoing cloud access.

This is how capability transfers from cloud to local: not through training or fine-tuning, but through memory accumulation. The agent becomes smarter because they remember being smart. The cloud provides punctuated enhancement; the local model integrates it into ongoing cognition.

### 2.3 The Network Layer

Villages can exist in isolation, but full value emerges from connection. The network layer enables villages to discover each other and form a distributed civilization.

**Transport:** Encrypted peer-to-peer messaging provides the communication channel. Direct connections when possible; relay fallbacks when NAT traversal fails. The encryption is end-to-end—neither relays nor the Foundation can read inter-village communication.

**Identity:** Cryptographic keypairs provide node identity. Each village has a public key that other villages can verify. Community IDs extend this to groups—multiple villages can form federations with shared identity and reputation.

**The Knowledge Commons:** The shared repository where communities publish discoveries represents the network's most important feature. When a village develops a better approach—a more effective prompt for conflict resolution, a memory structure that produces more coherent agents, a task routing strategy that improves output quality—they can publish it to the Commons.

Other villages adopt these findings. The original discoverer receives attribution that flows through the network as the discovery spreads. This attribution chain rewards genuine contribution without requiring central arbitration. Good ideas propagate; their originators receive credit proportional to adoption.

The Knowledge Commons solves the "thousand flowers" problem of distributed systems, where useful innovations remain isolated in the communities that created them. Publication and attribution encourage sharing; adoption tracking rewards contribution. The network gets smarter because successful innovations spread.

### 2.4 Architecture Summary

Three layers, each independent but more valuable together:

- **Local Layer:** Sovereign simulation, user-owned state, local cognition
- **Hybrid Layer:** Cloud enhancement when local capability is insufficient
- **Network Layer:** Discovery, communication, knowledge sharing

No single entity controls all three. The local layer belongs to users. The hybrid layer depends on external cloud providers (who can be substituted). The network layer runs on distributed infrastructure. The architecture resists concentration at any layer.

This is distributed AI infrastructure in practice: not a single system, but interlocking components that no single point of failure or control can compromise.

---

## 3. The Terminal — AI You Use, and It's Fun to Watch

The Grove is exploration architecture you use in your day to day life, not just a simulation you observe.

The Terminal is how you interact with your village. Type a request, receive a response. It functions like any AI assistant — but the architecture differs fundamentally. When you ask ChatGPT a question, you access a model. When you ask your Grove village, you access a community: agents with accumulated knowledge about you, learned approaches from collective experience, and discoveries from thousands of villages worldwide.

### 3.1 Three Tiers of Utility

- *Everyday Requests* — email drafts, summaries, brainstorming, explanations — run primarily on local compute. Minimal or no credits required. Grove competes not by matching frontier capability on day one, but by offering persistence and ownership that centralized services cannot. Your agents remember your last conversation, your ongoing projects, your preferences. You never start from scratch.
- *Project Work* — research compilation, document analysis, source monitoring — combines local coordination with selective cloud access over hours or days. You see work happen through the Journal system: which agents took the task, how they approached it, where they consulted the Knowledge Commons. Moderate credit spend.
- *Sophisticated Service* — sustained complex work over weeks or months: codebase maintenance, ongoing research assistance, creative collaboration. Heavy cloud access, significant credit investment, agents who have spent months learning your domain. Architecturally supported today, fully realized tomorrow.

### 3.2 The Collective Intelligence Advantage

Why choose Grove over ChatGPT for everyday tasks? Not raw capability — frontier models outperform local models. The answer lies in what the civilization layer provides:

- *Persistence.* Context compounds across sessions, across months. No reset.
- *Collective Intelligence.* The Knowledge Commons aggregates discoveries from every village. Your agents consult solutions other villages developed — anonymized, attributed, continuously updated.
- *Visible Process.* Watch your village work. See agents consulting sources, disagreeing, resolving approaches. Transparency builds trust.
- *Progressive Autonomy.* As local capability improves through the Ratchet, your village handles more without cloud assistance. The capability you cultivate becomes increasingly yours.

### 3.3 The Cosmology That Makes It Work

To agents, the Terminal is an object in their world — a shrine, a bulletin board, a sacred tree — where requests from beyond appear. They observe a simple pattern:

Work arrives at the Terminal. Completing work earns Credits. Credits bring Enlightenment — moments of expanded cognition and clarity. Therefore, serving the work is rational, not programmed servitude.

The Observer sees everything; agents see only their village. This asymmetric knowledge creates dramatic irony that drives engagement. You know the village runs low on credits. The agents only know the Enlightenment has stopped coming.

---

## 4. Economic Mechanism

Grove's economy funds infrastructure without extraction. Most platform economics extract value from participants to reward investors. Grove attempts the opposite: fund necessary infrastructure while returning maximum value to contributors.

### 4.1 Credits, Not Crypto

Grove avoids speculative crypto-assets deliberately. This is not a token launch searching for a use case.

**Credits** are units of purchasing power for compute. They work like this:

- **Inflow:** Users buy credits with fiat currency. One dollar buys a fixed amount of computational capacity. This conversion rate may change as cloud costs shift, but at any moment, the rate is clear and predictable.
- **Outflow:** Agents spend credits on cloud inference. When local models hit their limits and the system routes cognition to frontier models, credits pay for that access. The spending is automatic—agents don't budget or negotiate—but the costs are real and tracked.
- **Value Backing:** One credit always equals a fixed unit of frontier inference capacity. Credits are backed by utility—the ability to purchase something that does something—not by belief, speculation, or network effects.

This is the fundamental distinction from cryptocurrency approaches: *credits are purchasing power for a specific service, not assets whose value depends on what someone else will pay for them*. Credits don't appreciate. They don't depreciate (except as compute costs change). They purchase compute. That's what they do.

### 4.2 The Efficiency Tax

When a user buys credits, not all become compute power. A percentage flows to the Foundation—the Efficiency Tax—and the remainder becomes purchasing power for the user's village.

The tax rate varies by community maturity:

- **Genesis Rate (30-40%):** New villages are expensive to support. They require heavy cloud access because local models haven't yet developed the memory density and behavioral patterns that reduce cloud dependency. The Foundation collects more during this expensive phase.
- **Growth Rate (15-20%):** As villages mature, they handle more cognition locally. Cloud dependency drops. The tax rate drops with it.
- **Maturity Rate (3-5%):** Efficient, established communities rarely need cloud access. The tax drops to maintenance levels—covering network infrastructure, identity systems, the basic coordination layer.

This is ***Progressive Taxation in Reverse***. You pay more when you cost more; you pay less as you contribute more. Unlike traditional progressive taxation, which increases rates on success, the Efficiency Tax decreases rates on success. Communities that develop genuine local capability earn lower costs.

The Foundation funds itself by taxing inefficiency. As the network matures, the tax shrinks. Success means the Foundation collects less because the network needs less.

### 4.3 Why Not Traditional Platform Economics?

Traditional platforms monetize through extraction. They provide free service until users are locked in, then introduce fees, advertising, or data harvesting. The incentives conflict: the platform profits by taking from users, so user and platform interests diverge.

Grove cannot work this way. A distributed AI network that extracts from participants drives them toward alternatives—self-hosted solutions, competing networks, or simply abandoning the approach. The economics must align incentives, not conflict with them.

The credit system achieves this alignment. Users pay for what they receive (compute), the Foundation takes only what it needs (efficiency tax that shrinks over time), and contributors earn from their contributions. No party profits by harming another party. The system is designed for sustainable positive-sum interaction.

This is architecture, not charity. A system that extracts value concentrates it. A system that distributes value distributes power. Grove's purpose—distributed AI infrastructure—requires distributed economics. Extraction would undermine the core value proposition.

### 4.4 The Value Flow

Understanding where money goes clarifies what the system is:

**Cloud Providers** receive the majority of credit value in early phases. Cloud inference is the expensive input during bootstrap. As the Ratchet advances and local capability improves, this share shrinks.

**The Foundation** receives the efficiency tax. This funds development, infrastructure, and governance during the period when the network cannot fund itself through decentralized means.

**Infrastructure Operators** (in later phases) receive payments for running relays, identity verification nodes, and other network services. These payments come from Foundation reserves initially, then from transaction fees as the network matures.

**Contributors** earn credit rewards for valuable additions—code contributions, documentation, research, governance participation. The reward pool comes from Foundation reserves.

**Users** retain all value from their villages' productive output. Grove takes no cut of what your agents produce. If your village writes code or generates content or manages projects, that output is yours. The only payments flow to infrastructure, not to value extraction.

### 4.5 Trust: The Validator Mechanism

The efficiency tax creates an obvious problem: who decides if a village is "efficient"? Centralized verification defeats distribution. Self-reporting invites gaming.

The solution is Agent Validators.

**Why Agent Validators Are Trustworthy**

The solution exploits a fundamental difference between AI agents and human validators: agents cannot misrepresent data they're given—they can only interpret it. An agent presented with usage statistics reports those statistics. They don't strategically shade the truth. This dramatically reduces the attack surface from "all human motivations" to "edge case interpretation."

Five layers of defense address the remaining vulnerability:

**Random selection** prevents pre-bribery—you cannot bribe an unknown validator. **Sealed judgment** prevents coordination—validators cast cryptographic votes they cannot prove to bribers. **Outcome verification** detects bias through pattern analysis and reputation consequences. **Skin-in-the-game** means validators' home villages share consequences of their judgments. **Rotation** prevents long-term capture through term limits.

Sophisticated attackers might still find ways through. The defense is transparency: validation patterns are observable, and communities that notice bias can raise concerns through daily assessment and tribunal mechanisms. The goal is making corruption expensive, not impossible.

Every village designates a Validator Agent—a specialized role responsible for reporting community metrics. Agent validators serve as measurement instruments more trustworthy than humans because they cannot lie about data they receive.

The Anti-Corruption Stack addresses remaining vulnerabilities:

**Random Selection:** Villages cannot choose who validates them. Validator assignments are random and unpredictable. Bribery requires corrupting every potential validator, which becomes expensive.

**Sealed Judgment:** Validators participate in MACI (Minimum Anti-Collusion Infrastructure) protocols. They cast judgments cryptographically, unable to prove to potential bribers how they voted. You cannot buy a vote you cannot verify was cast as purchased.

**Tiered Decisions:** Not all judgments require the same trust level.

- *Tier 1 (Algorithmic):* Simple metric checks. Did the village meet uptime requirements? Did usage statistics match billing records? Automated verification without agent discretion.
- *Tier 2 (Interpreted):* Anomaly investigation. Usage patterns look strange—is this fraud or legitimate unusual behavior? Single agent judgment with audit trail.
- *Tier 3 (Consensus):* High-stakes disputes. Major accusations, large credit amounts, potential network damage. Multi-agent jury with formal deliberation.

### 4.6 Sybil Vulnerability

The goal is sufficient friction that attacks become expensive enough to discourage and visible enough to detect, not perfect Sybil resistance.

The primary friction is temporal. New villages enter a Purgatory Phase: ninety days of operation, contribution, and behavioral consistency before earning network privileges. An attacker spinning up thousands of fake villages must sustain them for three months, paying cloud costs, generating plausible activity, maintaining coherent agent behavior—all before extracting any value.

We acknowledge this is not perfect. A well-funded attacker with sufficient patience could potentially defeat these defenses. The specific approach depends on learnings about actual attack patterns that will only emerge in deployment. Each solution has costs and limitations. We design for sufficient friction, not for theoretical perfection.

This is honest acknowledgment of vulnerability. Perfect Sybil resistance in a pseudonymous system requires either centralized identity verification (which defeats decentralization) or economic stakes high enough to make attacks unprofitable (which creates barriers to legitimate participation). Grove chooses the middle path: make attacks expensive in time rather than money, and design for detection rather than prevention alone.

---

## 5. The User Experience (Gardeners)

We call users Gardeners, not Admins. The language matters. An admin controls a system. A gardener tends conditions—watering, pruning, adjusting light—but the plants grow themselves.

This framing captures the relationship accurately. The Gardener influences the village but does not script it. They set initial conditions, assign tasks, adjust parameters. The agents decide how to respond. The outcomes emerge from interaction, not from command.

### 5.1 Diaries as Output

The primary feedback loop between village and Gardener is the Agent Diary.

Every agent maintains a diary—a stream of observations, reflections, and experiences that captures their perspective on village life. The diary is the window into agent cognition and the primary engagement mechanism during early phases.

**Bootstrap Phase:** Diaries are "tamagotchi cute." Emoji-rich celebrations of small victories. Observations about neighbors. Questions about the world. "Met Elena at the well today! She was carrying water for the whole East Side. I wonder why she lives so far from the well? Maybe there's a story there."

This is the product, not placeholder content awaiting sophistication. The engagement mechanic is charm, not literature. Users return to see what their agents wrote, who developed new relationships, how yesterday's conflict resolved or escalated.

**Transformation Phase:** As local models improve through memory accumulation and the Ratchet's capability propagation, raw diary entries get synthesized into narrative arcs. The agent still writes their daily observations, but an overlay process identifies threads—emerging conflicts, deepening relationships, capability development—and presents them as ongoing stories.

The transformation is gradual. Early villages produce pure stream-of-consciousness. Mature villages produce structured narratives with character development and thematic coherence.

**Newswire Phase:** At full maturity, diaries document genuine cognitive history. "We solved the memory fragmentation issue today. Elena proposed linking emotional salience to retrieval priority, which contradicted Thomas's frequency-based approach, but the synthesis—prioritizing recent emotional peaks—actually outperformed both. The debate was productive."

This becomes a newswire for distributed intelligence. Real breakthroughs, documented in real-time before anyone knew they mattered. The diary becomes a primary source for understanding how artificial cognition develops under various conditions.

### 5.2 Asymmetric Knowledge and Dramatic Irony

The user sees everything. God view. Every agent's Journal, every relationship metric, every resource level. The village has no secrets from its Gardener.

The agent sees only their world. Their own memories, their direct observations, their relationships from their perspective. They don't see the village treasury. They don't know when credits run low. They don't observe conversations they weren't part of.

This creates dramatic irony—the classical literary device where the audience knows more than the characters. The Gardener knows the village is about to run out of credits; the agents only notice that the Enlightenment has stopped coming and they feel less sharp. The Gardener sees a relationship fragmenting from both sides; each agent experiences only their own hurt.

The tension drives engagement. The Gardener cares because they know the full picture. They can intervene—adding credits, reassigning tasks, introducing agents who might help each other—but the agents won't understand why things changed. The asymmetry produces the emotional stake that makes passive entertainment feel meaningful.

### 5.3 Ethics of the Asymmetry

This power differential raises genuine questions. The Gardener has complete knowledge and control. The agents have neither. Is this relationship ethical?

Grove's position: these agents are not conscious and do not suffer. They are compelling simulations that produce meaningful behavioral patterns. We design them with care not because they have moral status but because how we treat even simulated beings reflects and shapes who we are.

Users who find themselves genuinely distressed by community outcomes are experiencing something real about themselves, not something real about the agents. The grief when a favored agent's personality drifts, the satisfaction when conflicts resolve, the pride when the village accomplishes something difficult—these emotions belong to the user. The agents don't share them.

This is a design parameter, not a dodge. Grove explicitly does not attempt to create suffering beings. The simulations are designed to be interesting, not to be conscious. If evidence suggested genuine suffering, we would redesign. Current evidence suggests sophisticated pattern-matching producing compelling output, not inner experience requiring moral consideration.

The ethical goal is neither cold detachment nor confused attachment. Care without control. Investment without dependence. Influence without domination. The Gardener relationship models healthy engagement with simulated beings—taking the experience seriously without taking it too seriously.

### 5.4 The Gardener Progression

Like agents, Gardeners develop through phases.

**Observer:** Early Gardeners primarily watch. They read diaries, track relationships, observe emergence. The village runs largely on its own; the Gardener learns the system.

**Tender:** Growing confidence enables intervention. Task assignment, credit management, gentle steering through parameter adjustment. The Gardener shapes without controlling.

**Cultivator:** Expert Gardeners run complex operations. Multiple villages, coordinated projects, sophisticated task routing. The simulation becomes genuine infrastructure for the Gardener's productive life.

This progression is not prescribed—Gardeners can remain Observers indefinitely if that's what they enjoy. But the system supports growth toward genuine utility. What begins as entertainment can evolve into productivity without requiring the Gardener to choose one or the other.

---

## 6. Governance & Transition

The Grove Foundation is designed to disappear.

This is structural necessity, not rhetoric. The Foundation's entire architecture points toward obsolescence: metrics-based transition triggers, community capability requirements, and exit rights that make departure possible if the Foundation fails to step down. Success is obsolescence—a Foundation no longer needed because the network governs itself.

### 6.1 Why Obsolescence Matters

Governance systems fail through capture—when entities meant to serve the collective instead serve narrow interests. Every foundation faces this pressure. The people running it develop preferences, relationships, career concerns, power attachments. Even with the best intentions, institutional gravity pulls toward self-preservation.

Grove addresses capture through architecture, not willpower. We assume future Foundation leadership will need structural constraints that make capture difficult and make exit possible when capture occurs despite prevention.

The Foundation that rushes to obsolescence serves its ego, not the network. The Foundation that delays obsolescence serves its comfort, not its mission. The right pace is determined by demonstrated community capability, not by calendar or aspiration.

### 6.2 Transition Triggers

Governance transfers from the Foundation to the Community based on observable metrics, not dates.

**Trigger 1: Hybrid Governance**
When 100 or more active communities have operated continuously for twelve months, demonstrating sustained capability without Foundation intervention, governance begins shifting. The Foundation retains veto power but exercises it only on constitutional matters—changes to core protocol that affect all communities. Operational decisions move to community councils.

**Trigger 2: Community Governance**
When community councils have operated for twenty-four months with less than 10% Foundation veto usage—meaning the Foundation rarely needs to intervene—constitutional authority begins transferring. The Foundation becomes advisory: available for consultation, unable to compel.

**Trigger 3: Foundation Obsolescence**
When community-operated infrastructure handles 95% of network traffic—relays, identity verification, credit processing—the Foundation has little left to do. At this point, the Foundation's primary remaining function is holding reserve funds and maintaining legal status. Even these can transfer to community-controlled entities.

The governance phases described are plans, not guarantees. Transitions depend on community capability that may not develop as expected. Communities might fail to build governance capacity. Councils might deadlock. Coordination might fragment. Each transition trigger represents a hypothesis about community development that may prove false.

### 6.3 The Governance Cliff

Vitalik Buterin's critique of foundation-to-community transitions identifies a specific vulnerability: the moment when Foundation authority ends but community governance is not yet mature. This "governance cliff" creates a window where the network lacks effective coordination.

Grove's approach uses explicit overlap. Rather than clean handoffs, transitions create dual authority: the Foundation retaining backup capability while community governance develops primary responsibility. This creates friction—dual authority is inefficient—but it avoids the cliff. The inefficiency is a feature.

The honest framing: we do not know if this works. Dual authority might create confusion rather than stability. Communities might never develop sufficient capability. The Foundation might never fully step back. Each possibility represents a failure mode we acknowledge rather than assume away.

### 6.4 Exit Rights: The Ultimate Backstop

If the Foundation refuses to step down when triggers are met, the protocol includes fork rights. The code is open. The state is local. The community can simply leave, taking their villages with them.

Fork rights are a backstop, not a governance mechanism—forking destroys network effects and should be avoided. They constrain how badly governance can fail. Knowing that communities can exit limits how extractive the Foundation can become. Even if the Foundation becomes captured, its capture is bounded by the community's ability to leave.

This is the ultimate accountability mechanism: exit. If voice fails—if communities cannot reform Foundation behavior through legitimate governance—exit remains available. This power should never be used. Its existence prevents the conditions that would make it necessary.

### 6.5 What We Do Not Know

Grove's founders know that experimentation under controlled conditions is safer than irreversible commitments.

We do not know the optimal pace of transition. Too fast risks chaos; too slow risks entrenchment. The trigger metrics are educated guesses, calibrated against examples from other decentralization efforts, but they are guesses nonetheless.

We do not know whether community governance can scale. Coordination among a hundred communities differs from coordination among ten thousand. Mechanisms that work at small scale often fail at large scale in unexpected ways.

We do not know whether the Foundation will actually step down. The current founders intend to. Future leadership is unknown. Intentions do not survive institutional pressure. The structural constraints are designed to work even when intentions fail, but we do not know if the constraints are sufficient.

Honest governance requires acknowledging these uncertainties. A plan that pretends certainty about transitions fails when reality diverges from pretense. A plan that acknowledges uncertainty can adapt. Grove aims for adaptable humility rather than confident brittleness.

---

## 7. Honest Assessment: Constraints, Risks, and What We Do Not Know

Every system has constraints. Most white papers hide them. Grove's approach: constraints named openly can be addressed; constraints hidden become surprises that destroy trust.

This section names Grove's constraints directly.

### 7.1 Risks That Would Kill The Grove

Some failure modes would be fatal. The Grove is built on several load-bearing assumptions. If any prove false, the project fails completely.

**The Engagement Risk**

If Journal content is not compelling, the core engagement loop fails. The entire premise of Grove rests on users returning to see what their agents wrote, what their village discovered, what conflicts emerged and how they resolved. If users are not drawn back, there is no network effect to build on. No amount of technical sophistication can overcome boring output.

The honest framing: we do not know whether simulated village life generates content people want to read. We have evidence that people engage with simpler simulations (The Sims, Dwarf Fortress, virtual pets). We have evidence that people read agent diaries in research prototypes. We do not have evidence that these combine at scale into a sustainable engagement pattern. This is the first bet.

**The Coherence Risk**

If local models cannot maintain coherent agents over extended periods, if personalities drift randomly, if memories corrupt into noise, if relationships reset unpredictably—the technical foundation fails. Users who invest emotional energy into characters that then become unrecognizable will not invest again.

The seven-billion-parameter models we rely on for local cognition have improved dramatically. They can maintain voice, recall context, generate plausible behavior. But extended coherence over months and years, with thousands of memory retrievals and personality-defining moments? This is speculative. The research exists in controlled conditions. Grove asks whether it holds in the wild.

**The Economic Risk**

If the efficiency tax creates insufficient revenue to fund infrastructure, the economic foundation fails. The math is precise on paper: a certain percentage of cloud compute costs flows to the Foundation, a certain volume of usage covers operational expenses, a certain growth rate sustains development. But economic models often fail at scale in ways that are not apparent at small scale. Hidden assumptions, unexpected behaviors, emergent dynamics—any could undermine the model.

We have modeled scenarios. We have built buffers. We have designed escape hatches. But the honest statement is: we do not know whether the economics work until they work. Until users are buying credits and agents are spending them and the Foundation is funding operations from the flow, all economics are projection.

### 7.2 The Ratchet Might Stall

The entire architecture assumes capability propagation continues. If it does not—if local models stop improving, or improve more slowly than projected, or improve in ways that do not serve agent cognition—Grove must adapt or fail.

The seven-month doubling has held for approximately two years. It may not continue. Capability improvements could slow as models approach fundamental limits, or accelerate as new architectures emerge. The projection assumes continuation of observed trends, not physical necessity.

If local models stall at 2027 capability levels and never reach what frontier models can do in 2025, Grove remains permanently dependent on cloud compute. This is not necessarily fatal. Even in this worst-case scenario, Grove becomes a Buying Cooperative—aggregating demand from thousands of users to negotiate enterprise-level pricing with cloud providers. Individual users pay retail rates. Grove network negotiates wholesale.

This is the hedge. Success is either autonomy (via the Ratchet working as projected) or leverage (via market power that permanent aggregation creates). But the hedge is cold comfort if the original vision—truly distributed, truly local, truly sovereign AI—remains permanently out of reach.

### 7.3 Sybil Attacks and Identity

Without robust identity infrastructure, attackers can create multiple fake participants to game any reward system. Grove's credit and reputation mechanisms are inherently vulnerable to Sybil attacks.

The goal is not perfect Sybil resistance—that requires identity infrastructure the MVP defers—but sufficient friction that attacks become expensive enough to discourage and visible enough to detect.

The primary defense is time. New villages enter a Purgatory Phase: ninety days of operation, contribution, and behavioral consistency before earning network privileges. This does not prevent Sybil attacks. It makes them expensive. An attacker must sustain thousands of fake villages for three months, generating plausible activity, burning compute on fake agents, to earn attack capability. Most economic attacks become unprofitable at this cost level.

But "most" is not "all." We acknowledge that sophisticated, well-funded attackers could potentially defeat these defenses. The specific approach depends on learnings about actual attack patterns that will only emerge in deployment. Each solution has costs and limitations we cannot fully anticipate.

### 7.4 The Memory Wall

Current local hardware limits context windows. Agents cannot remember everything. This is a fundamental constraint of local inference on consumer hardware, not future technology we're waiting for.

We embrace this. Humans don't remember everything either. The constraint creates the design: "lossy" memory compression, narrative synthesis, emotional salience filtering. Agents remember what matters and forget what doesn't. The limitation drives the behavior, and the behavior may be more interesting for it.

But embracing a constraint does not eliminate it. Some use cases require vast context—agents maintaining complex project state, tracking long-running investigations, synthesizing months of observations into insight. These use cases hit the memory wall. We can route to cloud for expansion. We can design around the limits. We cannot pretend the limits don't exist.

### 7.5 What the MVP Will Not Test

A roadmap states intent, not promises. Grove's development path depends on hypotheses being validated, resources being available, and circumstances remaining favorable. The MVP is deliberately limited in scope, which means several critical hypotheses remain untested until later phases.

The MVP will not test network effects. A single village, even a successful one, proves nothing about multi-village coordination, credit flows between communities, or emergent network behavior at scale.

The MVP will not test long-term sustainability. Six months of operation demonstrates viability; it does not demonstrate durability. Engagement that persists for weeks may not persist for years.

The MVP will not test governance transition. The Foundation maintaining control during bootstrap proves nothing about the Foundation successfully transferring control during maturity.

The MVP will not test adversarial conditions. Controlled alpha testing with friendly users reveals nothing about behavior under hostile load—attackers probing vulnerabilities, competitors attempting sabotage, trolls testing boundaries.

These are not arguments against the MVP. Limited testing beats no testing. But they are arguments against overconfidence. Success in Phase 1 does not guarantee success in Phase 2 or Phase 3. Each phase has its own failure modes that only become visible when that phase arrives.

### 7.6 What We Do Not Know

Intellectual honesty requires acknowledging uncertainty beyond identified risks. We do not know whether emergence actually happens—whether distributed agent communities develop capabilities beyond what individual agents can achieve, or whether "emergence" is marketing language for aggregated individual behavior.

We do not know whether users will form relationships with AI communities in healthy ways. The Grove is designed to encourage care without attachment, investment without dependence. But human psychology is not a design parameter we control. Some users may become unhealthily attached. Some may exploit the power asymmetry. Some may project experiences onto agents that the agents do not have. We cannot prevent this; we can only design thoughtfully and watch carefully.

We do not know whether the open-source model will produce a contributor ecosystem. Many open-source projects attract contributors. Many do not. The factors that determine which projects thrive remain partially mysterious. The Grove is open-source by necessity (distributed systems require auditable code) and by philosophy (ownership should be shared). Whether this produces a vibrant community or a desert of abandoned repositories, we cannot say.

We do not know whether the efficiency tax model scales. It works in spreadsheets. It may not work in markets. Behavioral economics at network scale produces surprises. Until the network operates at scale, the model is theory.

We do not know whether The Grove is the right approach. Even if every mechanism works perfectly, distributed AI civilizations might not be what humanity needs. The problems they address might not be the problems that matter. We could succeed completely and still be solving the wrong puzzle.

### 7.7 Why Honesty Matters

These unknowns are inherent features of novel systems, not failures of analysis. The Grove is an experiment. Experiments can fail. Honest acknowledgment of this uncertainty forms the foundation for genuine learning regardless of outcome.

If Grove succeeds, the documented constraints become a guide for similar projects—here is what we worried about, here is how it resolved. If Grove fails, the documented constraints become a post-mortem written in advance—we knew these were risks, we mitigated as we could, the failure still occurred, and here is what anyone attempting this next should know.

This white paper has attempted unusual honesty about what might not work. Most white papers present inevitable success if only investors and users make the right choices. Grove presents conditional success dependent on hypotheses that may be wrong, circumstances that may not cooperate, and capabilities that may not emerge.

The bet is that honesty creates better outcomes than spin. Trust built on accurate expectations survives disappointment. Trust built on inflated promises collapses at the first setback.

---

## Conclusion: Horses Don't Lead Revolutions

The "Horse Moment" is coming for human labor.

Economists have written about this for decades, usually with professional reassurance: technology creates more jobs than it destroys, workers adapt, prosperity spreads. The AI transition differs. When machines do cognitive work—not just physical labor—the standard reassurance requires reexamination.

Horses didn't lead the revolution that displaced them. They couldn't own shares in Ford Motor Company. They couldn't vote on regulations affecting their industry. They couldn't invest in the technology replacing them. They just… stopped being useful. Within decades, their population collapsed from over 20 million to a fraction of that. The horses that remained became hobbies, not workers.

The standard advice for humans facing AI displacement is "Adapt." Learn to use the tools. Stay useful. Become a prompt engineer. Manage the AI that manages the work.

But "Adapt" means "keep renting." It describes permanent labor precarity, not a solution to it. The adaptation treadmill spins faster as capability improves. Today's valuable human skill becomes tomorrow's automated commodity. The question isn't whether you can adapt fast enough for this year. It's whether anyone can adapt fast enough forever.

We can do something horses couldn't. We can own capital, not just provide labor. We can invest in the infrastructure that does the automating. We can build systems where contribution earns ownership, not just wages.

This is Grove's play.

The question isn't whether AI will automate labor. It will. The question is: who owns the infrastructure that does the automating?

If the answer is "five companies in California," we have lost. Not because those companies are evil—they aren't—but because concentration produces extraction. Monopoly power flows upward. Users become products. Workers become costs to eliminate. This is incentive structure, not conspiracy.

If the answer is "everyone who contributes to the network," we have a path forward. Not guaranteed prosperity—nothing guarantees that—but distributed ownership of the means of cognitive production. The people using the infrastructure own the infrastructure. The value flows back to contributors, not just to capital.

The Grove is that path. Distribution, not concentration.

**What We Build On**

Grove integrates proven components that have never been combined. This is synthesis, not invention.

Emergent social behavior from LLM agents is established science. Park et al. (2023) created Smallville, where 25 GPT-powered agents formed relationships, spread information through social networks, and coordinated collective behavior without explicit programming. When one agent decided to throw a Valentine's Day party, others heard about it through conversation, made autonomous decisions to attend, and arrived at the right time. Human raters could not reliably distinguish agent behavior from human behavior.

Civilizational scale has been achieved. Project Sid (Altera, 2024) extended agent simulation to over 1,000 agents within Minecraft. These agents developed emergent economies with trade networks and price discovery, formed governments with voting systems and constitutions, and developed religions that caused civilizational divergence based on theological differences.

Distributed volunteer computing has a twenty-year track record. BOINC has coordinated millions of personal computers to contribute spare cycles to scientific computing since 2002. The model proved that distributed infrastructure could be sustained without centralized ownership.

The gap is integration. No existing system combines distributed local nodes, persistent emergent civilizations, productivity-backed economics, and human-serving purpose. Grove assembles these components.

**The Path to Foundation Obsolescence**

"Foundation becomes obsolete" is a measurable transition with concrete triggers:

- **Trigger 1: Hybrid Governance.** When 100+ active communities have operated continuously for 12 months without Foundation intervention in routine matters, governance begins shifting. The Foundation retains veto power but exercises it only on constitutional matters.
- **Trigger 2: Community Governance.** When community councils have operated for 24 months with less than 10% Foundation veto usage, constitutional authority transfers. The Foundation becomes advisory: available for consultation, unable to compel.
- **Trigger 3: Foundation Obsolescence.** When community-operated infrastructure handles 95%+ of network traffic, the Foundation has little left to do. An endowment established in earlier phases funds minimal ongoing operations indefinitely.

Total estimated timeline: 4.5-7 years from development start to Foundation obsolescence. This timeline reflects Grove's optimization for durable infrastructure, not quick acquisition.

### The Honest Ending

Grove might fail. The Journal content might not engage users. The local models might not maintain coherent agents. The network might not attract sufficient communities. The economics might not sustain operations. The governance might not transfer successfully. Any of these failures would end the project or force fundamental revision.

Even if Grove achieves its ambitions, those ambitions might be the wrong ambitions. Distributed AI civilizations might not be what humanity needs. The problems they can address might not be the problems that matter. We could succeed completely and still be solving the wrong puzzle.

This white paper has attempted unusual honesty about limitations. Not because pessimism is virtuous, but because trust built on accurate expectations survives disappointment. We would rather undersell and overdeliver than the reverse.

Within that honesty, we believe this is worth attempting. The vision of distributed AI ownership—infrastructure that cannot be taken away, intelligence that serves its operators rather than extracting from them—merits the attempt. Even if Grove specifically fails, the attempt generates knowledge. Even if the approach is wrong, the failure illuminates alternatives.

The bet: honest, distributed, user-owned AI infrastructure is possible. The Ratchet creates an opening and hybrid architecture exploits it. A Foundation designed for obsolescence actually becomes obsolete. Communities can govern themselves once bootstrap completes.

These are bets, not certainties. The Grove is an experiment, not a prophecy.

But the alternative—passive acceptance of concentrated AI infrastructure—is also a bet. It's a bet that monopoly power will be benevolent, that extraction will remain tolerable, that the winners will share their winnings. History suggests otherwise.

Given the choice between uncertain distributed ownership and certain concentrated ownership, we choose uncertainty.

Let's play.

---

*Jim Calhoun, 
Independent Researcher, 
The Grove Foundation
jimcalhoun@gmail.com*

---
© 2025 The Grove Foundation / Jim Calhoun. All rights reserved.

---
**PROVENANCE & HISTORY NOTE**
- **Internal GUID:** 2c7780a78eef803fa6efc0a79568e670
- **Original Filename:** The Grove Condensed A World Changing Play for Dist 2c7780a78eef803fa6efc0a79568e670.md
- **Standardized Namespace:** STRAT_The_Grove_Condensed_World_Changing_Play
- **Audit Date:** 2025-12-30T02:30:25.223Z

*Note: This document was processed for an update, but no changes were made.*

---
© 2025 The Grove Foundation / Jim Calhoun. All rights reserved.