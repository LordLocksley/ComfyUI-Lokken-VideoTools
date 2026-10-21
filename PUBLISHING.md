# Publishing to Comfy Registry

`lokken-videotools` version `1.0.0` is published under publisher `lokken` and
available through ComfyUI-Manager. These instructions cover future releases.

## Preparation

Install Comfy CLI in a Python environment chosen for publishing. A separate
virtual environment is optional and keeps publishing dependencies isolated;
an existing development Python can also be used after checking dependency changes.
Comfy CLI is a publishing tool, not a runtime dependency of the node.

For example, to create an isolated environment with a separately installed Python:

```powershell
python -m venv "$env:LOCALAPPDATA\LokkenVideoTools\registry-cli"
& "$env:LOCALAPPDATA\LokkenVideoTools\registry-cli\Scripts\python.exe" -m pip install comfy-cli
```

In the commands below, use your chosen Python interpreter in place of `python`
if it is not the one on PATH. Before the first CLI launch, disable telemetry:

```powershell
$env:COMFY_NO_TELEMETRY = '1'
python -m comfy_cli tracking disable
```

The command saves the tracking opt-out. The environment variable also suppresses
telemetry for the current PowerShell session; set it in future publishing sessions
as shown below.

## Publish a new version

1. Update the version in `pyproject.toml` and confirm the intended publisher and
   package name. Registry identifiers cannot be changed after creation. Use a new
   version for each release; the existing `1.0.0` archive is not replaced.
2. Run the bounded checks in [tests/README.md](tests/README.md), then commit and
   push the intended source. Review `git status --short` for unexpected files.
   The CLI's generated `node.zip` need not be committed.
3. In this repository's directory, run:

   ```powershell
   $env:COMFY_NO_TELEMETRY = '1'
   python -m comfy_cli node publish
   ```

4. Enter the Registry PAT at the hidden prompt. Do not put it in a command,
   source file, screenshot, issue or chat message.
5. Check the [version status](https://api.comfy.org/nodes/lokken-videotools/versions?include_status_reason=true).
   Upload success confirms transfer. `NodeVersionStatusActive` means the release
   is active; `Pending` or `Flagged` requires further processing or attention.
   The separate `comfy_node_extract_status` tracks the catalogue of individual
   nodes and can remain pending after activation. Check Manager availability
   before announcing a new release.

No automatic publishing action is installed. Pushing to GitHub does not publish
to the Registry. GitHub documentation can be newer than the documentation inside
an existing Registry archive; corrected files accompany the next release.

## Package contents and licensing

The CLI packages Git-tracked files; `.comfyignore` excludes the CPU tests from
the install archive. The backend, registration, frontend, README, NOTICE and both
license texts remain included. Tests remain available in the public Git repository.

The metadata records both GPL and AGPL obligations. See [NOTICE.md](NOTICE.md)
for their component scope. Do not replace this with GPL-only metadata.

The standalone node has a distinct identifier and exposes encoder controls absent
from the original upstream node. Future releases remain subject to Registry checks.

Official references: [publishing](https://docs.comfy.org/registry/publishing),
[metadata](https://docs.comfy.org/registry/specifications), and
[standards](https://docs.comfy.org/registry/standards).
