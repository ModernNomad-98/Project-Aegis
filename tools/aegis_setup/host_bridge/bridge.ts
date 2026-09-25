/** Offline callback candidate. Importing this module cannot start an SDK session. */
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import type { SyncHookJSONOutput } from '@anthropic-ai/claude-agent-sdk';

export type AgentOffer = { id: string; description: string; read_only: boolean };
export type SkillOffer = { id: string; description: string; manual_only: boolean };
export type AuthoritySnapshot = {
  generation: string;
  fresh: boolean;
  catalog_version: string;
  policy_version: string;
  synopsis: string;
  stage: 'discovery' | 'design' | 'implementation' | 'review' | 'release';
  agents: AgentOffer[];
  skills: SkillOffer[];
  mandatory_agents: string[];
  mandatory_skills: string[];
  selected_agents: string[];
  selected_skills: string[];
  invoked_manual_skills: string[];
  destination: 'local' | 'online' | string;
  local_only: boolean;
  ordinary_permission: 'allow' | 'deny' | string;
  read_only_required: boolean;
};
export type HostFacts = {
  snapshot: () => AuthoritySnapshot | Promise<AuthoritySnapshot>;
  /** An untrusted, synthetic reply; no network or provider fallback is supplied. */
  advice: (request: string) => string | Promise<string>;
  python?: string;
  worker?: string;
  timeout_ms?: number;
};
type Proposal = { kind: 'agent' | 'skill'; target: string; direct: boolean };
type HookInput = { tool_name?: unknown; tool_input?: unknown; expansion_type?: unknown; command_name?: unknown };

const here = dirname(fileURLToPath(import.meta.url));
const repo = resolve(here, '../../..');
const id = /^[a-z][a-z0-9-]{0,63}$/;

function bounded<T>(run: () => T | Promise<T>, milliseconds: number): Promise<T> {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(Error('offline callback timeout')), milliseconds);
    Promise.resolve().then(run).then(
      value => { clearTimeout(timer); resolve(value); },
      error => { clearTimeout(timer); reject(error); },
    );
  });
}

function requestFrom(snapshot: AuthoritySnapshot): string {
  return JSON.stringify({
    version: '1', synopsis: snapshot.synopsis, stage: snapshot.stage,
    catalog_version: snapshot.catalog_version, policy_version: snapshot.policy_version,
    agents: snapshot.agents.map(o => ({ id: o.id, description: o.description, read_only: o.read_only })),
    skills: snapshot.skills.map(o => ({ id: o.id, description: o.description, manual_only: o.manual_only })),
    mandatory_agents: snapshot.mandatory_agents, mandatory_skills: snapshot.mandatory_skills,
    selected_agents: snapshot.selected_agents, selected_skills: snapshot.selected_skills,
    invoked_manual_skills: snapshot.invoked_manual_skills,
  });
}

function canonicalJson(value: AuthoritySnapshot): string {
  return JSON.stringify(value, (_key, item) =>
    item !== null && typeof item === 'object' && !Array.isArray(item)
      ? Object.fromEntries(Object.entries(item).sort(([a], [b]) => a < b ? -1 : a > b ? 1 : 0))
      : item);
}

function validAuthority(s: AuthoritySnapshot, p: Proposal): boolean {
  if (!s || s.fresh !== true || s.destination !== 'local' || s.local_only !== true ||
      s.ordinary_permission !== 'allow' || !id.test(s.generation) || !id.test(p.target)) return false;
  const offers = p.kind === 'agent' ? s.agents : s.skills;
  if (!Array.isArray(offers) || !offers.some(o => o.id === p.target)) return false;
  if (p.kind === 'agent' && s.read_only_required &&
      !offers.some(o => o.id === p.target && o.read_only === true)) return false;
  if (p.kind === 'skill' && offers.some(o => o.id === p.target && o.manual_only === true) &&
      (!p.direct || !s.selected_skills.includes(p.target) || !s.invoked_manual_skills.includes(p.target))) return false;
  if (p.direct && (p.kind !== 'skill' || !s.selected_skills.includes(p.target))) return false;
  return true;
}

function validateLocally(request: string, response: string, proposal: Proposal, facts: HostFacts): boolean {
  if (Buffer.byteLength(request, 'utf8') > 4096 || Buffer.byteLength(response, 'utf8') > 1024) return false;
  const frame = JSON.stringify({ request, response, kind: proposal.kind, target: proposal.target });
  if (Buffer.byteLength(frame, 'utf8') > 6144) return false;
  const result = spawnSync(facts.python ?? (process.platform === 'win32' ? 'python' : 'python3'),
    facts.worker ? ['-B', '-S', facts.worker] : ['-B', '-S', '-m', 'tools.aegis_setup.host_bridge.contract_worker'], {
      cwd: repo, input: frame, encoding: 'utf8', timeout: facts.timeout_ms ?? 3000,
      maxBuffer: 1024, windowsHide: true,
      env: { PATH: process.env.PATH, SystemRoot: process.env.SystemRoot,
        WINDIR: process.env.WINDIR, TEMP: process.env.TEMP, TMP: process.env.TMP,
        PYTHONDONTWRITEBYTECODE: '1', PYTHONIOENCODING: 'utf-8' },
    });
  return !result.error && result.status === 0 && result.stderr === '' &&
    (result.stdout === 'allow\n' || result.stdout === 'allow\r\n');
}

async function evaluate(facts: HostFacts, proposal: Proposal): Promise<boolean> {
  try {
    const timeout = facts.timeout_ms ?? 3000;
    if (!Number.isInteger(timeout) || timeout < 1 || timeout > 5000) return false;
    const before = await bounded(() => facts.snapshot(), timeout);
    if (!validAuthority(before, proposal)) return false;
    const binding = canonicalJson(before);
    const request = requestFrom(before);
    if (Buffer.byteLength(request, 'utf8') > 4096) return false;
    const response = await bounded(() => facts.advice(request), timeout);
    if (typeof response !== 'string' || Buffer.byteLength(response, 'utf8') > 1024) return false;
    const after = await bounded(() => facts.snapshot(), timeout);
    if (binding !== canonicalJson(after) || !validAuthority(after, proposal)) return false;
    return validateLocally(request, response, proposal, facts);
  } catch {
    return false;
  }
}

function modelProposal(input: HookInput): Proposal | null {
  if (input.tool_name === 'Agent' && input.tool_input && typeof input.tool_input === 'object') {
    const target = (input.tool_input as { subagent_type?: unknown }).subagent_type;
    return typeof target === 'string' ? { kind: 'agent', target, direct: false } : null;
  }
  if (input.tool_name === 'Skill' && input.tool_input && typeof input.tool_input === 'object') {
    const target = (input.tool_input as { skill?: unknown }).skill;
    return typeof target === 'string' ? { kind: 'skill', target, direct: false } : null;
  }
  return null;
}

function directProposal(input: HookInput): Proposal | null {
  if (input.expansion_type !== 'slash_command' || typeof input.command_name !== 'string') return null;
  const target = input.command_name.replace(/^\//, '');
  return id.test(target) ? { kind: 'skill', target, direct: true } : null;
}

/** A passing recommendation makes no permission decision; a failure denies. No tool is dispatched here. */
export function createOfflineCallbacks(facts: HostFacts) {
  return {
    preToolUse: async (input: HookInput): Promise<SyncHookJSONOutput> => {
      const proposal = modelProposal(input);
      const allowed = proposal ? await evaluate(facts, proposal) : false;
      return allowed ? {} : { hookSpecificOutput: {
        hookEventName: 'PreToolUse', permissionDecision: 'deny',
        permissionDecisionReason: 'Offline bridge denied assisted dispatch',
      } };
    },
    userPromptExpansion: async (input: HookInput): Promise<SyncHookJSONOutput> => {
      const proposal = directProposal(input);
      const allowed = proposal ? await evaluate(facts, proposal) : false;
      return allowed ? {} : { decision: 'block', reason: 'Offline bridge denied direct skill dispatch' };
    },
  };
}
