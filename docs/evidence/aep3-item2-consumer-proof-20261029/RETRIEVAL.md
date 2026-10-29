# Retrieval and verification — AEP3-I2 consumer-proof final export

Everything needed to verify these bytes is inside this directory. No archive, sidecar or external tool is required.

## 1. Where this is obtained

    git clone https://github.com/ModernNomad-98/Project-Aegis.git
    cd Project-Aegis/docs/evidence/aep3-item2-consumer-proof-20261029

If you are reading this from a checkout, the publication already happened and **the commit that carries this directory is the identity of record**. The pull request that added it names the bundle aggregate; the merge receipt records base, head, merge commit and tree.

## 2. Verify every file

    sha256sum -c manifest.sha256        # every line: OK

PowerShell:

    Get-Content manifest.sha256 | ForEach-Object {
      $h,$p = $_ -split '  ',2
      if ((Get-FileHash $p -Algorithm SHA256).Hash -ne $h.ToUpper()) { "FAIL $p" } }

`manifest.sha256` covers every content file plus `EVIDENCE-INDEX.tsv`; it cannot cover itself or `BUNDLE-AGGREGATE.txt`.

**Aggregate.** SHA-256 over the concatenation of the 64-character lowercase per-file SHA-256 digests of the `EVIDENCE-INDEX.tsv` rows, in ascending path order (byte order of the UTF-8 path), with **no separators or newlines** between digests. Python:

    python - <<'PY'
    import csv, hashlib
    rows = sorted(csv.DictReader(open('EVIDENCE-INDEX.tsv', encoding='utf-8'), delimiter='\t'),
                  key=lambda r: r['path'].encode('utf-8'))
    h = hashlib.sha256()
    for r in rows:
        h.update(r['sha256'].encode('ascii'))
    print(len(rows), h.hexdigest())
    PY

The expected value, the row count and the total bytes are stated in `BUNDLE-AGGREGATE.txt`. `EVIDENCE-INDEX.tsv` also carries each file's byte and LF counts, so a byte/LF mismatch is detectable without opening the file.

## 3. Confirm the derivatives

Thirteen files differ from their Project Aegis workspace records (fourteen declared changes; one file carries two), each in declared ways only: eight have a personal full name in a commit-metadata citation replaced with `<name withheld>` (and, in one record, a host home path replaced with `<home-path withheld>`), and six JSON records have CRLF line endings normalised to LF so that the committed bytes verify against this manifest. `DERIVATIVE-MANIFEST.tsv` is the machine-readable before/after map (path, change class, bytes, SHA-256). Every other file is byte-identical to its source record.

## 4. Reading order

1. `README.md` §1–§3 — what this is, the 22 rows, the export gate.
2. `CONSOLIDATED-CP-LEDGER-V4.md` — the adjudicated ledger; then `rows/CP-01.md` … `rows/CP-22.md` for the row-level basis and evidence pointers.
3. `LIMITATIONS.md` — what is not claimed and what is withheld, before relying on any claim.
4. `records/CP21-EXECUTION-RECORD.md` and `records/CP22-SIGNATURE-BLOCK.txt` — the two observations that closed the export gate.
5. `deployments/live-capture-after.json` and the two retained manifests — the served bytes themselves.

## 5. Attribution and licence

`LICENSE` (Apache License 2.0, 11,357 B) and `NOTICE` (55 B) travel with the evidence. Do not redistribute the evidence without them.
