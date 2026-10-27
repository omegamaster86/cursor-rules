#!/usr/bin/env node
/**
 * agent-review レーン用 Task model を .cursor/rules/forge-models.mdc から解決する。
 * 親オーケストレーターはフェーズ1（Task 起動）の直前に必ず実行する。
 *
 * Usage: node .cursor/skills/agent-review/scripts/resolve-lane-models.mjs [projectRoot]
 */

import { readFileSync } from 'node:fs'
import { resolve, join } from 'node:path'

/** Cursor Task `model` が実際に受け付ける slug（forge 意図 slug とは別） */
const CURSOR_TASK_RUNTIME_ALLOWLIST = new Set([
  'claude-opus-5-5-medium',
  'claude-sonnet-5-5-high',
  'composer-2.5',
  'composer-2.5-fast',
  'cursor-grok-4.6-medium',
  'gemini-3.8-flash-medium',
  'gemini-4-argon-medium',
  'gpt-5.6-sol-medium',
  'grok-4.7-medium',
  'muse-wonder-1.0-high',
])

const LANES = {
  A: {
    role: 'review orchestrator grok',
    subagent_type: 'generalPurpose',
    defaultModel: 'grok-4.7-medium',
  },
  B: {
    role: 'review orchestrator sonnet correctness',
    subagent_type: 'generalPurpose',
    defaultModel: 'claude-opus-5-5-medium',
  },
  C: {
    role: 'review orchestrator sonnet quality',
    subagent_type: 'generalPurpose',
    defaultModel: 'claude-opus-5-5-medium',
  },
  D: {
    role: 'review orchestrator security',
    subagent_type: 'security-review',
    defaultModel: 'claude-opus-5-5-medium',
  },
  E: {
    role: 'review orchestrator blast radius',
    subagent_type: 'generalPurpose',
    defaultModel: 'claude-opus-5-5-medium',
  },
}

const projectRoot = resolve(process.argv[2] ?? process.cwd())
const forgePath = join(projectRoot, '.cursor/rules/forge-models.mdc')

function parseForgeModels(text) {
  const roleToModel = new Map()
  const allowed = new Set()

  let inTaskSlugSection = false
  for (const line of text.split('\n')) {
    if (line.startsWith('## Task `model` で使える model')) {
      inTaskSlugSection = true
      continue
    }
    if (inTaskSlugSection) {
      if (line.startsWith('## ')) inTaskSlugSection = false
      else {
        const bullet = line.match(/^-\s+`([^`]+)`/)
        if (bullet) allowed.add(bullet[1])
      }
    }

    const roleMatch = line.match(/^(review orchestrator[^:]+):\s*(\S+)\s*$/)
    if (roleMatch) {
      roleToModel.set(roleMatch[1].trim(), roleMatch[2].trim())
    }
  }

  return { roleToModel, allowed }
}

function resolveModel(role, defaultModel, roleToModel, allowed) {
  const fromForge = roleToModel.get(role)
  const raw = fromForge ?? defaultModel
  const source = fromForge != null ? 'forge-models.mdc' : 'models.md default'

  if (raw === 'inherit') {
    return { model: null, omitTaskModel: true, source, raw }
  }

  if (!allowed.has(raw)) {
    return {
      model: defaultModel,
      omitTaskModel: false,
      source: 'script defaultModel (forge slug not in Task allowlist)',
      raw,
      warning: `slug "${raw}" not in forge-models Task allowlist; fell back to ${defaultModel}`,
    }
  }

  return { model: raw, omitTaskModel: false, source, raw }
}

let text
try {
  text = readFileSync(forgePath, 'utf8')
} catch (err) {
  console.error(JSON.stringify({ error: `cannot read ${forgePath}`, detail: String(err) }))
  process.exit(1)
}

const { roleToModel, allowed } = parseForgeModels(text)
const lanes = {}
const warnings = []

for (const [id, cfg] of Object.entries(LANES)) {
  const resolved = resolveModel(
    cfg.role,
    cfg.defaultModel,
    roleToModel,
    allowed,
  )
  if (resolved.warning) warnings.push({ lane: id, ...resolved })
  lanes[id] = {
    role: cfg.role,
    subagent_type: cfg.subagent_type,
    model: resolved.model,
    omit_task_model: resolved.omitTaskModel,
    resolved_from: resolved.source,
    forge_value: roleToModel.get(cfg.role) ?? null,
  }
}

const out = {
  forge_models_path: forgePath,
  lanes,
  warnings,
}

console.log(JSON.stringify(out, null, 2))

