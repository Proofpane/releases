#!/usr/bin/env python3
"""
Standalone verifier for Proofpane Evidence Packs.

This tool runs **offline** with no backend or repo access. Give it a pack zip,
it reports PASS/FAIL with precise pointers to any broken byte.

Usage:
    python3 verify_evidence_pack.py <pack.zip> --pubkey signing-key.pem   # integrity + provenance
    python3 verify_evidence_pack.py <pack.zip> --verbose                  # integrity only (key from pack)

Requires only the `cryptography` package:
    pip install cryptography

Exit codes:
    0  bundle is intact
    1  any verification step failed
    2  bundle structure is malformed (cannot verify)
"""

import argparse
import base64
import hashlib
import json
import sys
import zipfile
from typing import Optional


GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
DIM = "\033[2m"
RESET = "\033[0m"
BOLD = "\033[1m"


def ok(msg: str) -> None:
    print(f"{GREEN}✓{RESET} {msg}")


def fail(msg: str) -> None:
    print(f"{RED}✗{RESET} {msg}")


def info(msg: str) -> None:
    print(f"{DIM}  {msg}{RESET}")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json_bytes(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str).encode("utf-8")


def _compute_audit_hash(row: dict, prev_hash: str) -> str:
    """Mirror of audit_log_service._compute_hash. Order is load-bearing."""
    parts = [
        str(row["id"]),
        row["timestamp"],
        row.get("org_id") or "default",
        row["actor"],
        row["event_type"],
        row.get("skill_id") or "",
        row.get("runtime_kind") or "",
        row.get("runtime_policy") or "",
        _canonical_json_bytes(row["payload"]).decode("utf-8"),
        prev_hash,
    ]
    h = hashlib.sha256()
    h.update("\x1f".join(parts).encode("utf-8"))
    return h.hexdigest()


def verify_pack(pack_path: str, verbose: bool = False, pubkey_path: Optional[str] = None) -> int:
    print(f"{BOLD}Verifying:{RESET} {pack_path}\n")

    # --- Open the zip ---
    try:
        zf = zipfile.ZipFile(pack_path, "r")
    except (zipfile.BadZipFile, FileNotFoundError) as e:
        fail(f"Cannot open zip: {e}")
        return 2

    names = set(zf.namelist())
    required = {"manifest.json", "signatures/manifest.sig", "signatures/public_key.pem", "audit/records.json"}
    missing = required - names
    if missing:
        fail(f"Missing required entries: {sorted(missing)}")
        return 2

    # --- Load manifest, signature, public key ---
    manifest_bytes = zf.read("manifest.json")
    sig_bytes = zf.read("signatures/manifest.sig")
    pub_pem = zf.read("signatures/public_key.pem")

    # --- Provenance pin (--pubkey): the key inside the pack proves internal
    # consistency only — a forger can rebuild a self-consistent pack around a
    # fresh keypair. Pinning an out-of-band copy of the publisher's key closes
    # that: every signature check below then verifies against a key the pack
    # itself cannot supply. Published at
    #   https://proofpane.com/evidence/sample-pack/signing-key.pem
    #   https://raw.githubusercontent.com/Proofpane/releases/main/evidence/signing-key.pem
    pinned = False
    if pubkey_path:
        try:
            from cryptography.hazmat.primitives import serialization
            pinned_pub = serialization.load_pem_public_key(open(pubkey_path, "rb").read())
            pack_pub = serialization.load_pem_public_key(pub_pem)
            from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
            if pinned_pub.public_bytes(Encoding.Raw, PublicFormat.Raw) != \
               pack_pub.public_bytes(Encoding.Raw, PublicFormat.Raw):
                fail("Pack's embedded key does NOT match the pinned publisher key — "
                     "self-consistent but not from this publisher. Treat as forged.")
                return 1
            pub_pem = open(pubkey_path, "rb").read()
            pinned = True
        except Exception as e:  # noqa: BLE001
            fail(f"Cannot load pinned public key {pubkey_path}: {e}")
            return 2

    try:
        manifest = json.loads(manifest_bytes)
    except json.JSONDecodeError as e:
        fail(f"manifest.json is not valid JSON: {e}")
        return 2

    fp = manifest.get("signing_key_fingerprint", "?")
    print(f"{DIM}Manifest version: {manifest.get('version')}{RESET}")
    print(f"{DIM}Exported at:      {manifest.get('exported_at')}{RESET}")
    print(f"{DIM}Records claimed:  {manifest.get('record_count')}{RESET}")
    print(f"{DIM}Key fingerprint:  {fp}{RESET}")
    print()

    failures = 0

    # --- Step 1: Verify the signature on manifest.json ---
    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import ed25519
        from cryptography.exceptions import InvalidSignature
    except ImportError:
        fail("Missing dependency: pip install cryptography")
        return 2

    try:
        pub = serialization.load_pem_public_key(pub_pem)
        if not isinstance(pub, ed25519.Ed25519PublicKey):
            fail("Public key in bundle is not Ed25519")
            return 2
        # Sign was over the canonical JSON bytes, which equal the on-disk manifest bytes
        pub.verify(sig_bytes, manifest_bytes)
        ok(f"Signature valid (Ed25519, key fingerprint {fp})")
        if pinned:
            ok("Signing key matches the pinned publisher key (provenance verified)")
    except InvalidSignature:
        fail("Signature INVALID — manifest.json was tampered with, or signed by a different key")
        failures += 1
    except Exception as e:  # noqa: BLE001
        fail(f"Signature verification error: {e}")
        failures += 1

    # --- Step 2: Re-hash every file listed in manifest, compare ---
    declared_files: dict = manifest.get("files", {})
    if not declared_files:
        fail("manifest.json declares no files — malformed pack")
        return 2

    mismatches = []
    for path, expected_hash in sorted(declared_files.items()):
        if path not in names:
            mismatches.append((path, "FILE MISSING FROM ZIP"))
            continue
        actual = _sha256(zf.read(path))
        if actual != expected_hash:
            mismatches.append((path, f"hash mismatch (expected {expected_hash[:12]}..., got {actual[:12]}...)"))

    if mismatches:
        fail(f"{len(mismatches)} of {len(declared_files)} files do not match manifest:")
        for path, why in mismatches:
            print(f"    {RED}- {path}: {why}{RESET}")
        failures += 1
    else:
        ok(f"All {len(declared_files)} file hashes match manifest")

    # Also flag any files in the zip NOT covered by the manifest (except manifest.json + sig itself)
    expected_extras = {"manifest.json", "signatures/manifest.sig"}
    extras = (names - set(declared_files.keys())) - expected_extras
    if extras:
        fail(f"Zip contains files NOT covered by manifest (potential injection): {sorted(extras)}")
        failures += 1

    # --- Step 3: Re-walk the audit hash chain inside audit/records.json ---
    try:
        records = json.loads(zf.read("audit/records.json"))
    except json.JSONDecodeError as e:
        fail(f"audit/records.json is not valid JSON: {e}")
        return 2

    if not isinstance(records, list):
        fail("audit/records.json must be a JSON array")
        return 2

    if not records:
        info("Audit slice is empty (nothing to chain-verify)")
    else:
        broken = None
        # First record's stored prev_hash is what links it to the global chain.
        # We can only verify this matches what the slice claims — anchors are advisory.
        expected_prev = records[0].get("prev_hash", "")
        for row in records:
            stored_prev = row.get("prev_hash", "")
            if stored_prev != expected_prev:
                broken = (row.get("id"), "prev_hash mismatch within slice")
                break
            recomputed = _compute_audit_hash(row, stored_prev)
            stored_recorded = row.get("record_hash", "")
            if recomputed != stored_recorded:
                broken = (row.get("id"), f"record_hash mismatch (recomputed {recomputed[:12]}..., stored {stored_recorded[:12]}...)")
                break
            expected_prev = stored_recorded

        if broken:
            fail(f"Audit chain BROKEN at record id={broken[0]}: {broken[1]}")
            failures += 1
        else:
            ok(f"Audit chain re-verified: {len(records)} records, all hashes match")

        # Sanity check anchors against actual slice
        anchors = manifest.get("chain_anchors", {})
        if anchors:
            if anchors.get("prev_hash_before_slice") != records[0]["prev_hash"]:
                fail("chain_anchors.prev_hash_before_slice does not match first record's prev_hash")
                failures += 1
            elif anchors.get("last_hash_in_slice") != records[-1]["record_hash"]:
                fail("chain_anchors.last_hash_in_slice does not match last record's record_hash")
                failures += 1
            else:
                ok("Chain anchors line up with slice boundaries")

        # --- Step 4: Verify Ed25519-signed chain-head NOTARIZATIONS (moat) ---
        # Each notary anchor independently proves — with the platform key — that
        # the chain head at a past point had a given record_hash. This catches a
        # whole-chain re-mine that internal hash-checking cannot: a forged chain
        # can't produce a valid signature over its own head. Optional section
        # (absent in packs built before any anchor was signed).
        if "audit/notary_anchors.json" in names:
            try:
                from cryptography.hazmat.primitives import serialization
                _pub = serialization.load_pem_public_key(pub_pem)
            except Exception as e:  # noqa: BLE001
                _pub = None
                info(f"cannot load public key for notary check: {e}")
            try:
                notary = json.loads(zf.read("audit/notary_anchors.json"))
            except Exception as e:  # noqa: BLE001
                fail(f"audit/notary_anchors.json is not valid JSON: {e}")
                notary = []
                failures += 1
            rec_by_id = {r["id"]: r for r in records}
            verified = 0
            for a in notary:
                payload = json.dumps(
                    {"max_id": a["max_id"], "head_record_hash": a["head_record_hash"],
                     "row_count": a["row_count"]},
                    sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                ).encode("utf-8")
                if _pub is None:
                    failures += 1
                    fail("notary anchor present but public key could not be loaded")
                    break
                try:
                    _pub.verify(base64.b64decode(a["signature_b64"]), payload)
                except Exception:  # noqa: BLE001
                    fail(f"notary anchor id={a.get('max_id')}: Ed25519 signature INVALID")
                    failures += 1
                    continue
                rec = rec_by_id.get(a["max_id"])
                if rec is None:
                    info(f"notary anchor id={a['max_id']} outside this slice (signature valid, not cross-checked)")
                    verified += 1
                elif rec["record_hash"] != a["head_record_hash"]:
                    fail(f"notary anchor id={a['max_id']}: head_record_hash != the record in this slice")
                    failures += 1
                else:
                    verified += 1
            if notary and verified == len(notary):
                ok(f"Notarization verified: {verified} signed chain-head anchor(s) — signatures + hashes match")

    if verbose and records:
        print()
        print(f"{DIM}Slice details:{RESET}")
        print(f"{DIM}  first id={records[0]['id']} at {records[0]['timestamp']}{RESET}")
        print(f"{DIM}  last  id={records[-1]['id']} at {records[-1]['timestamp']}{RESET}")
        events = {}
        for r in records:
            events[r["event_type"]] = events.get(r["event_type"], 0) + 1
        for et, c in sorted(events.items()):
            print(f"{DIM}  {et}: {c}{RESET}")

    print()
    if failures == 0:
        print(f"{GREEN}{BOLD}PASS{RESET} — bundle integrity confirmed.")
        if not pinned:
            print(f"{YELLOW}note:{RESET} the signing key was read from the pack itself — this proves internal")
            print("      consistency, not provenance. To also verify WHO produced it, pin the")
            print("      publisher's key:  --pubkey signing-key.pem   (published out-of-band at")
            print("      proofpane.com/evidence/sample-pack/signing-key.pem and mirrored on GitHub)")
        return 0
    print(f"{RED}{BOLD}FAIL{RESET} — {failures} verification step(s) failed. {YELLOW}Reject this bundle.{RESET}")
    return 1


def main():
    parser = argparse.ArgumentParser(description="Verify an Proofpane Evidence Pack offline.")
    parser.add_argument("pack", help="Path to the .zip evidence pack")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print extra detail about the slice")
    parser.add_argument("--pubkey", metavar="PEM",
                        help="Path to an out-of-band copy of the publisher's Ed25519 public key. "
                             "Verifies provenance, not just internal consistency: the pack's "
                             "embedded key must match, and all signatures verify against this key.")
    args = parser.parse_args()
    sys.exit(verify_pack(args.pack, verbose=args.verbose, pubkey_path=args.pubkey))


if __name__ == "__main__":
    main()
