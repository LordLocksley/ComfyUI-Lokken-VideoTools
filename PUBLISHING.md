# Publishing to Comfy Registry

The package is prepared as `lokken-videotools` version `1.0.0`, under publisher
`lokken`. It has not yet been published. Registry publication makes it available
to ComfyUI-Manager, subject to Registry checks and indexing.

## Preparation

Install Comfy CLI in a separate development environment, not in ComfyUI's
embedded Python. For example, with a separately installed Python:

```powershell
python -m venv "$env:LOCALAPPDATA\LokkenVideoTools\registry-cli"
& "$env:LOCALAPPDATA\LokkenVideoTools\registry-cli\Scripts\python.exe" -m pip install comfy-cli
```

This environment is a publishing tool only; it is not a runtime dependency of
the node. The node itself uses ComfyUI's existing packages.

## Publish when ready

1. Confirm `pyproject.toml` has the intended publisher, package name and version.
   Registry identifiers cannot be changed after creation; each published version
   is immutable.
2. Commit and push the intended source first. Confirm `git status --short` is
   empty and run the bounded checks in [tests/README.md](tests/README.md).
3. In this repository's directory, run:

   ```powershell
   & "$env:LOCALAPPDATA\LokkenVideoTools\registry-cli\Scripts\comfy.exe" node publish
   ```

4. Enter the Registry PAT at the hidden prompt. Do not put it in a command,
   source file, screenshot, issue or chat message.
5. Check the Registry result and Manager availability before announcing release.

No automatic publishing action is installed. Pushing to GitHub does not publish
to the Registry.

## Package contents and licensing

The CLI packages Git-tracked files; `.comfyignore` excludes the CPU tests from
the install archive. The backend, registration, frontend, README, NOTICE and both
license texts remain included. Tests remain available in the public Git repository.

The metadata records both GPL and AGPL obligations. See [NOTICE.md](NOTICE.md)
for their component scope. Do not replace this with GPL-only metadata.

The standalone node has a distinct identifier and exposes encoder controls absent
from the original upstream node. Registry fork acceptance and indexing are still
subject to Registry review; preparing metadata does not guarantee acceptance.

Official references: [publishing](https://docs.comfy.org/registry/publishing),
[metadata](https://docs.comfy.org/registry/specifications), and
[standards](https://docs.comfy.org/registry/standards).
