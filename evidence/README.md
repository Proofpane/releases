# Proofpane — Sample Evidence Pack (GitHub mirror)

Mirror of <https://proofpane.com/evidence/sample-pack/> for readers whose network
egress is allowlisted to common developer domains (github.com,
raw.githubusercontent.com, PyPI) and who therefore cannot download from
proofpane.com directly — sandboxed AI agents included. **Same bytes, same
claims, same honest labels as the site.** Synced 2026-07-26.

This is a real Proofpane Evidence Pack — exported by the production code path
and signed with Ed25519. Verify it on your own machine, offline: manifest
signature, every file hash, and the full audit hash chain, re-computed locally.
No Proofpane account. No API. No trusting us.

## Files

| File | sha256 |
|---|---|
| `proofpane-sample-evidence-pack.zip` | `88a097acb6ba453a8bc48ed1dd7189949d566034c0afd3e56cf02b8e1191da4c` |
| `verify_evidence_pack.py` (standalone verifier) | `4d8026b3ed0f9e39a0bf35a01aee3028b3b8fd189b8116f54df5709448dcba29` |
| `signing-key.pem` (publisher key, published out-of-band) | `92a517b7893084bb183299b40a4ba62a41af5655f6e1af43d047d60950d2d30b` |

Raw URLs (allowlist-friendly):

```
curl -LO https://raw.githubusercontent.com/Proofpane/releases/main/evidence/proofpane-sample-evidence-pack.zip
curl -LO https://raw.githubusercontent.com/Proofpane/releases/main/evidence/verify_evidence_pack.py
curl -LO https://raw.githubusercontent.com/Proofpane/releases/main/evidence/signing-key.pem
```

## Verify (two commands)

```
pip install cryptography        # the only dependency (Ed25519) — installs from PyPI
python3 verify_evidence_pack.py proofpane-sample-evidence-pack.zip --pubkey signing-key.pem --verbose
```

Success ends with: `PASS — bundle integrity confirmed.`

## Integrity vs provenance (why `--pubkey` matters)

Without `--pubkey`, the verifier reads the signing key from *inside* the pack —
that proves the pack is internally consistent (**integrity**) but not who
produced it (**provenance**). A forger can rebuild a fully self-consistent pack
around their own fresh key and pass an unpinned check. `--pubkey signing-key.pem`
pins the key published here, out-of-band; a forged pack's embedded key won't
match and is rejected before any signature is checked.

**Honest boundary:** pinning does not yet defend against a backdated whole-chain
rebuild by the publisher itself. The rigorous fix is an *external anchor* — RFC
3161 timestamp, an RFC 6962 / Certificate-Transparency-style log, or Sigstore
Rekor — binding the chain head to a rail neither party controls. Self-signed
chain-head anchors ship today; external-transparency-log anchoring is on the
roadmap, not shipped. This is the spec (invariant II: independent evidence needs
a rail the audited party can't control) held to its own line, in public.

## Then try to break it

Two experiments:

1. **Edit** — unzip the pack, change any byte of `audit/records.json`, re-zip,
   re-run. The signature breaks; it fails.
2. **Forge** — generate your own Ed25519 key, rewrite records, re-mine the whole
   chain, re-sign the manifest, swap in your key. An *unpinned* run passes (that's
   the point). Run again with `--pubkey signing-key.pem` and it fails:
   `embedded key does NOT match the pinned publisher key`.

## Honest labeling

The events in this pack are a seeded demo narrative — no real customer data.
Everything else is production-real: the export code path, the hash chain, the
manifest, the Ed25519 signature (a sample key; each deployment signs with its
own), and the verifier — byte-for-byte the tool an auditor would run on a real
engagement.

See `../docs/` for the mirrored public docs (Trust Center, Proof Index,
what-is-proofpane, the founder essay), or <https://proofpane.com/llms.txt>.
