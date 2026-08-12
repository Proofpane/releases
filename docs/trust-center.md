> Mirror of <https://proofpane.com/trust/> · synced 2026-08-12 · the canonical, always-current version lives on proofpane.com

# Trust Center

Plain text, structured, written for security review — no marketing images. Each item is tagged `[shipped]`  or `[roadmap]`  so you always know which is which.

Last updated: 2026-08-10 · Security contact: [Louie.Lu@proofpane.com](mailto:Louie.Lu@proofpane.com) · Company stage: early (no customer deployment yet; platform collaboration and the [direct governance offer](https://proofpane.com/governance/) run in parallel — neither waits for the other) · Founder: [Louie Lu on LinkedIn](https://www.linkedin.com/in/louielunz)

## Legal entity registered

- **PROOFPANE LIMITED** — a New Zealand limited company, incorporated 3 June 2026.
- **NZ company number:** 9434021 · **NZBN:** 9429053715692
- **Registered office:** 22 Harper Street, Chatswood, Auckland 0626, New Zealand.
- **Verify independently:** the [public Companies Register record](https://app.companiesoffice.govt.nz/companies/app/ui/pages/companies/9434021) is the authority; this page only points at it. Nothing here should be taken on our word when a register will answer.

## Deployment models `[shipped]`

**Two models, and we are precise about which one has been run.** Enforcement is local in both: the daemon runs on the user's machine, and DLP redaction happens before a model ever sees the text. What differs is where the control plane and the audit chain live.

- **Self-hosted in your environment** — the server ships as Docker images and runs in your cloud or on your own hardware behind the firewall. The control plane, the database and the audit chain stay inside your boundary; **no prompts, no tool calls and no audit rows leave it**. Signed chain-head anchors are still exported, so a third party can detect deletion or substitution of history even though you hold the record. This is the model built for regulated buyers. **Honest status: the images ship and the architecture is the same product, but we have not yet run a full deployment inside a customer environment** — every measurement published on this site was taken against the hosted model below.
- **Hosted by us** — a local connector pairs to a control plane we operate; tool-layer enforcement still happens locally, and audit rows are sent to that control plane. **This is what is running today**: the public demo, and the basis for every number and test result we publish.
- **Egress gateway:** model API calls route through the gateway for policy, DLP and metering, then forward to the provider the customer configured. Available in both models.
- **Fleet enrollment (MDM), `[shipped]` 2026-08-10:** an IT admin can push the endpoint as a signed `.pkg` plus a configuration profile carrying an **org enrollment token** — machines register themselves at first launch, nobody types a code. The token is a new credential class, so its posture is stated here: stored as SHA-256 only (the plaintext is returned once at mint and never again), revocable immediately, scopable with an expiry and a use limit, and every mint / enrollment / revocation lands on the audit chain. The enrollment endpoint answers every rejection identically, so it cannot be used to probe which tokens exist. **Identity honesty:** a managed install proves nothing about who is at the keyboard, so an MDM-enrolled machine's audit rows carry the OS username *as asserted*, labelled `os_user_unverified` — never presented as a verified account, and never attributed to the admin who minted the token. Verified per-user identity arrives with IdP binding, which is deliberately built against a real customer's IdP. Runbook: [docs/deployment/mdm-fleet-deployment.md](https://github.com/lywinged/proofpane/blob/main/docs/deployment/mdm-fleet-deployment.md).
- **Hosting (our instance):** the control plane runs on Fly.io (Sydney region). The landing site is served by Cloudflare Pages. In a self-hosted deployment neither is in your path.

## Data flow — what leaves your machine `[shipped]`

- The daemon sends **audit events** (tool name, decision, timestamps, actor/account label, DLP-redacted content previews) to the control plane. DLP redaction of secrets happens **on-device, before transmission** on hook-based captures.
- Model calls made through the egress gateway carry the prompt/response bodies through the gateway **only for the calls you route through it**; bodies are DLP-scrubbed per policy before forwarding to the model provider.
- We deliberately do **not** use TLS interception. Coverage comes from official vendor hooks, MCP proxying, and the gateway — no root CA on your machines, no new attack surface. Deeper techniques (OS-level hooks, TLS MITM, sandbox wrapping) exist in the product but ship **off by default behind a double consent gate**, only for customers who mandate them.

## What our logs contain — and do not contain `[shipped]`

- **Contain:** event type, timestamps, org and account attribution, tool/skill/workflow names, policy decisions and reasons, cost/token counts, DLP-redacted previews, hash-chain fields.
- **Do not contain:** plaintext secrets caught by DLP (redacted before the model and before the chain); passwords or API keys in application logs (never-log-secrets engineering rule); page titles in usage analytics are DLP-scrubbed before recording.

## Audit-log integrity `[shipped]`

- Append-only, SHA-256 hash-chained audit log with a **database-level immutability trigger** — sealed rows cannot be updated even by the application.
- **Ed25519 chain-head anchoring:** signed anchors are exported off-box, so deletion or substitution of history is detectable even after infrastructure loss.
- **Evidence Packs** are Ed25519-signed and verify with a standalone offline CLI — your auditor needs no Proofpane account and does not have to trust our backend.
- Daily integrity cron re-verifies the chain and records the check itself on the chain.

## Encryption & key custody `[shipped]`

- Transport: TLS for all client↔cloud and gateway↔provider traffic.
- At rest: customer API keys, device tokens and email credentials are Fernet-encrypted with a dedicated encryption secret (independent from session-token secrets, so credential rotation never destroys stored secrets).
- Evidence-signing key: Ed25519 private key held server-side; the corresponding public key ships inside every Evidence Pack so verification is self-contained.
- Device pairing: short-lived pairing codes; device tokens stored hashed; revocation enforced on every authenticated call.

## Tenant isolation `[shipped]`

- Every tenant-scoped table carries an organisation id; all queries filter on it, and isolation indexes are enforced by an automated guard.
- The audit chain embeds the organisation id in each row's hash, so cross-tenant tampering is detectable, and file storage is namespaced per organisation.
- Role-based access control: owner / admin / member, with destructive operations gated to admin and above. JWT authentication; SSO (WorkOS SAML/OIDC and Google OAuth) supported.

## Retention & backups `[shipped]`

- Audit archival moves rows past a configurable retention boundary out of the hot path without breaking chain verifiability.
- Database snapshots are compressed and `[shipped]` to S3-compatible object storage with retention rotation; signed chain anchors are additionally exported off-box for disaster recovery of verifiability.

## Subprocessors (current)

- **Fly.io** — application hosting (Sydney).
- **Cloudflare** — landing-page hosting and CDN.
- **Cloudflare R2** (S3-compatible) — encrypted backups and anchor export.
- **Model providers** (Anthropic, OpenAI, Google, DeepSeek, or any OpenAI-compatible endpoint) — only for calls the customer routes through the gateway, under the customer's own keys where configured.
- **Resend / Mailgun** — outbound email, if the customer enables email features.

## Upstream work on an independent standard — the founder's own

Louie Lu's pull requests are merged into [**trace-spec**](https://github.com/agentrust-io/trace-spec) (TRACE, an open attestation standard for agentic AI governance) and its conformance-test repository — neither owned, maintained nor funded by Proofpane. What was merged: conformance vectors for receipt rules that had none, profile-cutover enforcement at verification time, RFC 8785 portable vectors, and a schema resync that fails on the next drift. Those gaps were found by applying the **load-bearing-coverage criterion** — from the founder's third paper, a mechanical test of whether a conformance suite can be passed without doing the work — to that standard, whose receipts are its first corpus — the method run against someone else's artifact, the fixes accepted by their maintainer.

This is the founder's personal contribution, not the company's. Counts are deliberately not quoted because they move on the maintainer's schedule — the [current state of every pull request](https://github.com/agentrust-io/trace-spec/pulls?q=is%3Apr+author%3Alywinged) is one query. A merged pull request accepts specific fixes; it is not an endorsement of Proofpane or a certification of it, and the criterion has still not been applied to Proofpane's own conformance suite.

## Community directory listings — recognition, not security testing

- Listed as a governance proxy for MCP in [**awesome-mcp-servers**](https://github.com/punkpeye/awesome-mcp-servers) — the main community MCP directory (third-party, community-reviewed).
- Listed as a runtime governance gateway in [**awesome-ai-agent-governance**](https://github.com/systempromptio/awesome-ai-agent-governance), alongside Datadog LLM Observability and Patronus AI.
- Listed in the Governance Frameworks section of [**awesome-ai-governance**](https://github.com/agentrust-io/awesome-ai-governance) — the directory maintained by Imran Siddique (creator of Microsoft's Agent Governance Toolkit; Chief Platform Officer at OPAQUE), merged by the maintainer.

Three independent, community-curated directories; none ours, none paid. Every listing states plainly that Proofpane is a closed-source proprietary daemon and links the CC BY 4.0 reference architecture.

## Assurance status, at a glance

**Code signing in one line:** macOS signed and Apple-notarised, Windows unsigned, Linux SHA-256 digests. Three separate rows — a summary that reports "Proofpane binaries are unsigned" has carried the Windows row over to macOS, where it does not hold.

- **Signing credential: held.** PROOFPANE LIMITED holds an Apple Developer ID Application certificate (team B94QM75QNG).
- **Current distributed daemon: signed and notarised.** Both macOS builds of daemon v1.5.24 are Developer ID-signed and Apple-notarised. The bare executable cannot carry a stapled ticket, so macOS resolves it online during assessment; the protected script installer performs that assessment before installation.
- **Public Tray release: signed, notarised and anonymously downloadable.** The universal macOS `.dmg` on [`tray-v0.3.9`](https://github.com/Proofpane/releases/releases/tag/tray-v0.3.9) is Developer ID-signed, Apple-notarised and stapled. The public release carries an adjacent SHA-256 sidecar and can be downloaded without an account.
- **Desktop CI build: verified, not presented as a public release.** A macOS desktop CI build passed Developer ID signing, notarisation and stapling checks. The canonical release record contains no post-certificate public desktop release yet.
- **Other platforms:** Windows Authenticode is outstanding; Linux releases carry published SHA-256 digests rather than a platform-signing claim.
- **External checks and signals: present.** Apple returned its own verdict on the current daemon, the public Tray v0.3.9 disk image and installer package, and a named desktop CI artifact; dependency audits use PyPA, GitHub and RustSec data; Semgrep, Bandit and gitleaks contribute independently maintained rules; community maintainers reviewed the three directory listings above.
- **Independent security assessment: not yet.** Those checks are useful, but they are not a penetration test, red team, bug bounty or review by a named assessor. The detailed boundary below is deliberate.

## External verdicts, intelligence and recognition

These are different currencies, so they stay separated: Apple controlled its own verdict; external communities maintain the advisory data and rules that our scanners consume; maintainers controlled whether to merge the directory listings. Only the first is an external check run against a named Proofpane artifact. None is an independent security assessment.

- **Apple notarisation** — the strongest item here, because Apple ran a check and returned a verdict we did not control. Both macOS binaries in the current distributed daemon v1.5.24 were accepted. The public `tray-v0.3.9` universal disk image and its MDM installer package were also accepted and stapled, and can be downloaded anonymously with its SHA-256 sidecar; a separate desktop CI build was accepted and stapled but is not presented as a public release. `spctl -a -vvv -t install` on the downloaded daemon answers `accepted / source=Notarized Developer ID`. **What it is not:** notarisation is an automated malware and code-signing-policy scan. It says Apple found no known malware and the signing meets their requirements. It is not a security review and Apple does not claim it is.
- **External vulnerability databases** — dependency auditing resolves against advisory data we do not maintain: the PyPA Advisory Database, GitHub's Advisory Database, and RustSec. On 2026-08-07 that surfaced 23 known vulnerabilities across three Python packages we were shipping — our JWT library, our multipart parser, and the MCP SDK — all three upgraded the same day. We did not find those; a database maintained by other people did.
- **External rulesets** — Semgrep's published security rules, Bandit, and gitleaks' secret patterns are written and maintained by their communities, not by us. What they look for is somebody else's judgement about what is dangerous, which is the part that makes them worth running at all.
- **Community directory review** — the three listings in the section above were reviewed and merged by maintainers with no relationship to us.

**And the honest limit on all of it: we run these, and we configure them.** We choose which rulesets, we set the baseline, and we wrote the allowlist that suppresses twelve secret-scan findings as false positives — each with its reason recorded, and every one of them checked, but checked by us. An external tool operated by the party being examined is not an external assessment, and describing it as one would be exactly the move this page exists to avoid.

What that leaves genuinely open, and what money and a customer engagement buy: **nobody has been paid or invited to attack this product.** No penetration test, no bug bounty, no red team, no security review by a named assessor. Researchers are welcome at the security contact above, and a finding will be published here whatever it says.

## Daemon security model

The obvious objection first, in our own words: **the daemon is a high-privilege security chokepoint** — it proxies MCP tool calls and can touch the filesystem and shell on the machines it governs. We treat it that way by design:

- **Protocol layer only:** a single user-space binary — no kernel extensions, no TLS interception, no browser hooks. Installing Proofpane does not add an attack surface class your security team has never certified before.
- **Credential hygiene:** pairing secrets and device tokens are encrypted at rest; device tokens rotate with a grace window, and revocation is enforced server-side — a revoked device gets 401 everywhere, immediately.
- **Capability containment:** per-agent policies constrain allowed/denied filesystem paths and shell usage, so a governed agent's blast radius is bounded by configuration, not trust.
- **Data minimisation:** DLP redaction of secrets happens on-device, before transmission.
- **Lifecycle honesty:** pairing, disconnect and per-app monitoring-off are audit events on the chain — the daemon being off is a recorded fact, not a blind spot.
- **Reviewable design:** the full reference architecture is published under CC BY 4.0 for independent scrutiny.

What design cannot substitute for: **a third-party penetration test** (roadmap below). We consider that the single most legitimate objection to installing Proofpane today, and it is scheduled against the first enterprise engagement rather than denied.

## Certifications & assurance `[roadmap]`

- **SOC 2 Type II:** not yet certified; program start is on the current company roadmap. We say this plainly rather than implying otherwise.
- **Penetration test:** no third-party pen test completed yet; planned alongside the first enterprise deployment. Security researchers are welcome at the contact above. **What we do instead, and what it is worth, is set out below** — it is not a substitute, and we would rather show you the difference than leave one sentence standing in for it.
- **Binary signing — macOS is DONE, not roadmap** (only the Windows half of this item is outstanding, which is why it still sits under this heading): **the current distributed macOS daemon is done** (v1.5.24, 2026-08-10) — both architectures are signed with the Apple Developer ID issued to PROOFPANE LIMITED and notarised by Apple. The public Proofpane Tray v0.3.9 release carries an anonymously downloadable signed, notarised and stapled universal `.dmg` with an adjacent SHA-256 sidecar. A separate desktop CI build was verified with stapled `.app`/`.dmg` artifacts but is not presented as a public release. A bare daemon executable cannot be stapled, so macOS resolves its ticket online during assessment; the protected script installer performs that assessment before installation. **Windows Authenticode is still outstanding**; Linux carries SHA-256 digests rather than a platform-signing claim.

## What we test, and what testing establishes `[shipped]`

A pen test and a test suite answer different questions. An assessor asks *what can an adversary do that you did not think of*. A suite asks *does the thing you built still do what you said*. Only the first needs somebody who does not share our blind spots, which is why it is on the `[roadmap]` above and nothing here replaces it. The second is ours to do properly, and this is what it currently covers.

**5,650 backend tests** across 464 files, plus 29 frontend suites and a Playwright end-to-end spec. Rather than a total, the useful breakdown is by the property under test:

- **Tenant isolation** (8 suites) — cross-org reads, control-plane routes, chat history, case events, custom skills. The recurring assertion is that another tenant's identifier returns **404, not their row**.
- **Authorization and policy** (27 suites) — the four-tier risk classifier against command variants (a flag between a verb and its subcommand, a binary alias, a wrapper), server-side refusal of a click-approval on an escalated request, JWT strength, revoked-device enforcement on every authenticated path.
- **DLP** (9 suites) — redaction before the model and before the chain, on the daemon (which must work with no backend reachable), the control plane, and the egress broker.
- **Audit-chain integrity** — the append-only trigger, chain verification, and a test that forbids any new code path from updating or deleting an audit row.
- **The Evidence Pack claim, tested as an auditor would meet it** — a pack is built, then verified in a **fresh virtualenv containing only `cryptography`**, with a control asserting that interpreter cannot import our application. Verifying it in our own environment would prove the tool works on our machine and nothing about "your auditor needs no Proofpane account".

**17 structural guards.** These are the unusual ones, and they exist because a fixed bug that can silently return is not fixed. Each forbids a *class* of defect rather than an instance, and each was written after that class actually bit us:

- no raw database connection outside the session layer (tenant filtering lives there)
- no raw provider call outside the metering choke point (an unmetered call is an unbilled and unaudited one)
- no `UPDATE` or `DELETE` path against the audit log
- no unconditional re-signing in an install path — added 2026-08-07, when the updater was found replacing the Developer ID signature it had just verified
- no SQL that a Postgres deployment could not run
- every public claim carries a resolvable basis; every claim about a *software* property carries a **test** basis, because a document goes on saying so after the behaviour changes
- every buildable stack has a CI job that builds it — added the same day, after pull requests touching three stacks were found running nothing and showing green

**Automated scanning** runs on pull requests and weekly: SAST (Semgrep, Bandit), dependency auditing (pip-audit, npm audit, cargo audit), and secret scanning over full git history (gitleaks). Findings are held against a committed baseline that may shrink and not grow, so a new one is visible without pretending the backlog is zero. First run, 2026-08-07: five high-severity findings triaged to zero, and twelve secret-scan hits — all twelve false positives, individually checked, allowlisted with reasons rather than left to make the number meaningless.

**Whether a suite tests what it names** is a separate question from how many tests it has, and counting does not answer it. A rule that is named by a test but never *decides* that test's outcome can be deleted from an implementation, which will still pass. We published the method for measuring this rather than only asserting we had thought about it: [*Load-Bearing Coverage — Mechanically Checking Whether a Conformance Suite Can Be Passed Without Doing the Work*](https://doi.org/10.5281/zenodo.21844893) (2026-08-08, CC BY 4.0; implementation Apache-2.0). A rule counts as load-bearing only if deleting it from the reference verifier changes at least one published vector's outcome. Across nine measurements on seven corpora in three languages, suites that pass in the sense their authors intend were found certifying implementations that could skip obligations entirely — and the paper reports the same method turned back on its own suite, including three findings that were bugs in the checker.

**What none of this establishes.** Every test here encodes something we already thought of. That is precisely the limitation an independent assessor exists to address, and no amount of self-testing closes it — a suite cannot surprise its author.

And the criterion above has **not been run against the suite on this page**. It was built for conformance vector sets with a reference verifier to mutate, which is not the shape of most of these tests; adapting it is work we have not done. So the honest position is that we can state the standard and have applied it elsewhere, while the 5,650 figure remains a count — and this paragraph is here because publishing a method for detecting overstated coverage, and then quietly exempting yourself from it, is the failure the paper is about.

Specific gaps we would rather name than have found: no third-party penetration test; no adversarial review of the tier classifier by someone trying to defeat it; the hardware authorization path (`R3-dev`) cannot run in CI at all and is verified by measurement on a physical device; and the self-hosted deployment model has never been exercised inside a customer environment.

## Incident response

- Report security issues to [Louie.Lu@proofpane.com](mailto:Louie.Lu@proofpane.com) — acknowledged within 48 hours.
- Structured application logging and error tracking are in place; customers affected by a confirmed incident are notified directly.

**Legal boundary.** Proofpane produces **operational evidence** — a tamper-evident, independently verifiable record of what your AI systems actually did. It does **not** replace legal advice, certification bodies, or a regulator's judgment, and using Proofpane does not by itself make an organisation compliant with any framework. Control mappings (NIST AI RMF, ISO/IEC 42001, EU AI Act, GDPR, SOC 2) indicate which controls an exported record can evidence — your compliance obligations remain your own.

Questions a security review needs answered that aren't on this page? Email us — the answer will be added here.
