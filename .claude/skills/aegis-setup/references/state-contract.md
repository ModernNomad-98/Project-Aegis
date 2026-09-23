# Aegis setup state contract, version 1

Support is limited to a single-user Windows PowerShell 5.1 host and one local
checkout. `selection.ps1` obtains the user-local application data directory
from Windows and writes under `ProjectAegis\setup\v1`. It rejects a checkout
or state path containing a reparse redirect and rejects state inside the
checkout. The project key is lowercase SHA-256 of the uppercase absolute
physical checkout root (UTF-8). A moved checkout has a different key.

Each `<key>.json` has exactly these fields: `schema_version: 1`,
`project_key`, `choice: "aegis-only"`, `state: "selected"`,
`selected_at_utc`, `updated_at_utc`, `setup_completed_at_utc` (millisecond UTC
timestamps), and `evidence_version: "package-2"`. No raw credential, task
text, transcript, model result or helper verification is stored. `selected`
is a preference, not authority. `configured`, `verified` and `unavailable`
remain distinct future states; this writer cannot produce them.

Missing record means `unselected` and ordinary Aegis behavior. Unknown fields,
versions, duplicate keys, malformed timestamps and unsupported choices fail
closed. The user may explicitly select Aegis-only repair after a read error;
repair cannot overwrite a valid record. Selection reuses the original
`selected_at_utc` when replacing a valid record and sets a new completion time.

The writer takes a bounded per-project exclusive lock. It writes and flushes
a unique temporary file in the state directory, then uses same-directory
Windows file move for creation or Windows file replacement for overwrite.
Failed precommit writes retain the previous valid record and cannot claim
completion. There is no sync across computers. Other operating systems may
show the conversation but cannot claim saved selection until tested.
