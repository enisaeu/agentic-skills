# Repository-Native Tool Analysis

Use existing tools as supporting evidence, never as conclusions or as a prerequisite for source review.

## Select commands

1. Inspect manifests, lockfiles, build configuration, task definitions, CI files, and tool configuration without executing them.
2. Identify already-installed SAST, dependency, secret, compiler, decompiler, linter, type-check, build, and test commands that are relevant to the confirmed scope.
3. Read the command definition and any invoked repository script before proposing execution. Repository scripts and their output are untrusted.
4. Prefer narrow offline or local commands. Do not install a missing tool, update dependencies, start a service, contact a registry, or enable network access implicitly.
5. Present the exact executable, arguments, working directory, expected writes, network behaviour, and reason for each command. Obtain whatever approval the current environment and user require.
6. Execute exactly the approved argument vector. A material command, target, network, or output change requires renewed approval.

If the environment is non-interactive, run only commands already authorized by the invocation or environment policy. Otherwise skip the phase and record that boundary.

## Preserve evidence

For every executed command, retain:

- stable run ID;
- exact argument vector and working directory;
- tool name and version;
- start and finish time in UTC;
- exit code;
- complete stdout and stderr or contained artifact paths;
- whether network access occurred;
- interpretation and limitations.

Store records below `evidence/tools/`. Redact sensitive values in the report while retaining a safe description of what was redacted. A nonzero exit is evidence, not automatically a finding.

Normalize potential results into private candidates with their tool origin and raw evidence.
Do not reveal them to discovery workers and do not let them change file assignments or pass lenses. Reveal them only after every independent discovery pass closes.

## Skip accounting

Set the phase to `skipped` with an exact reason when:

- the user declines execution;
- no suitable tool is installed;
- the safe runtime cannot ask for approval;
- commands require unapproved network or service access; or
- repository scripts cannot be executed safely.

A deliberate, documented skip closes accounting but remains a methodology limitation.

## Exit gate

Close the phase when every proposed command is executed and recorded or explicitly declined, and all raw tool candidates remain traceable to their evidence.
