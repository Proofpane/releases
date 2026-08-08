> Mirror of <https://proofpane.com/proof/> · synced 2026-08-08 · the canonical, always-current version lives on proofpane.com

# Proof Index

**Proofpane** is an AI-governance layer: every AI call your team makes — coding agents, workflow platforms, direct API — is **policy-gated before execution**, hash-chained after every step, and exported as an Ed25519-signed Evidence Pack an auditor verifies offline. This page exists because a governance product should hold itself to its own standard: **claims tied to evidence, not asserted.** Every major claim below is mapped to how *you* can check it — and we label the honest verifiability tier of each, including the ones you can only see in the demo or that are still stage-gated.

Last updated 2026-07-25 · Louie.Lu@proofpane.com

VERIFY NOW · public, no account REPRODUCE · script + method provided SEE IT · recorded on camera IN THE DEMO · free, no signup PUBLISHED · honest boundary

| Claim | How to check it yourself | Tier |
|---|---|---|
| Evidence Pack is tamper-evident & verifiable offline | Download the real signed pack + the standalone verifier, run it (no network, no account), then flip one byte and watch it fail: [/evidence/sample-pack/](https://proofpane.com/evidence/sample-pack/) — or, from an allowlist-only sandbox, the [GitHub mirror](https://github.com/Proofpane/releases/tree/main/evidence) | VERIFY NOW |
| Ed25519 signature + SHA-256 hash chain | The verifier re-computes the manifest signature, all file hashes, and the whole chain — the captured PASS output and the verifier source are on the same page: [sample pack](https://proofpane.com/evidence/sample-pack/) | VERIFY NOW |
| Provenance, not just integrity — a self-consistent forgery is caught | We publish the signing key **out-of-band** from the pack; `verify_evidence_pack.py --pubkey signing-key.pem` pins it, so a pack rebuilt around a forger’s own key is rejected. Rebuild it yourself and watch it fail — plus the honest boundary (external anchoring is roadmap): [integrity vs provenance](https://proofpane.com/evidence/sample-pack/#provenance) | VERIFY NOW |
| The standard we’re judged by is public, versioned & citable | The full reference architecture (six invariants, seven planes, L1–L3 conformance ladder) is published under CC BY 4.0 at [/architecture/](https://proofpane.com/architecture/), archived at [github.com/Proofpane/architecture](https://github.com/Proofpane/architecture), and citable via DOI [10.5281/zenodo.21402331](https://doi.org/10.5281/zenodo.21402331) — a private rubric can’t back an auditability claim | VERIFY NOW |
| ~1,800 governed calls/second across three nodes, chain still valid | Download the exact k6 load-test script and run it against your own rig — method + numbers below. [proofpane-loadtest-k6.js](https://proofpane.com/proof/proofpane-loadtest-k6.js) | REPRODUCE |
| DLP redacts secrets before the model sees them | Watch five AI tools read a secret file — the AWS key comes back redacted before any model sees it: [/demos](https://proofpane.com/demos) (govern-tools walkthrough, captured live) | SEE IT |
| Policy gate denies / pauses risky actions before execution | On camera: a menu-bar tray fires an Approve/Deny checkpoint before a tool call runs — [/demos](https://proofpane.com/demos); or trigger it yourself in the [no-signup demo](https://app.proofpane.com/login?demo=1) | SEE IT |
| 335 controls across NIST AI RMF · ISO 42001 · EU AI Act · GDPR · SOC 2 | Browse the control catalogue and per-skill mappings in the demo org: [app.proofpane.com/login?demo=1](https://app.proofpane.com/login?demo=1) → Compliance | IN THE DEMO |
| Cost metered at one choke point, reconciled 1:1 vs vendor invoice | Open the usage ledger + reconciliation view in the demo org: [demo](https://app.proofpane.com/login?demo=1) → Billing / Usage | IN THE DEMO |
| Every run is a replayable audit tree with full lineage | Open any agent run in the demo org and expand the tree — each tool call, policy decision, token and dollar: [demo](https://app.proofpane.com/login?demo=1) → Agent runs | IN THE DEMO |
| Per-client coverage depth (gate+transform / gate-only / observe) | The full honest coverage matrix — including the column of what we deliberately can't reach — is on the homepage’s deep-dive and in [vs GRC & logs](https://proofpane.com/answers/proofpane-vs-grc-vs-logs/) | PUBLISHED |
| Security posture (data flow, encryption, tenant isolation, roadmap) | Plain-text, item-by-item: the current distributed macOS daemon carries public Apple signing/notarisation evidence; a private-repository tray prerelease and desktop CI build are labelled separately from anonymous public distribution; SOC 2, a third-party pen test and Windows Authenticode remain roadmap: [Trust Center](https://proofpane.com/trust/) | PUBLISHED |

**Reproduce the throughput number.** The claim is ~1,800 governed calls/second across three 16-vCPU nodes with the hash-chained audit still verify-valid under concurrent load (measured on the async-writer path, p99 ≈ 0.9 s at that rate). The script above is the exact k6 test; point it at your own deployment and target rate:

```
BASE_URL=https://your-deployment DEVICE_ID=<id> TOKEN=<device-token> \
  MODE=perf TARGET=mcp_event TARGET_RPS=1800 DURATION=80s \
  k6 run proofpane-loadtest-k6.js
```

Numbers scale with hardware; a single node holds a lower rate. We publish the ceilings and the trade-offs (latency vs throughput, the lock-convoy vs decoupled-sealer story) rather than a single hero figure — ask for the perf notes if you want the full methodology.

**Tiers we won’t pretend about.** Two claim-classes have no public artifact yet, and we say so: a **third-party penetration test** and **SOC 2 Type II** are stage-gated (see the [Trust Center](https://proofpane.com/trust/) roadmap), and there is **no customer case study** yet — we’re onboarding founding design partners. Those are the honest gaps; everything above this line, you can check today.

Found a claim on the site without a row here? Email [Louie.Lu@proofpane.com](mailto:Louie.Lu@proofpane.com) — it either gets an evidence link or gets cut.
