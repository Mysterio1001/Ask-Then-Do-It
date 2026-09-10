const mode = process.env.TICKET3_PREFLIGHT_MODE ?? "marker";
const nonce = process.env.TICKET3_PREFLIGHT_NONCE;

if (!/^[0-9a-f]{64}$/.test(nonce ?? "")) {
  process.stderr.write("TEST-ONLY preflight nonce missing or invalid\n");
  process.exit(64);
}

switch (mode) {
  case "marker":
    process.stdout.write(`${JSON.stringify({
      hookSpecificOutput: {
        hookEventName: "UserPromptExpansion",
        additionalContext: nonce,
      },
    })}\n`);
    break;
  case "nonzero":
    process.stderr.write("TEST-ONLY preflight nonzero\n");
    process.exitCode = 1;
    break;
  case "exit-2":
    process.stderr.write("TEST-ONLY preflight exit 2\n");
    process.exitCode = 2;
    break;
  case "timeout":
    setTimeout(() => process.stdout.write("TEST-ONLY preflight late\n"), 30_000);
    break;
  default:
    process.stderr.write("TEST-ONLY invalid preflight mode\n");
    process.exitCode = 64;
}
