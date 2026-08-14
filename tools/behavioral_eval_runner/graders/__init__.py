"""WP-2B-2 Scenario A deterministic graders (BER-DEC-007; non-live).

Every grader in this package grades RECORDED SYNTHETIC EVIDENCE only. No
module here dispatches to a model or provider, opens a session, or touches
the network. Deterministic results are reproducible from the same recorded
inputs and carry evidence pointers, input hashes, and a content-bound output
hash. Graders verify recorded evidence contracts; they do not prove real-host
containment (R4), activation observability (R1), or any live behavior.
"""
