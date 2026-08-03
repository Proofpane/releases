> Mirror of <https://proofpane.com/thinking/who-approved-that/> · synced 2026-07-26 · the canonical, always-current version lives on proofpane.com

[THINKING](https://proofpane.com/thinking/) · 25 JULY 2026

# Who approved that?

Now that AI agents do real work beside humans, authorization and accountability have quietly become the audit question. Most of today's answers fail it.

**Louie Lu** · Founder, Proofpane · Auckland![ProofKey concept preview — a customer-held USB-C authorization device with trusted display, physical confirm and cancel buttons, secure element, and the seven-step approval flow into Proofpane's hash-chained evidence log](https://proofpane.com/thinking/who-approved-that/img/proofkey-concept.webp)**ProofKey × Proofpane: designed as a pair.** Proofpane software defines and enforces policy and records tamper-evident evidence; ProofKey, a customer-held hardware root, protects the authority to change the rules. Software and hardware, one cryptographic chain of governance: every approval independently verifiable offline. Concept preview only, subject to change; industrial design and final form factor will vary with the OEM and secure-element supplier. *Click any image to enlarge.*

The composition of work changed faster than the paperwork did.

Two years ago, "the team" meant people. Today almost every knowledge task has AI in the loop: drafting the contract, triaging the inbox, reconciling the invoices, pushing the fix. The org chart still says forty employees. The activity log tells the truth: forty humans and a few hundred agent identities, acting around the clock.

Most of that is good news. Here's the part that isn't settled: **when humans and AI produce work together, authorization and accountability stop being obvious.** And unlike most unsettled questions, this one has a deadline, because it gets asked, retroactively, by people with checklists: auditors, regulators, insurers, incident reviewers, courts.

- The agent issued the refund. Who approved it?
- The agent "fixed" the source data so validation would pass. Who authorized that?
- The model's summary was wrong and a customer relied on it. Which human signed off, and what exactly were they looking at when they did?

"An AI did it" has no standing anywhere that matters. Accountability always lands on a person. The only question is whether your systems can show *which* person, *what* they authorized, and *what they saw* when they authorized it.

## Why today's answers fail the audit

**Logs record what happened, not who meant it.** Every platform has an activity trail. Almost none can distinguish "a human with authority deliberately approved this specific action" from "a request arrived from a session bearing this human's cookies." Those are different facts, and after an incident they're the only fact that matters: stolen sessions, over-privileged service accounts and rubber-stamp fatigue all collapse the first into the second.

**Blanket delegation isn't authorization.** "The agent is allowed to handle refunds" is a policy. It is not an answer to "who approved *this* refund, of *this* amount, to *this* customer." When the delegation chain runs human → agent → action, accountability needs per-action anchors somewhere in that chain, or every incident review ends in a shrug.

**And the vendor's word isn't evidence.** If the only proof of an approval lives inside the vendor's own database, the audit answer amounts to "the system being audited says it's fine." That includes your cloud's built-in approval workflows: an approval that exists only in the platform's own logs is the audited system grading itself. Evidence that matters has to be verifiable by a third party who trusts neither the vendor nor the platform: offline, after the fact, years later if needed.

## Approvals that scale: the frequency law

The failure mode on the other side is just as real: drown people in confirmation dialogs and they will click yes to everything. Accountability theatre. The design rule I keep coming back to:

Assurance should scale with blast radius divided by frequency.

Frequent actions must stay light or people stop reading them. Catastrophic actions must be rare enough that a deliberate ritual is affordable. Mapped onto how organizations actually operate:

| How often | Typical actions | Right level | Why this level |
|---|---|---|---|
(The assurance ladder is numbered R1-R4; editions of this page before 2026-08-03 numbered the same ladder L1-L4.)

| Many times a day | Release a paused agent action · accept a redaction · approve one step of a workflow | R1 Software confirmation | Blast radius is small and reversible. Added friction here doesn't add safety; it trains the reflex to click yes. |
| A few times a month | Activate a policy version · change a model or provider · register a governed device · export evidence externally · elevate a role | R2 Hardware-backed approval | These change the rules for everything downstream. Each one deserves a per-action signature bound to what was on screen. Five seconds on a phone. |
| A few times a year | Create a tenant root · break-glass / disable governance · rotate root keys · recovery | R3 Dedicated-device ceremony | Catastrophic blast radius. Rarity is exactly what makes a deliberate, witnessed ceremony affordable. The device lives in a safe, not a pocket. |
| Where regulation demands | The same boundary changes, in regulated or high-impact deployments | R4 Multi-party + attestation | No single person, device or vendor should be sufficient: dual control plus an attested runtime. |

Banking arrived at this junction first, and it's worth noticing why: the industry with the most hardened infrastructure is the one that wrote *human transaction signing* into law (PSD2's dynamic linking; chipTAN's independent displays). Trusted machines didn't remove the need for provable human authorization. They made it the standard.

## The assurance ladder, level by level

The ladder only works if you're honest about what each rung proves, and what it doesn't:

|  | Level | Mechanism | Where the key lives | What it proves | What it does *not* prove |
|---|---|---|---|---|---|
| ![R1 — Proofpane desktop tray approval card: release paused agent action, Approve / Hold](https://proofpane.com/thinking/who-approved-that/img/lvl1-software.webp) | R1 Software confirm | Authenticated session + explicit click; event recorded in the audit trail | — (session credential) | The account holder's session confirmed, in the flow of work | That the person, rather than whoever holds their session, meant it |
| ![R2 — phone approval sheet: exact action summary, confirm with Face ID unlocking a device-bound key](https://proofpane.com/thinking/who-approved-that/img/lvl2-phone.webp) | R2 Hardware-backed approval | System biometrics unlock a device-bound, non-exportable key (Secure Enclave / TPM / hardware keystore); that key signs this one action, with nonce and expiry | Inside your phone or laptop's protected hardware | The key's holder authorized *this exact payload*: replay-proof, per-action | Display integrity on a compromised device: the summary is app-rendered. The biometric is the unlock, never the root |
| ![R3 — ProofKey concept device: USB-C signer with trusted display showing the exact action, physical Confirm and Cancel buttons](https://proofpane.com/thinking/who-approved-that/img/lvl3-usb.webp) | R3 Dedicated-device ceremony | A standalone signer with its own display and physical confirm/cancel; separate smartcard-class secure element (chip-level EAL5+/6+ certified parts) | Inside the dedicated device; it never leaves | An authorized human saw *this action* on an independent display and physically confirmed it | That the policy itself is wise; anything happening outside the governed surface |
| ![R4 — dual control 2-of-3: two approvers signed, one pending, executes on attested runtime](https://proofpane.com/thinking/who-approved-that/img/lvl4-multiparty.webp) | R4 Multi-party + attested execution | 2-of-3 or dual-control approval, plus runtime attestation of the executing environment | Split across independent custodians | No single actor could have fabricated the approval; the approved code ran unmodified | Provider conduct beyond the boundary; the hardware supply chain itself |

## The phone step, precisely: the biometric is the unlock, never the root

When people hear "approve it on your phone," many picture the app scanning your face or matching your voice. They're right to be suspicious of that picture, especially now. An app-managed camera or microphone flow is exactly what AI has learned to beat: synthetic faces, cloned voices, replayed clips. And even when recognition works, all it produces is a yes/no from the app: nothing that binds *you* to *this specific action*.

R2 is built the other way around:

| ✗ What R2 is not: recognition as authorization | ✓ What R2 is: a biometric-gated key signature |
|---|---|
| The app processes camera, voice or fingerprint data and decides "it's you" | The operating system's own biometric check (Face ID, Touch ID, Windows Hello, Android BiometricPrompt) runs entirely inside the platform. **The app never sees biometric data** |
| The output is a boolean "matched": it says *who*, never *what* | Success unlocks a private key that lives in the Secure Enclave / TPM / hardware keystore and **cannot be exported** |
| Beatable at a distance: a deepfaked face, a cloned voice, a replayed recording | That key signs the **exact canonical action**: target, payload hash, nonce, expiry. **The signature is the authorization**, not the face-match |
| Nothing lands in evidence except the app's word for it | The signed payload lands in the hash-chained log, verifiable offline by anyone, years later |

Two consequences worth spelling out. **Privacy:** nothing biometric is ever captured, stored or transmitted by the governance layer: no face images, no fingerprint templates, no voiceprints. The platform keeps the biometrics; the governance layer only ever sees a signature, so there is nothing biometric to breach. **And the AI-era point:** a synthetic face can beat a camera; it cannot conjure a signature from a key it does not hold. Even a fooled biometric on a stolen phone still requires *that physical phone, in hand*; remote, scaled attack has nothing to grab. And even on the day deception wins, the record it leaves is not “the AI silently did X.” It is “this person was shown exactly this, and confirmed.” Accountability survives the failure of judgment; that is the entire design goal. Voice is never an approval factor here; at most it's an accessibility aid.

**"This is just passkeys," a security veteran will say. Same silicon, same gesture, different job.** WebAuthn proved this hardware path years ago. But a passkey answers *login* ("is the account holder's device present?") once, at the start of a session; everything after that first hello rides on the session. Accountability needs the other end of the interaction: a signature over *this* action (this refund, this policy version, this export), minted at the moment of decision. Authentication opens the door; authorization signs the deed. Banking regulators drew exactly this line when PSD2 refused to accept "logged in" as approval and demanded a fresh signature dynamically linked to each transaction.

**And one fair objection deserves a straight answer:** isn't the Secure Enclave still Apple's silicon, a chip maker's root by another name? The distinction that matters is **custody versus manufacture**. The enclave vendor built the vault, but your key is generated inside *your* device, holds no copy anywhere, and signs nothing without you present. The manufacturer cannot produce your signature today, and cannot retroactively forge yesterday's. Attestation is different in kind: there the chip maker's *own* provisioned key actively signs every claim, so the vendor sits in the verification loop forever. You do still trust the safe-maker's engineering at R2. That is exactly why R3 exists: a dedicated device built around a **smartcard-class secure element**, the kind that ships with chip-level EAL5+/EAL6+ Common Criteria certification (the same tier as banking cards and passports) from a vendor *you* choose. And why R4 splits authority across devices and vendors. No layer removes trust; each layer shrinks it, diversifies it, and keeps custody with you.

**Two boundaries, stated plainly.** First: at R2, what binds "what you saw" to "what was signed" is app-level: a fully compromised phone can lie about the summary it shows. Only R3's independent display closes that gap, which is exactly why R3 exists and why it's reserved for the actions that deserve it. Second: none of this makes a bad policy good, and none of it governs activity that bypasses the agreed surface. Anyone who tells you a device solves governance is selling the device, not the governance.**Where this stands today, honestly:** Proofpane ships R1 and R2 in production: explicit human approvals in the desktop tray, and for rule-changing actions, the operator's device biometrics (Touch ID / Windows Hello) unlock a hardware-held, device-bound key that signs that exact action. Every event lands in a SHA-256 hash-chained audit log, exportable as an Ed25519-signed Evidence Pack that verifies offline. The R3 hardware key is real but early: I'm prototyping the signing flow on blank, off-the-shelf USB security keys: development hardware, not a manufactured product. The ladder above is the design framework we build against.

## The chain has to end at a root your organization holds

The machine side of trust is genuinely improving: attested execution and confidential computing can increasingly prove that approved code ran unmodified. That end of the stack is being mapped well by practitioners like [Imran Siddique](https://imransiddique.com/), creator of the Agent Governance Toolkit. But every root in those chains belongs to a chip maker or a cloud. The human side (*who had the authority, and did they really exercise it*) can't be outsourced to either.

That's the direction we're building toward at Proofpane: agents governed by policy in the middle, every event landing in a tamper-evident log a third party can verify offline, and at the top, human authority anchored to keys the customer organization itself holds. We've been sketching that top layer as **ProofKey**, the customer-held hardware root previewed at the top of this piece. It's a concept, not a product; but concepts are where standards start.

 Software defines and enforces policy.
 Hardware protects the authority to change it.
 Evidence proves what happened.
The customer holds the final key. [See governed AI in real workflows →](https://proofpane.com/use-cases/)[Verify a real Evidence Pack yourself →](https://proofpane.com/evidence/sample-pack/)Built in Aotearoa New Zealand · [Louie.Lu@proofpane.com](mailto:Louie.Lu@proofpane.com)[Thinking](https://proofpane.com/thinking/) · [Trust Center](https://proofpane.com/trust/) · [Proof Index](https://proofpane.com/proof/) · [Sample Evidence Pack](https://proofpane.com/evidence/sample-pack/) · [What is Proofpane?](https://proofpane.com/answers/what-is-proofpane/) · © 2026 Proofpane
