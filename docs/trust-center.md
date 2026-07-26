> Mirror of <https://proofpane.com/trust/> · synced 2026-07-26 · the canonical, always-current version lives on proofpane.com

# Trust Center

Plain text, structured, written for security review — no marketing images. Each item is tagged `[shipped]`  or `[roadmap]`  so you always know which is which.

Last updated: 2026-07-09 · Security contact: [Louie.Lu@proofpane.com](mailto:Louie.Lu@proofpane.com) · Company stage: early (founding design partners onboarding) · Founder: [Louie Lu on LinkedIn](https://www.linkedin.com/in/louielunz)

## Deployment models `[shipped]`

- **Cloud + local daemon (default):** a local connector (single binary; macOS arm64/x86_64, Linux, Windows) runs on the user's machine and pairs to the cloud control plane. Tool-layer enforcement happens locally; audit rows are sent to the cloud.
- **Egress gateway:** model API calls route through the gateway for policy, DLP and metering, then forward to the provider the customer configured.
- **Hosting:** the control plane runs on Fly.io (Sydney region). The landing site is served by Cloudflare Pages.

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

## Certifications & assurance `[roadmap]`

- **SOC 2 Type II:** not yet certified; program start is on the current company roadmap. We say this plainly rather than implying otherwise.
- **Penetration test:** no third-party pen test completed yet; planned alongside the first enterprise deployment. Security researchers are welcome at the contact above.
- **Binary signing:** macOS notarisation (Developer ID) and Windows Authenticode signing are pending certificate procurement; the build pipeline publishes SHA-256 checksums today, and the installer verifies them.

## Incident response

- Report security issues to [Louie.Lu@proofpane.com](mailto:Louie.Lu@proofpane.com) — acknowledged within 48 hours.
- Structured application logging and error tracking are in place; customers affected by a confirmed incident are notified directly.

**Legal boundary.** Proofpane produces **operational evidence** — a tamper-evident, independently verifiable record of what your AI systems actually did. It does **not** replace legal advice, certification bodies, or a regulator's judgment, and using Proofpane does not by itself make an organisation compliant with any framework. Control mappings (NIST AI RMF, ISO/IEC 42001, EU AI Act, GDPR, SOC 2) indicate which controls an exported record can evidence — your compliance obligations remain your own.

Questions a security review needs answered that aren't on this page? Email us — the answer will be added here.
