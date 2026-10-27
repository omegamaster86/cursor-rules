#!/usr/bin/env node
/**
 * agent-review レーン用 Task model を .cursor/rules/forge-models.mdc から解決する。
 * 親オーケストレーターはフェーズ1.9（Task 起動）の直前に必ず実行する。
 *
 * Usage: node .cursor/skills/agent-review/scripts/resolve-lane-models.mjs [projectRoot]
 */

import { readFileSync } from 'node:fs'
import { resolve, join } from 'node:path'

const LANES = {
  A: {
    role: 'review orchestrator grok',
    subagent_type: 'generalPurpose',
  },
  B: {
    role: 'review orchestrator sonnet correctness',
    subagent_type: 'generalPurpose',
  },
  C: {
    role: 'review orchestrator sonnet quality',
    subagent_type: 'generalPurpose',
  },
  D: {
    role: 'review orchestrator security',
    subagent_type: 'security-review',
  },
  E: {
    role: 'review orchestrator blast radius',
    subagent_type: 'generalPurpose',
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

function resolveModel(role, roleToModel, allowed) {
  const fromForge = roleToModel.get(role)

  if (fromForge == null) {
    return {
      model: null,
      omitTaskModel: true,
      source: 'parent-chat (role line missing)',
      raw: null,
    }
  }

  const raw = fromForge
  if (raw === 'inherit') {
    return { model: null, omitTaskModel: true, source: 'forge-models.mdc (inherit)', raw }
  }

  if (allowed.size === 0) {
    return {
      model: null,
      omitTaskModel: true,
      source: 'parent-chat (Task allowlist empty in forge-models.mdc)',
      raw,
      warning:
        'forge-models.mdc has no parsed Task allowlist bullets; omitting Task model for all lanes',
    }
  }

  if (!allowed.has(raw)) {
    return {
      model: null,
      omitTaskModel: true,
      source: 'parent-chat (slug not in Task allowlist)',
      raw,
      warning: `slug "${raw}" not in forge-models Task allowlist; omitting Task model`,
    }
  }

  return { model: raw, omitTaskModel: false, source: 'forge-models.mdc', raw }
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
  const resolved = resolveModel(cfg.role, roleToModel, allowed)
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
