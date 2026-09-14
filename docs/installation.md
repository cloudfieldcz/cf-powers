# Installing CF Powers

Version 2.5.1 adds standalone installation for Codex IDE environments. Choose
one Codex installation route per environment; installing both exposes duplicate
skills. Claude Code installation is independent and can coexist with either.

| Where you use CF Powers | Installation route |
|---|---|
| Claude Code | Claude plugin marketplace |
| Codex CLI only | Native Codex plugin |
| Codex in VS Code, optionally also CLI | Standalone skills from a full checkout |
| Codex App | Native plugin through its marketplace UI; manual UI verification pending |

The IDE extension currently supports standalone skills, but not plugins.
Installing a CLI plugin is therefore not an IDE installation. See
[OpenAI plugin availability](https://learn.chatgpt.com/docs/plugins) and
[standalone discovery](https://learn.chatgpt.com/docs/build-skills).

## Claude Code

Run in Claude Code:

```text
/plugin marketplace add cloudfieldcz/cf-powers
/plugin install cf-powers@cf-powers
/help
```

Check that the cf-powers commands appear. The SessionStart hook activates the
workflow. Use Claude's `/plugin` manager to update or uninstall cf-powers.

## Codex CLI: native plugin

Requires a Codex CLI with `codex plugin` commands; tested with 0.154.0.
Run in your terminal:

```bash
codex plugin marketplace add https://github.com/cloudfieldcz/cf-powers.git
codex plugin add cf-powers@cf-powers
```

For a local checkout, replace the Git URL with its absolute path. A local
marketplace uses that checkout as its source; a Git marketplace maintains its
own snapshot. Neither requires copying individual skills.

Start a new Codex session. Run `/skills` or type `$` and select
`cf-powers:analysis`, `cf-powers:writing-plans` or `cf-powers:orchestrator`.
Codex may also select skills automatically from the request. On 0.154.0, extra
`cf-powers:source-command-*` entries are imported Claude command wrappers.

### Update

For a Git marketplace:

```bash
codex plugin marketplace upgrade cf-powers
codex plugin add cf-powers@cf-powers
```

For a local marketplace, update its checkout with `git pull --ff-only` first,
then run the same `codex plugin add` command. Start a new session afterward.
Plugin updates need a new manifest version; editing a cached installation is
not an update mechanism.

### Uninstall

```bash
codex plugin remove cf-powers@cf-powers
```

This removes the installed plugin cache. It does not remove a separately
installed standalone skill link.

## VS Code and CLI: standalone skills

Requires Git, Python 3 and a Codex IDE extension with standalone skill support.
Commands below target macOS/Linux. Windows-native installation is not verified.
For Remote SSH, WSL or dev containers, run them in the environment where the
Codex extension executes, under the same user.

### New checkout

```bash
mkdir -p ~/.codex
git clone https://github.com/cloudfieldcz/cf-powers.git ~/.codex/cf-powers
python3 ~/.codex/cf-powers/bin/codex-skills install
```

The checkout must contain 2.5.1 or later for `bin/codex-skills` to exist.
If that directory is already a cf-powers checkout, update it instead of cloning
again. If it belongs to something else, choose another checkout path.

### Existing checkout

From the cf-powers repository:

```bash
python3 bin/codex-skills install
```

Both forms create `~/.agents/skills/cf-powers`, a symlink to this checkout's
`skills/` directory. Repeating installation from the same checkout is harmless.
An unrelated existing file, directory or symlink is left untouched and reported
as a conflict. To move to another checkout, uninstall using the old checkout
before installing from the new one.

Keep the complete checkout at this location. Reviews and execution also need
its `agents/`, runtime references and helper scripts. Do not copy only SKILL.md
files. No global model settings, AGENTS.md or custom agent definitions are edited.

### Activate and verify

1. Reload VS Code with **Developer: Reload Window** and start a new Codex chat.
2. Type `$` or `/skills` and find `cf-powers:analysis`. Codex 0.154.0 adds the
   discovery folder prefix; older clients may show `analysis` without a prefix.
3. Invoke the skill on a real task. The same standalone installation is also
   discoverable in CLI running under the same user/environment.

Check the link in a terminal if a skill is missing:

```bash
ls -ld ~/.agents/skills/cf-powers
python3 -c 'from pathlib import Path; print((Path.home()/".agents/skills/cf-powers").resolve())'
```

The resolved directory should be your checkout's `skills/`, containing the
individual skill folders. Confirm that VS Code is not running its extension in
a different remote environment. Restart the Codex chat after changes.

### Update

For the default checkout location:

```bash
git -C ~/.codex/cf-powers pull --ff-only
```

For another location, use that path instead. The symlink exposes updated files
immediately; start a new session so previously loaded instructions are replaced.
If Git reports local changes or divergence, resolve those before updating;
no reset or overwrite is necessary for the installer.

### Uninstall

Use the same checkout you installed from:

```bash
python3 ~/.codex/cf-powers/bin/codex-skills uninstall
```

Only its matching discovery symlink is removed. The checkout and project files
remain. Start a new session to drop the skills from discovery.

### Project-scoped alternative

To expose skills only to one project, run from the cf-powers checkout:

```bash
python3 bin/codex-skills install --skills-dir /absolute/path/to/project/.agents/skills
```

Use the same `--skills-dir` with `uninstall`. The absolute symlink is local to
this machine; do not commit it as a portable team installation.

## Switching routes and avoiding duplicates

When switching from the CLI plugin to standalone skills, remove the plugin with
`codex plugin remove cf-powers@cf-powers`, then install the standalone link.
When switching back, remove the link with `bin/codex-skills uninstall`, then
install the native plugin. Start a new session after either switch.

Standalone upstream Superpowers overlaps with cf-powers skill names. Avoid
enabling both standalone trees in the same environment. Do not delete another
installation merely because it has a similar name.

## Codex App and verification coverage

Use the App's supported repository marketplace import flow for the cf-powers
repository, then choose and install CF Powers and start a new chat. This plugin
is not listed in OpenAI's public catalog. The App UI flow has not been manually
verified; native install/update and resource discovery were tested through the
CLI/App Server.

The standalone route also passed real App Server discovery for all 20 skills,
shared reviewer resolution and installer lifecycle checks. A live VS Code UI
workflow remains unverified. Subagent availability depends on the host; when
independent review is unavailable, the skills report it and preserve review
artifacts rather than claiming approval.

Codex uses no SessionStart integrity hook. Run `bin/check-integrity` from the
checkout for a manual SKILL.md baseline check. See [SECURITY.md](../SECURITY.md)
for its scope and [verification record](codex-verification.md) for actual results.
