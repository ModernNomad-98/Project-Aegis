import assert from 'node:assert/strict';
import { test } from 'node:test';
import { mkdtempSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { createOfflineCallbacks, type AuthoritySnapshot } from './bridge.ts';

const base: AuthoritySnapshot = {
  generation: 'one', fresh: true, catalog_version: 'cat-1', policy_version: 'pol-1',
  synopsis: 'Review a synthetic API change', stage: 'review',
  agents: [{ id: 'reviewer', description: 'Reviews code', read_only: true },
    { id: 'writer', description: 'Writes code', read_only: false }],
  skills: [{ id: 'api', description: 'Reviews APIs', manual_only: false },
    { id: 'manual', description: 'Manually invoked', manual_only: true }],
  mandatory_agents: ['reviewer'], mandatory_skills: [],
  selected_agents: [], selected_skills: [], invoked_manual_skills: [],
  destination: 'local', local_only: true, ordinary_permission: 'allow', read_only_required: false,
};
const reply = (req: string, agents = ['reviewer'], skills = ['api']) => {
  const parsed = JSON.parse(req);
  return JSON.stringify({ version: '1', catalog_version: parsed.catalog_version,
    policy_version: parsed.policy_version, status: 'recommend', agents, skills });
};
function harness(change: Partial<AuthoritySnapshot> = {}, advise = reply) {
  const facts = { ...base, ...change };
  let calls = 0;
  const callbacks = createOfflineCallbacks({ snapshot: () => { calls++; return facts; }, advice: advise });
  return { callbacks, calls: () => calls, facts };
}
const agent = { tool_name: 'Agent', tool_input: { subagent_type: 'reviewer' } };
const skill = { tool_name: 'Skill', tool_input: { skill: 'api' } };
const noDecision = (result: any) => Object.keys(result).length === 0;
const denied = (result: any) => result.hookSpecificOutput?.permissionDecision === 'deny';

test('Agent and model Skill dispatch each recheck authority', async () => {
  const h = harness();
  assert.equal(noDecision(await h.callbacks.preToolUse(agent)), true);
  assert.equal(noDecision(await h.callbacks.preToolUse(skill)), true);
  assert.equal(h.calls(), 4);
});

test('unknown tool, unknown ID, malformed tool input and subagent name deny', async () => {
  const h = harness();
  for (const input of [{ tool_name: 'Read', tool_input: {} },
    { tool_name: 'Agent', tool_input: { subagent_type: 'unknown' } },
    { tool_name: 'Agent', tool_input: { subagent_type: '../bad' } },
    { tool_name: 'Agent', tool_input: {} },
    { tool_name: 'Skill', tool_input: { skill: 'unknown' } }]) {
    assert.equal(denied(await h.callbacks.preToolUse(input)), true);
  }
});

test('direct typed skill can be absent from model allowlist but needs genuine invocation', async () => {
  const h = harness({ selected_skills: ['manual'], invoked_manual_skills: ['manual'] },
    req => reply(req, ['reviewer'], ['manual']));
  assert.equal((await h.callbacks.userPromptExpansion({ expansion_type: 'slash_command', command_name: 'manual' })).decision, undefined);
  const ordinary = harness({ selected_skills: ['api'] });
  assert.equal((await ordinary.callbacks.userPromptExpansion({ expansion_type: 'slash_command', command_name: 'api' })).decision, undefined);
  assert.equal(denied(await h.callbacks.preToolUse({ tool_name: 'Skill', tool_input: { skill: 'manual' } })), true);
  assert.equal((await h.callbacks.userPromptExpansion({ expansion_type: 'slash_command', command_name: 'unknown' })).decision, 'block');
  assert.equal((await h.callbacks.userPromptExpansion({ expansion_type: 'mcp_prompt', command_name: 'manual' })).decision, 'block');
  assert.equal((await harness({ selected_skills: ['manual'] }).callbacks.userPromptExpansion({ expansion_type: 'slash_command', command_name: 'manual' })).decision, 'block');
});

test('mandatory and explicit selections cannot be dropped by advice', async () => {
  const h = harness({ selected_agents: ['writer'], selected_skills: ['api'] },
    req => reply(req, ['reviewer'], ['api']));
  assert.equal(denied(await h.callbacks.preToolUse(agent)), true);
  const missingMandatory = harness({}, req => reply(req, [], ['api']));
  assert.equal(denied(await missingMandatory.callbacks.preToolUse(skill)), true);
});

test('read-only and ordinary host permissions remain host-owned', async () => {
  const writer = harness({ read_only_required: true }, req => reply(req, ['reviewer', 'writer'], ['api']));
  assert.equal(denied(await writer.callbacks.preToolUse({ tool_name: 'Agent', tool_input: { subagent_type: 'writer' } })), true);
  for (const change of [{ ordinary_permission: 'deny' }, { destination: 'online' },
    { local_only: false }, { fresh: false }]) {
    assert.equal(denied(await harness(change).callbacks.preToolUse(agent)), true);
  }
});

test('changed or missing fresh authority between advice and dispatch denies', async () => {
  let generation = 0;
  let adviceCalls = 0;
  const callbacks = createOfflineCallbacks({
    snapshot: () => ({ ...base, generation: ++generation === 1 ? 'one' : 'two' }),
    advice: req => { adviceCalls++; return reply(req); },
  });
  assert.equal(denied(await callbacks.preToolUse(agent)), true);
  assert.equal(generation, 2);
  assert.equal(adviceCalls, 1);
  const reused = { ...base };
  const mutated = createOfflineCallbacks({ snapshot: () => reused,
    advice: req => { reused.policy_version = 'pol-2'; return reply(req); } });
  assert.equal(denied(await mutated.preToolUse(agent)), true);
  const missing = createOfflineCallbacks({ snapshot: () => { throw Error('missing'); }, advice: reply });
  assert.equal(denied(await missing.preToolUse(agent)), true);
});

test('equivalent authority with reordered object keys passes, but changed array order denies', async () => {
  const reordered = Object.fromEntries(Object.entries({ ...base,
    agents: base.agents.map(o => ({ read_only: o.read_only, description: o.description, id: o.id })),
    skills: base.skills.map(o => ({ manual_only: o.manual_only, description: o.description, id: o.id })),
  }).reverse()) as AuthoritySnapshot;
  let calls = 0;
  const equivalent = createOfflineCallbacks({ snapshot: () => ++calls === 1 ? base : reordered, advice: reply });
  assert.equal(noDecision(await equivalent.preToolUse(agent)), true);
  let changedCalls = 0;
  const changed = createOfflineCallbacks({ snapshot: () => ++changedCalls === 1 ? base : {
    ...reordered, agents: [...reordered.agents].reverse(),
  }, advice: reply });
  assert.equal(denied(await changed.preToolUse(agent)), true);
});

test('missing offer flags deny when runtime facts bypass the required TypeScript contract', async () => {
  const withoutReadOnly = { ...base, agents: [{ id: 'reviewer', description: 'Reviews code' }] } as unknown as AuthoritySnapshot;
  const withoutManualOnly = { ...base, skills: [{ id: 'api', description: 'Reviews APIs' }] } as unknown as AuthoritySnapshot;
  for (const facts of [withoutReadOnly, withoutManualOnly]) {
    const callbacks = createOfflineCallbacks({ snapshot: () => facts, advice: reply });
    assert.equal(denied(await callbacks.preToolUse(agent)), true);
  }
});

test('malformed, duplicate-key, oversized and contaminated replies deny', async () => {
  for (const advise of [() => '{', () => '{"version":"1","version":"1"}',
    () => 'x'.repeat(1025), req => reply(req).replace('"cat-1"', '"stale"'),
    req => JSON.stringify({ ...JSON.parse(reply(req)), agents: ['unknown'] }),
    req => JSON.stringify({ ...JSON.parse(reply(req)), status: 'abstain', agents: [], skills: [] })]) {
    assert.equal(denied(await harness({}, advise).callbacks.preToolUse(agent)), true);
  }
  assert.equal(denied(await harness({ synopsis: 'x'.repeat(4097) }).callbacks.preToolUse(agent)), true);
});

test('worker exit, timeout, output contamination and callback exception deny', async () => {
  const absent = createOfflineCallbacks({ snapshot: () => base, advice: reply, worker: 'absent-worker.py' });
  assert.equal(denied(await absent.preToolUse(agent)), true);
  const error = createOfflineCallbacks({ snapshot: () => base, advice: () => { throw Error('fail'); } });
  assert.equal(denied(await error.preToolUse(agent)), true);
  const timeout = createOfflineCallbacks({ snapshot: () => base, advice: reply, timeout_ms: 1 });
  assert.equal(denied(await timeout.preToolUse(agent)), true);
  const hungAdvice = createOfflineCallbacks({ snapshot: () => base,
    advice: () => new Promise<string>(() => {}), timeout_ms: 10 });
  assert.equal(denied(await hungAdvice.preToolUse(agent)), true);
  const temp = mkdtempSync(join(tmpdir(), 'aegis-bridge-'));
  try {
    const noisy = join(temp, 'noisy.py');
    writeFileSync(noisy, 'print("allow")\nprint("extra")\n');
    const contaminated = createOfflineCallbacks({ snapshot: () => base, advice: reply, worker: noisy });
    assert.equal(denied(await contaminated.preToolUse(agent)), true);
  } finally { rmSync(temp, { recursive: true, force: true }); }
});

test('worker rejects duplicate and oversized envelope frames', () => {
  const worker = 'tools.aegis_setup.host_bridge.contract_worker';
  const options = { cwd: new URL('../../..', import.meta.url), input: '{"kind":"agent","kind":"skill"}', encoding: 'utf8' as const };
  const duplicate = spawnSync(process.platform === 'win32' ? 'python' : 'python3', ['-B', '-m', worker], options);
  assert.equal(duplicate.status, 0);
  assert.equal(duplicate.stdout.trim(), 'deny');
  const oversized = spawnSync(process.platform === 'win32' ? 'python' : 'python3', ['-B', '-m', worker],
    { ...options, input: 'x'.repeat(6145) });
  assert.equal(oversized.status, 0);
  assert.equal(oversized.stdout.trim(), 'deny');
});

test('worker receives no unrelated inherited environment value', async () => {
  const temp = mkdtempSync(join(tmpdir(), 'aegis-bridge-env-'));
  const marker = 'AEGIS_SYNTHETIC_SECRET';
  const prior = process.env[marker];
  try {
    const worker = join(temp, 'env.py');
    writeFileSync(worker, 'import os\nprint("allow" if "AEGIS_SYNTHETIC_SECRET" not in os.environ else "deny")\n');
    process.env[marker] = 'invented-value';
    const callbacks = createOfflineCallbacks({ snapshot: () => base, advice: reply, worker });
    assert.equal(noDecision(await callbacks.preToolUse(agent)), true);
  } finally {
    if (prior === undefined) delete process.env[marker]; else process.env[marker] = prior;
    rmSync(temp, { recursive: true, force: true });
  }
});
