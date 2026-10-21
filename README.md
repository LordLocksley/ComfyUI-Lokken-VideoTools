# ComfyUI Lokken VideoTools

One video post-processing node for ComfyUI, derived from the Turbo Post
Processing node in [Elvax Nodes](https://github.com/younestft/Elvax-nodes),
with configurable H.264 encoder presets and profiles.

## Status and installation

The standalone implementation is available from this repository. It has not yet
been published to Comfy Registry. To install manually, run the following from
your `ComfyUI/custom_nodes/` directory:

```sh
git clone https://github.com/LordLocksley/ComfyUI-Lokken-VideoTools.git
```

Restart ComfyUI and search for **Video Post Processing — Lokken**.
Registry publishing instructions are in [PUBLISHING.md](PUBLISHING.md).

The internal node identifier is `LokkenVideoPostProcessing`, in category
`Lokken/Video`. It can be installed alongside Elvax Nodes. Existing workflows
using `ElvaxPostProcessing` continue to use Elvax; they are not migrated
automatically.

## Usage

Connect a `VIDEO` or an `IMAGE` batch. A connected `VIDEO` supplies its own
frames and frame rate and takes precedence over `images`. For an image batch,
set `original_fps` to its intended frame rate. Optional `audio_pass` supplies
audio; otherwise a video input's soundtrack is retained when available.

The processing order is Lanczos upscale, RIFE interpolation, optional film
grain, then H.264 encoding. Disable the processing toggles you do not need.
The node returns `VIDEO`, `FPS` and a timing summary. Connect `VIDEO` to
ComfyUI's Save Video node.

| Setting | Meaning |
| --- | --- |
| `encoder_preset` | `ultrafast`, `superfast`, `veryfast`, `faster`, `fast`, `medium`, `slow`, `slower`, `veryslow`. Default: `medium`. Slower presets trade encoding time for compression efficiency. |
| `h264_profile` | `auto`, `baseline`, `main`, `high`. Default: `auto`, leaving the profile constraint unset. A forced profile constrains allowed features; the actual profile can be lower when a preset disables those features. |
| `compress` / `crf` | Compression is on by default at CRF 18. Disabling compression or setting CRF 0 uses the inherited encoder's lossless mode. That mode requires profile `auto`; forced profiles produce an error. |
| `grain` | Enables random film grain. `grain_intensity` sets its amount; `saturation_mix` blends the inherited channel-weighted grain with shared green-channel noise. There is no fixed-seed control. |
| `batching_mode` | `full sequence`, `normal (64)`, `low vram (16)` or `custom`. `custom_batch_size` is used only in custom mode. |

For matching segment exports, use the same frame geometry, frame rate, CRF,
preset and profile on both encoders. The node retains the fork's four-frame
encoding handoff and disk-backed temporary video output; it does not eliminate
memory occupied by the input image batch. Temporary files remain alive while
their video objects are retained, including by ComfyUI's cache.

The inherited timing summary tracks workflow start through a local
`PromptServer.send_sync` wrapper. It forwards events to the existing handler.

## Requirements

The node uses PyTorch, NumPy and PyAV supplied by ComfyUI. No additional pip
packages or install scripts are added. The checked environment is ComfyUI
0.42.0, PyTorch 2.14.1 and PyAV 17.0.1.

**RIFE interpolation only:** requires the `FL_RIFE` node from Fill Nodes and
its `rife49` model. This dependency is accessed only when interpolation runs.
Encoding, grain and Lanczos upscaling do not require Fill Nodes.

## Development checks

See [tests/README.md](tests/README.md) for small CPU checks. Real GPU processing
and model-backed RIFE interpolation require separate runtime testing.

## Attribution and license

The copied backend and frontend originate in **Elvax Nodes**, maintained by
[younestft](https://github.com/younestft/Elvax-nodes), and its contributors.
Our H.264 preset/profile controls are also available in the
[upstream pull request](https://github.com/younestft/Elvax-nodes/pull/1).

The inherited grain routine is credited to **Fast Film Grain by Jean Thompson
(VRGameDevGirl)**. It is covered here by the historical AGPLv3 source grant
identified in [NOTICE.md](NOTICE.md).

ComfyUI's native Lanczos scaler is called at runtime. Optional RIFE interpolation
calls `FL_RIFE` from **Fill Nodes by filliptm**. Their implementations and model
weights are not bundled; those projects retain their own licenses.

Elvax-derived portions and Lokken's original additions use **GPL-3.0-or-later**;
the grain-derived portion uses **AGPL-3.0-only**. They are distributed together
under GPLv3 section 13, with AGPLv3's network-interaction requirements applying
to the combination. Both applicable license texts are included:
[GPLv3](LICENSE) and [AGPLv3](LICENSE-AGPL-3.0.txt).

See [NOTICE.md](NOTICE.md) for the per-component scope, preserved notices and
dated modifications. This covers this repository's code; it does not relicense
the wider Elvax pack, ComfyUI, Fill Nodes or their models. No endorsement by
the original authors is implied.
