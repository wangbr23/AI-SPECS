#!/usr/bin/env node

import { existsSync, readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";

const inputPath = process.argv[2] ?? "TODO.md";
const todoPath = resolve(inputPath);

if (!existsSync(todoPath)) {
  console.error(`TODO validation failed: file not found: ${todoPath}`);
  process.exit(1);
}

const lines = readFileSync(todoPath, "utf8").split(/\r?\n/);
const taskPattern = /^- \[([ xX])\] `T(\d+)` (.+) \u2014 (manual|agent)(.*)$/;
const tasks = new Map();
const orderedIds = [];
const errors = [];

for (const [index, line] of lines.entries()) {
  if (!line.startsWith("- [")) continue;

  const match = line.match(taskPattern);
  if (!match) {
    errors.push(`line ${index + 1}: malformed task`);
    continue;
  }

  const [, marker, rawId, description, kind, metadata] = match;
  const id = Number(rawId);

  if (tasks.has(id)) errors.push(`line ${index + 1}: duplicate T${id}`);
  if (!description.trim()) errors.push(`T${id}: missing description`);

  const complexityMatches = [
    ...metadata.matchAll(/(?:^|, )complexity: (simple|complex)(?=, |$)/g),
  ];
  const complexity = complexityMatches[0]?.[1];

  if (kind === "agent" && complexityMatches.length !== 1) {
    errors.push(`T${id}: agent task needs exactly one simple/complex classification`);
  }
  if (kind === "manual" && complexityMatches.length !== 0) {
    errors.push(`T${id}: manual task must not declare complexity`);
  }

  const dependencyMatch = metadata.match(
    /(?:^|, )depends-on: (.*?)(?=, design:|$)/,
  );
  const dependencyText = dependencyMatch?.[1];
  const dependencies = dependencyText
    ? [...dependencyText.matchAll(/T(\d+)/g)].map((entry) => Number(entry[1]))
    : [];

  if (dependencyText && !/^T\d+(?:, T\d+)*$/.test(dependencyText)) {
    errors.push(`T${id}: malformed dependency list: ${dependencyText}`);
  }
  if (new Set(dependencies).size !== dependencies.length) {
    errors.push(`T${id}: duplicate dependency`);
  }
  if (dependencies.includes(id)) errors.push(`T${id}: self dependency`);

  const designMatch = metadata.match(/(?:^|, )design: ([^,]+)$/);
  const designPath = designMatch?.[1];
  if (designPath && !existsSync(resolve(dirname(todoPath), designPath))) {
    errors.push(`T${id}: design path does not exist: ${designPath}`);
  }

  const expectedMetadata = [
    kind === "agent" && complexity ? `complexity: ${complexity}` : null,
    dependencyText ? `depends-on: ${dependencyText}` : null,
    designPath ? `design: ${designPath}` : null,
  ]
    .filter(Boolean)
    .map((entry) => `, ${entry}`)
    .join("");

  if (metadata !== expectedMetadata) {
    errors.push(`T${id}: metadata is malformed or not in canonical order`);
  }

  tasks.set(id, {
    checked: marker.toLowerCase() === "x",
    dependencies,
    kind,
  });
  orderedIds.push(id);
}

if (tasks.size === 0) errors.push("no task lines found");

const highestId = Math.max(0, ...orderedIds);
const expectedIds = Array.from({ length: highestId }, (_, index) => index + 1);
if (
  orderedIds.length !== expectedIds.length ||
  orderedIds.some((id, index) => id !== expectedIds[index])
) {
  errors.push("task ids must be unique and sequential from T1 in file order");
}

for (const [id, task] of tasks) {
  for (const dependency of task.dependencies) {
    if (!tasks.has(dependency)) {
      errors.push(`T${id}: missing dependency T${dependency}`);
    }
  }
}

const states = new Map();
const stack = [];
const cycles = new Set();

function visit(id) {
  if (states.get(id) === "done") return;
  if (states.get(id) === "active") {
    const start = Math.max(0, stack.indexOf(id));
    cycles.add([...stack.slice(start), id].map((entry) => `T${entry}`).join(" -> "));
    return;
  }

  states.set(id, "active");
  stack.push(id);
  for (const dependency of tasks.get(id)?.dependencies ?? []) {
    if (tasks.has(dependency)) visit(dependency);
  }
  stack.pop();
  states.set(id, "done");
}

for (const id of tasks.keys()) visit(id);
for (const cycle of cycles) errors.push(`dependency cycle: ${cycle}`);

if (errors.length > 0) {
  console.error("TODO validation failed:");
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

const readyTasks = [...tasks].filter(
  ([, task]) =>
    !task.checked &&
    task.dependencies.every((dependency) => tasks.get(dependency).checked),
);
const manualReady = readyTasks
  .filter(([, task]) => task.kind === "manual")
  .map(([id]) => `T${id}`);
const agentReady = readyTasks
  .filter(([, task]) => task.kind === "agent")
  .map(([id]) => `T${id}`);

const formatIds = (ids) => (ids.length > 0 ? ids.join(", ") : "none");

console.log(`TODO validation passed: ${tasks.size} tasks through T${highestId}`);
console.log(`Manual-ready: ${formatIds(manualReady)}`);
console.log(`Agent-ready: ${formatIds(agentReady)}`);
