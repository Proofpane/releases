# Proofpane downloads

This repo hosts download artefacts for [proofpane.com](https://proofpane.com).
The main Proofpane codebase is private; this public mirror gives
browsers (Chrome Safe Browsing, Edge SmartScreen) a high-reputation
host so downloads aren't flagged as "unverified".

## Get the daemon

See [proofpane.com/install](https://proofpane.com/install) for the
guided install. Direct download links live on the
[Releases](https://github.com/proofpane/releases/releases) page.

## SHA-256 verification

Every binary ships with a `.sha256` sibling:

```bash
shasum -a 256 -c ProofpaneDaemon-macos-x86_64.zip.sha256
```

## Reporting issues

For daemon issues, email Louie.Lu@proofpane.com.
