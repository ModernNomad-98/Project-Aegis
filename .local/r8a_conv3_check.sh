#!/bin/sh
: "${BASE:?BASE required}"
: "${HEAD:?HEAD required}"
if [ -z "${TARGET_PATH:-}" ]; then echo "content_match_status=UNVERIFIED reason=empty_TARGET_PATH"; exit 2; fi
set +e
git merge-base --is-ancestor "$BASE" "$HEAD"; anc_rc=$?
GIT_LITERAL_PATHSPECS=1 git diff --no-textconv --no-ext-diff --quiet "$BASE" "$HEAD" -- "$TARGET_PATH"; content_rc=$?
base_oid=$(git rev-parse --verify --quiet "$BASE:$TARGET_PATH"); base_oid_rc=$?
head_oid=$(git rev-parse --verify --quiet "$HEAD:$TARGET_PATH"); head_oid_rc=$?
set -e
case "$anc_rc" in 0) ancestry_status=ancestor_or_equal ;; 1) ancestry_status=not_ancestor ;; *) ancestry_status=UNVERIFIED ;; esac
case "$content_rc" in 0) content_match_status=same ;; 1) content_match_status=differs ;; *) content_match_status=UNVERIFIED ;; esac
if [ "$base_oid_rc" -eq 0 ] && [ "$head_oid_rc" -eq 0 ]; then
  if [ "$base_oid" = "$head_oid" ]; then oid_match_status=same; else oid_match_status=differs; fi
else oid_match_status=UNVERIFIED; fi
echo "ancestry_status=$ancestry_status ancestry_rc=$anc_rc"
echo "content_match_status=$content_match_status content_rc=$content_rc"
echo "blob_oid base=$base_oid head=$head_oid oid_match_status=$oid_match_status"
if [ "$ancestry_status" = UNVERIFIED ] || [ "$content_match_status" = UNVERIFIED ] || [ "$oid_match_status" = UNVERIFIED ]; then exit 3; fi
exit 0