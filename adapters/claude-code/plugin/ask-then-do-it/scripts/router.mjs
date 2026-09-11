import { createHash, randomBytes } from "node:crypto";
import { constants as fsConstants } from "node:fs";
import { link, lstat, mkdir, open, readdir, rename, unlink } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";


const PLUGIN = "ask-then-do-it";
const VERSION = "1.4.1";
const STATE_SCHEMA_VERSION = 1;
const MINIMUM_NODE_MAJOR = 22;
const MAPPING_SEMANTIC_SHA256 = "bcfde7bc67cd286bae822dbf9993e68263a385c244ffb5e3b9353d2418504d78";
const MAPPING_KEYS = new Set([
  "schema_version",
  "release_version",
  "evidence_checked_on",
  "lookup_mode",
  "unknown_classification",
  "sources",
  "classifications",
]);
const MAPPING_SOURCE_IDS = new Set([
  "models-overview",
  "model-ids-and-versions",
  "model-deprecations",
  "claude-code-model-config",
]);
const MAPPING_SOURCE_KEYS = new Set(["url", "checked_on"]);
const MAPPING_CLASSIFICATION_COUNTS = new Map([
  ["claude-5", 4],
  ["supported-non-5", 4],
  ["unsupported", 22],
]);
const ROUTE_FRAME_START = "ASK_THEN_DO_IT_ROUTE_ENVELOPE_V1";
const ROUTE_FRAME_END = "END_ASK_THEN_DO_IT_ROUTE_ENVELOPE_V1";
const AUTOMATIC_COMMAND = "ask-then-do-it:ask-then-do-it";
const AUTOMATIC_ENTRY = `/${AUTOMATIC_COMMAND}`;
const EXPLICIT_COMMAND = "ask-then-do-it:ask-then-do-it-5";
const EXPLICIT_ENTRY = `/${EXPLICIT_COMMAND}`;
const ROUTER_DIRECTORY = path.dirname(fileURLToPath(import.meta.url));
const MAPPING_PATH = path.resolve(ROUTER_DIRECTORY, "..", "config", "model-classifications.json");

const CLASSIFICATIONS = new Set([
  "claude-5",
  "supported-non-5",
  "unsupported",
  "unknown",
]);
const SESSION_SOURCES = new Set(["startup", "resume", "clear", "compact", "fork"]);
const REQUESTED_SWITCH_SOURCES = new Set(["command", "picker", "sdk"]);
const AUTOMATIC_SWITCH_SOURCES = new Set(["auto", "resume"]);
const STATE_KEYS = new Set([
  "schema_version",
  "session_key",
  "session_source",
  "routing_status",
  "model_generation",
  "model_id",
  "model_classification",
  "model_observed_from",
  "pending_switch",
  "updated_at",
  "operation",
]);
const PENDING_SWITCH_KEYS = new Set([
  "next_generation",
  "from_model",
  "source",
  "started_at",
]);
const OPERATION_KEYS = new Set([
  "operation_id",
  "entry",
  "bound_profile",
  "bound_classification",
  "started_at",
]);
const UTC_TIMESTAMP = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/;
const OPERATION_ID = /^op_[0-9a-f]{32}$/;
const SESSION_FILENAME = /^([0-9a-f]{64})\.json$/;
const CONTROL_CHARACTER = /[\u0000-\u001f\u007f-\u009f]/u;
const CANONICAL_MODEL_ID = /^claude-[a-z0-9.]+(?:-[a-z0-9.]+)*$/;
const CORRELATABLE_FUTURE_MODEL_ID = /^claude-(?:(?:opus|sonnet|haiku|fable)-[1-9]\d*(?:-\d{1,2})?|[1-9]\d*(?:-\d{1,2})?-(?:opus|sonnet|haiku|fable)|[1-9]\d*(?:\.\d+)+)$/;
const MAX_STDIN_BYTES = 65_536;
const MAX_SESSION_ID_BYTES = 4_096;
const MAX_TEXT_BYTES = 65_536;
const MAX_MAPPING_BYTES = 65_536;
const MAX_STATE_BYTES = 16_384;
const MAX_LOCK_RECORD_BYTES = 1_024;
const SESSION_MAX_AGE_MS = 30 * 24 * 60 * 60 * 1_000;
const LOCK_SCHEMA_VERSION = 1;
const LOCK_LEASE_MS = 30_000;
const LOCK_RECLAIM_GRACE_MS = 30_000;
const LOCK_RECORD_TOKEN = /^[0-9a-f]{32}$/;
const LOCK_RECORD_KEYS = new Set([
  "schema_version",
  "owner_token",
  "pid",
  "created_at",
  "lease_until",
]);
const LOCK_RETRY_COUNT = 100;
const LOCK_RETRY_MS = 10;
const EFFORT_LEVELS = new Set(["low", "medium", "high", "xhigh", "max"]);
const EXPANSION_TYPES = new Set(["slash_command", "mcp_prompt"]);
const CACHE_TTLS = new Set(["5m", "1h"]);
const PRICING_SOURCES = new Set(["configured", "catalog", "default"]);
const COMMON_EVENT_KEYS = new Set([
  "session_id",
  "prompt_id",
  "transcript_path",
  "cwd",
  "permission_mode",
  "effort",
  "hook_event_name",
  "agent_id",
  "agent_type",
]);
const SESSION_START_EVENT_KEYS = new Set([
  ...COMMON_EVENT_KEYS,
  "source",
  "model",
  "session_title",
  "seconds_since_last_response",
  "context_tokens",
  "prompt_cache_likely_expired",
  "estimated_cache_write_usd",
]);
const EXPANSION_EVENT_KEYS = new Set([
  ...COMMON_EVENT_KEYS,
  "expansion_type",
  "command_name",
  "command_args",
  "command_source",
  "prompt",
]);
const SWITCH_EVENT_KEYS = new Set([
  ...COMMON_EVENT_KEYS,
  "from_model",
  "to_model",
  "requested_model",
  "source",
  "context_tokens",
  "prompt_cache_warm",
  "cache_ttl",
  "estimated_cache_write_usd",
  "pricing",
]);
const READY_OPERATION_TUPLES = new Set([
  `${AUTOMATIC_ENTRY}|claude-5|claude-5`,
  `${AUTOMATIC_ENTRY}|supported-non-5|general`,
  `${AUTOMATIC_ENTRY}|unknown|general`,
  `${EXPLICIT_ENTRY}|claude-5|claude-5`,
  `${EXPLICIT_ENTRY}|supported-non-5|general`,
  `${EXPLICIT_ENTRY}|unknown|claude-5`,
]);
const READY_DISCLOSURE_CODES = new Set([
  "none",
  "non-claude-5-explicit-general",
  "unknown-model-explicit-claude-5",
  "unknown-model-general-compatibility",
]);
const FAILURE_DISCLOSURE_CODES = new Set([
  "command-identity-invalid",
  "internal-error",
  "invalid-hook-input",
  "mapping-invalid",
  "node-too-old",
  "state-indeterminate",
  "state-invalid",
  "state-missing",
  "state-ownership-mismatch",
  "state-pending",
  "state-read-failed",
  "state-schema-unsupported",
  "state-stale",
  "state-write-failed",
  "transition-invalid",
  "unsupported-model",
]);


export class RouterError extends Error {
  constructor(code) {
    super(code);
    this.name = "RouterError";
    this.code = code;
  }
}


function requireObject(value, code = "invalid-hook-input") {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new RouterError(code);
  }
  return value;
}


function isWellFormedString(value) {
  for (let index = 0; index < value.length; index += 1) {
    const codeUnit = value.charCodeAt(index);
    if (codeUnit >= 0xd800 && codeUnit <= 0xdbff) {
      const next = value.charCodeAt(index + 1);
      if (!(next >= 0xdc00 && next <= 0xdfff)) {
        return false;
      }
      index += 1;
    } else if (codeUnit >= 0xdc00 && codeUnit <= 0xdfff) {
      return false;
    }
  }
  return true;
}


function requireString(value, code = "invalid-hook-input") {
  if (
    typeof value !== "string" ||
    value.length === 0 ||
    !isWellFormedString(value) ||
    CONTROL_CHARACTER.test(value)
  ) {
    throw new RouterError(code);
  }
  return value;
}


function requireIdentifier(value, { code = "invalid-hook-input", maximum = MAX_TEXT_BYTES } = {}) {
  requireString(value, code);
  if (Buffer.byteLength(value, "utf8") > maximum) {
    throw new RouterError(code);
  }
  return value;
}


function correlatableModelIdOrNull(value, mapping) {
  requireIdentifier(value, { maximum: 512 });
  return CANONICAL_MODEL_ID.test(value) && (
    Object.hasOwn(mapping, value) || CORRELATABLE_FUTURE_MODEL_ID.test(value)
  ) ? value : null;
}


function isCorrelatableModelId(value, mapping) {
  return typeof value === "string" && CANONICAL_MODEL_ID.test(value) && (
    Object.hasOwn(mapping, value) || CORRELATABLE_FUTURE_MODEL_ID.test(value)
  );
}


function hasExactKeys(value, expected) {
  const actual = Object.keys(value);
  return actual.length === expected.size && actual.every((key) => expected.has(key));
}


function isUtcTimestamp(value) {
  if (typeof value !== "string" || !UTC_TIMESTAMP.test(value)) {
    return false;
  }
  const milliseconds = Date.parse(value);
  return Number.isFinite(milliseconds) && new Date(milliseconds).toISOString() === value;
}


function requireBoundedText(value, { allowEmpty = true, maximum = MAX_TEXT_BYTES } = {}) {
  if (
    typeof value !== "string" ||
    (!allowEmpty && value.length === 0) ||
    value.includes("\0") ||
    Buffer.byteLength(value, "utf8") > maximum
  ) {
    throw new RouterError("invalid-hook-input");
  }
  return value;
}


function requireOptionalFiniteNumber(event, key) {
  if (event[key] !== undefined && (
    typeof event[key] !== "number" || !Number.isFinite(event[key])
  )) {
    throw new RouterError("invalid-hook-input");
  }
}


function requireOptionalBoolean(event, key) {
  if (event[key] !== undefined && typeof event[key] !== "boolean") {
    throw new RouterError("invalid-hook-input");
  }
}


function requireOptionalEnum(event, key, values) {
  if (event[key] !== undefined && !values.has(event[key])) {
    throw new RouterError("invalid-hook-input");
  }
}


function validateOptionalEffort(effort) {
  if (effort === undefined) {
    return;
  }
  const value = requireObject(effort);
  if (!hasExactKeys(value, new Set(["level"])) || !EFFORT_LEVELS.has(value.level)) {
    throw new RouterError("invalid-hook-input");
  }
}


export function parseJsonStrict(source, code = "invalid-hook-input") {
  if (typeof source !== "string") {
    throw new RouterError(code);
  }
  let index = 0;
  const fail = () => {
    throw new RouterError(code);
  };
  const skipWhitespace = () => {
    while (/[\t\n\r ]/.test(source[index] ?? "")) {
      index += 1;
    }
  };
  const parseString = () => {
    if (source[index] !== '"') {
      fail();
    }
    const start = index;
    index += 1;
    let escaped = false;
    while (index < source.length) {
      const character = source[index];
      if (escaped) {
        escaped = false;
      } else if (character === "\\") {
        escaped = true;
      } else if (character === '"') {
        index += 1;
        try {
          return JSON.parse(source.slice(start, index));
        } catch {
          fail();
        }
      }
      index += 1;
    }
    fail();
  };
  const parseValue = () => {
    skipWhitespace();
    const character = source[index];
    if (character === '"') {
      return parseString();
    }
    if (character === "{") {
      index += 1;
      skipWhitespace();
      const value = Object.create(null);
      const keys = new Set();
      if (source[index] === "}") {
        index += 1;
        return value;
      }
      while (index < source.length) {
        skipWhitespace();
        const key = parseString();
        if (keys.has(key)) {
          fail();
        }
        keys.add(key);
        skipWhitespace();
        if (source[index] !== ":") {
          fail();
        }
        index += 1;
        value[key] = parseValue();
        skipWhitespace();
        if (source[index] === "}") {
          index += 1;
          return value;
        }
        if (source[index] !== ",") {
          fail();
        }
        index += 1;
      }
      fail();
    }
    if (character === "[") {
      index += 1;
      skipWhitespace();
      const value = [];
      if (source[index] === "]") {
        index += 1;
        return value;
      }
      while (index < source.length) {
        value.push(parseValue());
        skipWhitespace();
        if (source[index] === "]") {
          index += 1;
          return value;
        }
        if (source[index] !== ",") {
          fail();
        }
        index += 1;
      }
      fail();
    }
    for (const [token, value] of [["true", true], ["false", false], ["null", null]]) {
      if (source.startsWith(token, index)) {
        index += token.length;
        return value;
      }
    }
    const number = source.slice(index).match(/^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/);
    if (number !== null) {
      index += number[0].length;
      return Number(number[0]);
    }
    fail();
  };
  try {
    const value = parseValue();
    skipWhitespace();
    if (index !== source.length) {
      fail();
    }
    return value;
  } catch (error) {
    if (error instanceof RouterError) {
      throw error;
    }
    throw new RouterError(code);
  }
}


function validateEvent(event, action) {
  requireObject(event);
  const allowed = action === "session-start"
    ? SESSION_START_EVENT_KEYS
    : action === "user-prompt-expansion"
      ? EXPANSION_EVENT_KEYS
      : SWITCH_EVENT_KEYS;
  if (Object.keys(event).some((key) => !allowed.has(key))) {
    throw new RouterError("invalid-hook-input");
  }
  requireIdentifier(event.session_id, { maximum: MAX_SESSION_ID_BYTES });
  requireBoundedText(event.hook_event_name, { allowEmpty: false, maximum: 64 });
  for (const key of ["prompt_id", "transcript_path", "cwd", "permission_mode", "agent_id", "agent_type"]) {
    if (event[key] !== undefined) {
      requireBoundedText(event[key]);
    }
  }
  validateOptionalEffort(event.effort);
  if (action === "session-start") {
    requireBoundedText(event.source, { allowEmpty: false, maximum: 32 });
    if (event.model !== undefined) {
      requireIdentifier(event.model, { maximum: 512 });
    }
    if (event.session_title !== undefined) {
      requireBoundedText(event.session_title);
    }
    for (const key of [
      "seconds_since_last_response",
      "context_tokens",
      "estimated_cache_write_usd",
    ]) {
      requireOptionalFiniteNumber(event, key);
    }
    requireOptionalBoolean(event, "prompt_cache_likely_expired");
  } else if (action === "user-prompt-expansion") {
    for (const key of ["expansion_type", "command_name", "command_args", "command_source", "prompt"]) {
      requireBoundedText(event[key], { allowEmpty: key === "command_args" });
    }
    requireOptionalEnum(event, "expansion_type", EXPANSION_TYPES);
  } else {
    for (const key of ["from_model", "to_model", "source"]) {
      requireIdentifier(event[key], { maximum: 512 });
    }
    if (event.requested_model !== undefined && event.requested_model !== null) {
      requireIdentifier(event.requested_model, { maximum: 512 });
    }
    for (const key of ["context_tokens", "estimated_cache_write_usd"]) {
      requireOptionalFiniteNumber(event, key);
    }
    requireOptionalBoolean(event, "prompt_cache_warm");
    requireOptionalEnum(event, "cache_ttl", CACHE_TTLS);
    requireOptionalEnum(event, "pricing", PRICING_SOURCES);
  }
  return event;
}


export function sessionKey(sessionId) {
  return createHash("sha256").update(requireString(sessionId), "utf8").digest("hex");
}


export function checkNodeVersion(version) {
  if (typeof version !== "string" || !/^\d+\.\d+\.\d+(?:[-+].*)?$/.test(version)) {
    throw new RouterError("node-too-old");
  }
  const major = Number.parseInt(version.split(".", 1)[0], 10);
  if (!Number.isSafeInteger(major) || major < MINIMUM_NODE_MAJOR) {
    throw new RouterError("node-too-old");
  }
}


export async function readBoundedHandle(handle, maximumBytes, code) {
  if (!Number.isSafeInteger(maximumBytes) || maximumBytes < 0) {
    throw new RouterError(code);
  }
  const buffer = Buffer.alloc(maximumBytes + 1);
  let total = 0;
  try {
    while (total < buffer.length) {
      const result = await handle.read(buffer, total, buffer.length - total, null);
      if (!Number.isSafeInteger(result?.bytesRead) || result.bytesRead < 0) {
        throw new RouterError(code);
      }
      if (result.bytesRead === 0) {
        break;
      }
      total += result.bytesRead;
    }
  } catch (error) {
    if (error instanceof RouterError) {
      throw error;
    }
    throw new RouterError(code);
  }
  if (total > maximumBytes) {
    throw new RouterError(code);
  }
  try {
    return new TextDecoder("utf-8", { fatal: true }).decode(buffer.subarray(0, total));
  } catch {
    throw new RouterError(code);
  }
}


async function readBoundedRegularFile(pathname, maximumBytes, code) {
  let handle;
  try {
    handle = await open(pathname, fsConstants.O_RDONLY);
    const information = await handle.stat();
    if (!information.isFile() || information.size > maximumBytes) {
      throw new RouterError(code);
    }
    return await readBoundedHandle(handle, maximumBytes, code);
  } catch (error) {
    if (error instanceof RouterError) {
      throw error;
    }
    throw new RouterError(code);
  } finally {
    if (handle !== undefined) {
      await handle.close().catch(() => {});
    }
  }
}


async function readJson(pathname, code) {
  const source = await readBoundedRegularFile(pathname, MAX_MAPPING_BYTES, code);
  return requireObject(parseJsonStrict(source, code), code);
}


function canonicalJson(value) {
  if (Array.isArray(value)) {
    return `[${value.map((item) => canonicalJson(item)).join(",")}]`;
  }
  if (value !== null && typeof value === "object") {
    return `{${Object.keys(value).sort().map(
      (key) => `${JSON.stringify(key)}:${canonicalJson(value[key])}`,
    ).join(",")}}`;
  }
  return JSON.stringify(value);
}


export async function loadMapping(mappingPath = MAPPING_PATH) {
  const mapping = await readJson(mappingPath, "mapping-invalid");
  if (
    !hasExactKeys(mapping, MAPPING_KEYS) ||
    mapping.schema_version !== 1 ||
    mapping.release_version !== VERSION ||
    mapping.evidence_checked_on !== "2026-09-07" ||
    mapping.lookup_mode !== "exact" ||
    mapping.unknown_classification !== "unknown"
  ) {
    throw new RouterError("mapping-invalid");
  }
  const sources = requireObject(mapping.sources, "mapping-invalid");
  if (!hasExactKeys(sources, MAPPING_SOURCE_IDS)) {
    throw new RouterError("mapping-invalid");
  }
  for (const source of Object.values(sources)) {
    requireObject(source, "mapping-invalid");
    if (
      !hasExactKeys(source, MAPPING_SOURCE_KEYS) ||
      source.checked_on !== mapping.evidence_checked_on ||
      !requireString(source.url, "mapping-invalid").startsWith("https://")
    ) {
      throw new RouterError("mapping-invalid");
    }
  }
  const classifications = requireObject(mapping.classifications, "mapping-invalid");
  const counts = new Map([...MAPPING_CLASSIFICATION_COUNTS.keys()].map((key) => [key, 0]));
  for (const [modelId, classification] of Object.entries(classifications)) {
    requireString(modelId, "mapping-invalid");
    if (
      !CANONICAL_MODEL_ID.test(modelId) ||
      !MAPPING_CLASSIFICATION_COUNTS.has(classification)
    ) {
      throw new RouterError("mapping-invalid");
    }
    counts.set(classification, counts.get(classification) + 1);
  }
  if (
    Object.keys(classifications).length !== 30 ||
    [...MAPPING_CLASSIFICATION_COUNTS].some(
      ([classification, expected]) => counts.get(classification) !== expected,
    )
  ) {
    throw new RouterError("mapping-invalid");
  }
  const digest = createHash("sha256").update(canonicalJson(mapping), "utf8").digest("hex");
  if (digest !== MAPPING_SEMANTIC_SHA256) {
    throw new RouterError("mapping-invalid");
  }
  return classifications;
}


export function classifyExact(modelId, mapping) {
  if (modelId === null) {
    return "unknown";
  }
  requireString(modelId);
  return Object.hasOwn(mapping, modelId) ? mapping[modelId] : "unknown";
}


function statePath(pluginData, key) {
  const supplied = requireString(pluginData, "state-write-failed");
  if (!path.isAbsolute(supplied)) {
    throw new RouterError("state-write-failed");
  }
  const root = path.resolve(supplied);
  return path.join(root, "routing", "v1", "sessions", `${key}.json`);
}


async function assertNoLinkedAncestors(pathname) {
  const resolved = path.resolve(pathname);
  const parsed = path.parse(resolved);
  const parts = resolved.slice(parsed.root.length).split(path.sep).filter(Boolean);
  let current = parsed.root;
  for (const part of parts) {
    current = path.join(current, part);
    let information;
    try {
      information = await lstat(current);
    } catch (error) {
      if (error?.code === "ENOENT") {
        return;
      }
      throw new RouterError("state-read-failed");
    }
    if (information.isSymbolicLink()) {
      throw new RouterError("state-read-failed");
    }
  }
}


async function ensureStateDirectory(directory) {
  await assertNoLinkedAncestors(directory);
  try {
    await mkdir(directory, { recursive: true, mode: 0o700 });
  } catch {
    throw new RouterError("state-write-failed");
  }
  await assertNoLinkedAncestors(directory);
  const information = await lstat(directory).catch(() => null);
  if (information === null || !information.isDirectory() || information.isSymbolicLink()) {
    throw new RouterError("state-write-failed");
  }
}


function wait(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}


function lockRecord(ownerToken, now = new Date()) {
  return {
    schema_version: LOCK_SCHEMA_VERSION,
    owner_token: ownerToken,
    pid: process.pid,
    created_at: now.toISOString(),
    lease_until: new Date(now.getTime() + LOCK_LEASE_MS).toISOString(),
  };
}


function validateLockRecord(value) {
  requireObject(value, "state-write-failed");
  if (
    !hasExactKeys(value, LOCK_RECORD_KEYS) ||
    value.schema_version !== LOCK_SCHEMA_VERSION ||
    typeof value.owner_token !== "string" ||
    !LOCK_RECORD_TOKEN.test(value.owner_token) ||
    !Number.isSafeInteger(value.pid) ||
    value.pid <= 0 ||
    !isUtcTimestamp(value.created_at) ||
    !isUtcTimestamp(value.lease_until) ||
    Date.parse(value.lease_until) < Date.parse(value.created_at)
  ) {
    throw new RouterError("state-write-failed");
  }
  return value;
}


async function inspectLockRecord(lockPath) {
  try {
    await assertNoLinkedAncestors(lockPath);
    const information = await lstat(lockPath);
    if (!information.isFile() || information.isSymbolicLink()) {
      return null;
    }
    const source = await readBoundedRegularFile(
      lockPath,
      MAX_LOCK_RECORD_BYTES,
      "state-write-failed",
    );
    const record = validateLockRecord(parseJsonStrict(source, "state-write-failed"));
    return { record, information };
  } catch {
    return null;
  }
}


function processIsDefinitelyDead(pid) {
  try {
    process.kill(pid, 0);
    return false;
  } catch (error) {
    return error?.code === "ESRCH";
  }
}


function isRecoverableLock(candidate, now = new Date()) {
  if (candidate === null) {
    return false;
  }
  const leaseUntil = Date.parse(candidate.record.lease_until);
  const modifiedAt = candidate.information.mtimeMs;
  return (
    Number.isFinite(leaseUntil) &&
    Number.isFinite(modifiedAt) &&
    now.getTime() > leaseUntil + LOCK_RECLAIM_GRACE_MS &&
    now.getTime() > modifiedAt + LOCK_RECLAIM_GRACE_MS &&
    processIsDefinitelyDead(candidate.record.pid)
  );
}


async function moveAndRemoveOwnedRecord(pathname, ownerToken, purpose) {
  const current = await inspectLockRecord(pathname);
  if (current === null || current.record.owner_token !== ownerToken) {
    return false;
  }
  const quarantine = path.join(
    path.dirname(pathname),
    `.${path.basename(pathname)}.${purpose}.${ownerToken}.${randomBytes(8).toString("hex")}`,
  );
  try {
    await rename(pathname, quarantine);
  } catch {
    return false;
  }
  const moved = await inspectLockRecord(quarantine);
  if (moved === null || moved.record.owner_token !== ownerToken) {
    await rename(quarantine, pathname).catch(() => {});
    return false;
  }
  try {
    await unlink(quarantine);
    return true;
  } catch {
    await rename(quarantine, pathname).catch(() => {});
    return false;
  }
}


async function createOwnedRecord(pathname, ownerToken) {
  const prepared = `${pathname}.prepare-${ownerToken}-${randomBytes(8).toString("hex")}`;
  let handle;
  try {
    handle = await open(
      prepared,
      fsConstants.O_CREAT | fsConstants.O_EXCL | fsConstants.O_WRONLY,
      0o600,
    );
    await handle.writeFile(JSON.stringify(lockRecord(ownerToken)), "utf8");
    await handle.sync();
    await handle.close();
    handle = undefined;
    await link(prepared, pathname);
  } catch (error) {
    if (handle !== undefined) {
      await handle.close().catch(() => {});
    }
    throw error;
  } finally {
    await unlink(prepared).catch(() => {});
  }
}


async function acquireRecoveryGuard(lockPath, targetToken) {
  const guardPath = `${lockPath}.recover-${targetToken}`;
  for (let attempt = 0; attempt < 2; attempt += 1) {
    const ownerToken = randomBytes(16).toString("hex");
    try {
      await createOwnedRecord(guardPath, ownerToken);
      return { guardPath, ownerToken };
    } catch (error) {
      if (error?.code !== "EEXIST") {
        return null;
      }
      const existing = await inspectLockRecord(guardPath);
      if (!isRecoverableLock(existing)) {
        return null;
      }
      await moveAndRemoveOwnedRecord(
        guardPath,
        existing.record.owner_token,
        "stale-recovery-guard",
      );
    }
  }
  return null;
}


async function tryRecoverStaleLock(lockPath) {
  const observed = await inspectLockRecord(lockPath);
  if (!isRecoverableLock(observed)) {
    return false;
  }
  const targetToken = observed.record.owner_token;
  const guard = await acquireRecoveryGuard(lockPath, targetToken);
  if (guard === null) {
    return false;
  }
  try {
    const currentGuard = await inspectLockRecord(guard.guardPath);
    const currentLock = await inspectLockRecord(lockPath);
    if (
      currentGuard === null ||
      currentGuard.record.owner_token !== guard.ownerToken ||
      currentLock === null ||
      currentLock.record.owner_token !== targetToken ||
      !isRecoverableLock(currentLock)
    ) {
      return false;
    }
    return await moveAndRemoveOwnedRecord(lockPath, targetToken, "stale-lock");
  } finally {
    await moveAndRemoveOwnedRecord(
      guard.guardPath,
      guard.ownerToken,
      "recovery-guard-release",
    );
  }
}


export async function withSessionLock(
  pathname,
  callback,
  { retryCount = LOCK_RETRY_COUNT, allowReclaim = true } = {},
) {
  const directory = path.dirname(pathname);
  await ensureStateDirectory(directory);
  const lockPath = path.join(directory, `.${path.basename(pathname)}.lock`);
  let ownerToken;
  for (let attempt = 0; attempt <= retryCount; attempt += 1) {
    let candidateToken = randomBytes(16).toString("hex");
    try {
      await createOwnedRecord(lockPath, candidateToken);
      ownerToken = candidateToken;
      break;
    } catch (error) {
      if (error?.code !== "EEXIST") {
        throw new RouterError("state-write-failed");
      }
      if (allowReclaim && await tryRecoverStaleLock(lockPath)) {
        candidateToken = randomBytes(16).toString("hex");
        try {
          await createOwnedRecord(lockPath, candidateToken);
          ownerToken = candidateToken;
          break;
        } catch (reacquireError) {
          if (reacquireError?.code !== "EEXIST") {
            throw new RouterError("state-write-failed");
          }
        }
      }
      if (attempt === retryCount) {
        throw new RouterError("state-write-failed");
      }
      await wait(LOCK_RETRY_MS);
    }
  }
  if (ownerToken === undefined) {
    throw new RouterError("state-write-failed");
  }
  try {
    return await callback();
  } finally {
    if (ownerToken !== undefined) {
      await moveAndRemoveOwnedRecord(lockPath, ownerToken, "lock-release");
    }
  }
}


async function atomicWriteJson(pathname, value) {
  const directory = path.dirname(pathname);
  await ensureStateDirectory(directory);
  const temporary = path.join(
    directory,
    `.${path.basename(pathname)}.${process.pid}.${randomBytes(8).toString("hex")}.tmp`,
  );
  let handle;
  try {
    handle = await open(
      temporary,
      fsConstants.O_CREAT | fsConstants.O_EXCL | fsConstants.O_WRONLY,
      0o600,
    );
    await handle.writeFile(`${JSON.stringify(value)}\n`, "utf8");
    await handle.sync();
    await handle.close();
    handle = undefined;
    await rename(temporary, pathname);
  } catch {
    throw new RouterError("state-write-failed");
  } finally {
    if (handle !== undefined) {
      await handle.close().catch(() => {});
    }
    await unlink(temporary).catch(() => {});
  }
}


export function validateState(state, expectedKey, mapping = null) {
  requireObject(state, "state-invalid");
  if (!hasExactKeys(state, STATE_KEYS)) {
    throw new RouterError("state-invalid");
  }
  if (state.schema_version !== STATE_SCHEMA_VERSION) {
    throw new RouterError("state-schema-unsupported");
  }
  if (state.session_key !== expectedKey) {
    throw new RouterError("state-ownership-mismatch");
  }
  if (
    !SESSION_SOURCES.has(state.session_source) ||
    !new Set(["ready", "pending", "indeterminate"]).has(state.routing_status) ||
    !Number.isSafeInteger(state.model_generation) ||
    state.model_generation < 0 ||
    (state.model_id !== null && (
      typeof state.model_id !== "string" ||
      !CANONICAL_MODEL_ID.test(state.model_id)
    )) ||
    !CLASSIFICATIONS.has(state.model_classification) ||
    !new Set(["SessionStart", "PostModelSwitch", null]).has(state.model_observed_from) ||
    typeof state.updated_at !== "string" ||
    !isUtcTimestamp(state.updated_at)
  ) {
    throw new RouterError("state-invalid");
  }
  if (state.model_id !== null) {
    requireIdentifier(state.model_id, { code: "state-invalid", maximum: 512 });
  }
  if (
    (state.model_id === null && state.model_classification !== "unknown") ||
    (mapping !== null && state.model_id !== null && !isCorrelatableModelId(state.model_id, mapping)) ||
    (mapping !== null && classifyExact(state.model_id, mapping) !== state.model_classification) ||
    (state.model_observed_from === null && state.model_id !== null) ||
    (state.model_observed_from !== null && state.model_id === null) ||
    (state.routing_status === "indeterminate" && (
      state.model_id !== null ||
      state.model_classification !== "unknown" ||
      state.model_observed_from !== null
    ))
  ) {
    throw new RouterError("state-invalid");
  }
  if (state.pending_switch === null) {
    if (state.routing_status === "pending") {
      throw new RouterError("state-invalid");
    }
  } else {
    const pending = requireObject(state.pending_switch, "state-invalid");
    if (
      !hasExactKeys(pending, PENDING_SWITCH_KEYS) ||
      state.routing_status !== "pending" ||
      pending.next_generation !== state.model_generation + 1 ||
      !Number.isSafeInteger(pending.next_generation) ||
      typeof pending.from_model !== "string" ||
      !CANONICAL_MODEL_ID.test(pending.from_model) ||
      (state.model_id !== null && pending.from_model !== state.model_id) ||
      !REQUESTED_SWITCH_SOURCES.has(pending.source) ||
      typeof pending.started_at !== "string" ||
      !isUtcTimestamp(pending.started_at)
    ) {
      throw new RouterError("state-invalid");
    }
    requireIdentifier(pending.from_model, { code: "state-invalid", maximum: 512 });
    if (mapping !== null && !isCorrelatableModelId(pending.from_model, mapping)) {
      throw new RouterError("state-invalid");
    }
  }
  if (state.operation !== null) {
    const operation = requireObject(state.operation, "state-invalid");
    if (
      !hasExactKeys(operation, OPERATION_KEYS) ||
      typeof operation.operation_id !== "string" ||
      !OPERATION_ID.test(operation.operation_id) ||
      !new Set([AUTOMATIC_ENTRY, EXPLICIT_ENTRY]).has(operation.entry) ||
      !new Set(["general", "claude-5"]).has(operation.bound_profile) ||
      !CLASSIFICATIONS.has(operation.bound_classification) ||
      typeof operation.started_at !== "string" ||
      !isUtcTimestamp(operation.started_at)
    ) {
      throw new RouterError("state-invalid");
    }
    const tuple = [
      operation.entry,
      operation.bound_classification,
      operation.bound_profile,
    ].join("|");
    if (!READY_OPERATION_TUPLES.has(tuple)) {
      throw new RouterError("state-invalid");
    }
  }
  return state;
}


async function readState(
  pathname,
  expectedKey,
  allowMissing = false,
  allowStale = false,
  mapping = null,
) {
  await assertNoLinkedAncestors(pathname);
  let source;
  try {
    const information = await lstat(pathname);
    if (!information.isFile() || information.isSymbolicLink()) {
      throw new RouterError("state-read-failed");
    }
    source = await readBoundedRegularFile(pathname, MAX_STATE_BYTES, "state-invalid");
  } catch (error) {
    if (error instanceof RouterError) {
      throw error;
    }
    if (allowMissing && error?.code === "ENOENT") {
      return null;
    }
    throw new RouterError(error?.code === "ENOENT" ? "state-missing" : "state-read-failed");
  }
  let state;
  try {
    state = parseJsonStrict(source, "state-invalid");
  } catch {
    throw new RouterError("state-invalid");
  }
  const validated = validateState(state, expectedKey, mapping);
  if (
    !allowStale &&
    Date.now() - Date.parse(validated.updated_at) > SESSION_MAX_AGE_MS
  ) {
    throw new RouterError("state-stale");
  }
  return validated;
}


async function cleanupExpiredSessions(directory, currentKey, now, mapping) {
  let entries;
  try {
    entries = await readdir(directory, { withFileTypes: true });
  } catch {
    return;
  }
  for (const entry of entries) {
    const match = SESSION_FILENAME.exec(entry.name);
    if (match === null || match[1] === currentKey || !entry.isFile() || entry.isSymbolicLink()) {
      continue;
    }
    const pathname = path.join(directory, entry.name);
    try {
      await withSessionLock(pathname, async () => {
        const candidate = await readState(pathname, match[1], false, true, mapping);
        const updatedAt = Date.parse(candidate.updated_at);
        if (Number.isFinite(updatedAt) && now.getTime() - updatedAt > SESSION_MAX_AGE_MS) {
          await unlink(pathname);
        }
      }, { retryCount: 0, allowReclaim: false });
    } catch {
      // Invalid, linked, or concurrently changing files are retained for diagnosis.
    }
  }
}


function operationFor(entry, profile, classification, now = new Date()) {
  return {
    operation_id: `op_${randomBytes(16).toString("hex")}`,
    entry,
    bound_profile: profile,
    bound_classification: classification,
    started_at: now.toISOString(),
  };
}


function successEnvelope(entry, operation, classification, profile, disclosureCode) {
  const tuple = [entry, classification, profile].join("|");
  if (!READY_OPERATION_TUPLES.has(tuple) || !READY_DISCLOSURE_CODES.has(disclosureCode)) {
    throw new RouterError("internal-error");
  }
  return {
    plugin: PLUGIN,
    version: VERSION,
    entry,
    operation_id: operation.operation_id,
    model_classification: classification,
    selected_profile: profile,
    routing_status: "ready",
    disclosure_code: disclosureCode,
  };
}


function failureEnvelope(entry, classification, code) {
  const disclosureCode = FAILURE_DISCLOSURE_CODES.has(code) ? code : "internal-error";
  return {
    plugin: PLUGIN,
    version: VERSION,
    entry,
    operation_id: null,
    model_classification: classification,
    selected_profile: null,
    routing_status: "failure",
    disclosure_code: disclosureCode,
  };
}


function writeRouteEnvelope(envelope) {
  const additionalContext = [
    ROUTE_FRAME_START,
    JSON.stringify(envelope),
    ROUTE_FRAME_END,
  ].join("\n");
  process.stdout.write(
    JSON.stringify({
      hookSpecificOutput: {
        hookEventName: "UserPromptExpansion",
        additionalContext,
      },
    }),
  );
}


function writeHookOutput(hookEventName, { additionalContext, systemMessage } = {}) {
  const output = {};
  if (systemMessage !== undefined) {
    output.systemMessage = systemMessage;
  }
  if (additionalContext !== undefined) {
    output.hookSpecificOutput = { hookEventName, additionalContext };
  }
  process.stdout.write(JSON.stringify(output));
}


function continuationContext(operation, unsupported = false, postSynchronized = false) {
  const lines = [
    "ASK_THEN_DO_IT_OPERATION_BINDING_V1",
    `operation_id=${operation.operation_id}`,
    `bound_profile=${operation.bound_profile}`,
    "If this operation is still in progress, keep its bound profile and reload only the needed modules from that same profile; use workflow artifacts or conversation evidence to decide what must be reloaded. Do not reroute until the next public entry.",
  ];
  if (unsupported) {
    lines.push("The active model has left formal Ask Then Do It model support; the current operation profile remains unchanged.");
  }
  if (postSynchronized) {
    lines.push("Tell the user that the active model changed and the routing state is synchronized; the current operation profile remains unchanged, and only the next permitted public entry reroutes.");
  }
  return lines.join("\n");
}


function incrementGeneration(generation) {
  if (!Number.isSafeInteger(generation) || generation >= Number.MAX_SAFE_INTEGER) {
    throw new RouterError("transition-invalid");
  }
  return generation + 1;
}


async function handleSessionStart(event, pluginData, mapping) {
  if (event.hook_event_name !== "SessionStart" || !SESSION_SOURCES.has(event.source)) {
    throw new RouterError("invalid-hook-input");
  }
  const key = sessionKey(event.session_id);
  const pathname = statePath(pluginData, key);
  const modelWasOmitted = event.model === undefined;
  const modelId = modelWasOmitted ? null : correlatableModelIdOrNull(event.model, mapping);
  const now = new Date();
  let prior = null;
  if (!new Set(["startup", "fork"]).has(event.source)) {
    prior = await readState(pathname, key, true, event.source === "clear", mapping);
  }
  if (event.source === "compact" && prior !== null && modelWasOmitted && prior.routing_status !== "ready") {
    throw new RouterError(`state-${prior.routing_status}`);
  }
  const preserveOperation = new Set(["resume", "compact"]).has(event.source) && prior !== null;
  const preserveModel = event.source === "compact" && modelWasOmitted && prior !== null;
  let generation;
  try {
    generation = prior === null
      ? 0
      : preserveModel
        ? prior.model_generation
        : incrementGeneration(prior.model_generation);
  } catch (error) {
    if (prior !== null && error instanceof RouterError && error.code === "transition-invalid") {
      await markIndeterminate(pathname, prior);
    }
    throw error;
  }
  const state = {
    schema_version: STATE_SCHEMA_VERSION,
    session_key: key,
    session_source: event.source,
    routing_status: "ready",
    model_generation: generation,
    model_id: preserveModel ? prior.model_id : modelId,
    model_classification: preserveModel
      ? prior.model_classification
      : classifyExact(modelId, mapping),
    model_observed_from: preserveModel
      ? prior.model_observed_from
      : modelId === null
        ? null
        : "SessionStart",
    pending_switch: null,
    updated_at: now.toISOString(),
    operation: preserveOperation ? prior.operation : null,
  };
  await atomicWriteJson(pathname, state);
  if (preserveOperation && state.operation !== null) {
    writeHookOutput("SessionStart", {
      additionalContext: continuationContext(
        state.operation,
        state.model_classification === "unsupported",
      ),
    });
  }
}


async function handleUserPromptExpansion(event, pluginData, mapping) {
  if (
    event.hook_event_name !== "UserPromptExpansion" ||
    event.expansion_type !== "slash_command" ||
    event.command_source !== "plugin" ||
    (event.command_name !== AUTOMATIC_COMMAND && event.command_name !== EXPLICIT_COMMAND)
  ) {
    throw new RouterError("command-identity-invalid");
  }
  const explicit = event.command_name === EXPLICIT_COMMAND;
  const entry = explicit ? EXPLICIT_ENTRY : AUTOMATIC_ENTRY;
  const key = sessionKey(event.session_id);
  const pathname = statePath(pluginData, key);
  const state = await readState(pathname, key, false, false, mapping);
  if (state.routing_status !== "ready") {
    return failureEnvelope(
      entry,
      "unknown",
      state.routing_status === "pending" ? "state-pending" : "state-indeterminate",
    );
  }
  if (classifyExact(state.model_id, mapping) !== state.model_classification) {
    throw new RouterError("state-invalid");
  }
  let profile;
  let disclosureCode = "none";
  if (state.model_classification === "unsupported") {
    return failureEnvelope(entry, "unsupported", "unsupported-model");
  }
  if (state.model_classification === "claude-5") {
    profile = "claude-5";
  } else if (state.model_classification === "supported-non-5") {
    profile = "general";
    if (explicit) {
      disclosureCode = "non-claude-5-explicit-general";
    }
  } else if (state.model_classification === "unknown") {
    if (explicit) {
      profile = "claude-5";
      disclosureCode = "unknown-model-explicit-claude-5";
    } else {
      profile = "general";
      disclosureCode = "unknown-model-general-compatibility";
    }
  } else {
    throw new RouterError("state-invalid");
  }
  const now = new Date();
  const operation = operationFor(entry, profile, state.model_classification, now);
  const updated = { ...state, updated_at: now.toISOString(), operation };
  await atomicWriteJson(pathname, updated);
  return successEnvelope(
    entry,
    operation,
    state.model_classification,
    profile,
    disclosureCode,
  );
}


async function handlePreModelSwitch(event, pluginData, mapping) {
  if (
    event.hook_event_name !== "PreModelSwitch" ||
    !REQUESTED_SWITCH_SOURCES.has(event.source)
  ) {
    throw new RouterError("invalid-hook-input");
  }
  const key = sessionKey(event.session_id);
  const pathname = statePath(pluginData, key);
  const state = await readState(pathname, key, false, false, mapping);
  const fromModel = correlatableModelIdOrNull(event.from_model, mapping);
  requireString(event.to_model);
  if (fromModel === null) {
    await markIndeterminate(pathname, state);
    throw new RouterError("transition-invalid");
  }
  if (state.routing_status !== "ready") {
    throw new RouterError("transition-invalid");
  }
  if (state.model_id !== null && state.model_id !== fromModel) {
    await markIndeterminate(pathname, state);
    throw new RouterError("transition-invalid");
  }
  const now = new Date();
  await atomicWriteJson(pathname, {
    ...state,
    routing_status: "pending",
    pending_switch: {
      next_generation: incrementGeneration(state.model_generation),
      from_model: fromModel,
      source: event.source,
      started_at: now.toISOString(),
    },
    updated_at: now.toISOString(),
  });
}


async function markIndeterminate(pathname, state) {
  const now = new Date();
  await atomicWriteJson(pathname, {
    ...state,
    routing_status: "indeterminate",
    model_id: null,
    model_classification: "unknown",
    model_observed_from: null,
    pending_switch: null,
    updated_at: now.toISOString(),
  });
}


async function commitPostModelSwitch(event, pathname, state, mapping) {
  if (
    event.hook_event_name !== "PostModelSwitch" ||
    (!REQUESTED_SWITCH_SOURCES.has(event.source) && !AUTOMATIC_SWITCH_SOURCES.has(event.source))
  ) {
    throw new RouterError("invalid-hook-input");
  }
  const fromModel = requireString(event.from_model);
  const toModel = correlatableModelIdOrNull(event.to_model, mapping);
  let generation;
  if (REQUESTED_SWITCH_SOURCES.has(event.source)) {
    const pending = state.pending_switch;
    if (
      state.routing_status !== "pending" ||
      pending === null ||
      pending.from_model !== fromModel ||
      pending.source !== event.source
    ) {
      await markIndeterminate(pathname, state);
      throw new RouterError("transition-invalid");
    }
    generation = pending.next_generation;
  } else {
    if (state.routing_status !== "ready" && state.routing_status !== "indeterminate") {
      await markIndeterminate(pathname, state);
      throw new RouterError("transition-invalid");
    }
    try {
      generation = incrementGeneration(state.model_generation);
    } catch (error) {
      if (error instanceof RouterError && error.code === "transition-invalid") {
        await markIndeterminate(pathname, state);
      }
      throw error;
    }
  }
  const now = new Date();
  const classification = classifyExact(toModel, mapping);
  const committed = {
    ...state,
    routing_status: "ready",
    model_generation: generation,
    model_id: toModel,
    model_classification: classification,
    model_observed_from: toModel === null ? null : "PostModelSwitch",
    pending_switch: null,
    updated_at: now.toISOString(),
  };
  await atomicWriteJson(pathname, committed);
  if (committed.operation !== null) {
    return {
      additionalContext: continuationContext(
        committed.operation,
        classification === "unsupported",
        true,
      ),
    };
  }
  return null;
}


async function readStdin() {
  const chunks = [];
  let size = 0;
  for await (const chunk of process.stdin) {
    size += chunk.length;
    if (size > MAX_STDIN_BYTES) {
      throw new RouterError("invalid-hook-input");
    }
    chunks.push(chunk);
  }
  try {
    const source = new TextDecoder("utf-8", { fatal: true }).decode(Buffer.concat(chunks));
    return requireObject(parseJsonStrict(source));
  } catch (error) {
    if (error instanceof RouterError) {
      throw error;
    }
    throw new RouterError("invalid-hook-input");
  }
}


export async function main(argv = process.argv.slice(2)) {
  const action = argv[0];
  const isExpansion = action === "user-prompt-expansion";
  const expectedCommand = argv[1];
  let entry = expectedCommand === EXPLICIT_COMMAND ? EXPLICIT_ENTRY : AUTOMATIC_ENTRY;
  try {
    if (
      isExpansion &&
      expectedCommand !== undefined &&
      expectedCommand !== AUTOMATIC_COMMAND &&
      expectedCommand !== EXPLICIT_COMMAND
    ) {
      throw new RouterError("command-identity-invalid");
    }
    checkNodeVersion(process.versions.node);
    const rawEvent = await readStdin();
    if (isExpansion) {
      if (expectedCommand === undefined) {
        entry = rawEvent.command_name === EXPLICIT_COMMAND ? EXPLICIT_ENTRY : AUTOMATIC_ENTRY;
      } else if (rawEvent.command_name !== expectedCommand) {
        throw new RouterError("command-identity-invalid");
      }
    }
    if (action === "post-model-switch") {
      requireIdentifier(rawEvent.session_id, { maximum: MAX_SESSION_ID_BYTES });
      const pluginData = process.env.CLAUDE_PLUGIN_DATA;
      const key = sessionKey(rawEvent.session_id);
      const pathname = statePath(pluginData, key);
      const output = await withSessionLock(pathname, async () => {
        const prior = await readState(pathname, key);
        await markIndeterminate(pathname, prior);
        const event = validateEvent(rawEvent, action);
        const mapping = await loadMapping();
        validateState(prior, key, mapping);
        return commitPostModelSwitch(event, pathname, prior, mapping);
      });
      if (output !== null) {
        writeHookOutput("PostModelSwitch", output);
      }
      return 0;
    }
    const event = validateEvent(rawEvent, action);
    const pluginData = process.env.CLAUDE_PLUGIN_DATA;
    const pathname = statePath(pluginData, sessionKey(event.session_id));
    if (action === "session-start") {
      const mapping = await loadMapping();
      await withSessionLock(pathname, () => handleSessionStart(event, pluginData, mapping));
       await cleanupExpiredSessions(
         path.dirname(pathname),
         sessionKey(event.session_id),
         new Date(),
         mapping,
       );
      return 0;
    }
    if (isExpansion) {
      const mapping = await loadMapping();
      const envelope = await withSessionLock(
        pathname,
        () => handleUserPromptExpansion(event, pluginData, mapping),
      );
      writeRouteEnvelope(envelope);
      return 0;
    }
    if (action === "pre-model-switch") {
      const mapping = await loadMapping();
      await withSessionLock(
        pathname,
        () => handlePreModelSwitch(event, pluginData, mapping),
        { retryCount: 0, allowReclaim: false },
      );
      return 0;
    }
    throw new RouterError("invalid-hook-input");
  } catch (error) {
    if (isExpansion) {
      const code = error instanceof RouterError ? error.code : "internal-error";
      writeRouteEnvelope(failureEnvelope(entry, "unknown", code));
      return 0;
    }
    if (action === "pre-model-switch") {
      writeHookOutput("PreModelSwitch", {
        systemMessage: "Ask Then Do It could not update routing state. The requested model switch is not denied or changed.",
      });
      return 0;
    }
    if (action === "post-model-switch") {
      writeHookOutput("PostModelSwitch", {
        additionalContext: "Ask Then Do It routing state could not be synchronized. Stop both public entries until a new valid SessionStart state is established.",
        systemMessage: "Ask Then Do It routing state warning: the model changed, but safe state synchronization failed.",
      });
      return 0;
    }
    return 0;
  }
}


if (
  process.argv[1] !== undefined &&
  import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href
) {
  process.exitCode = await main();
}
