# Attribution and license scope

This notice concerns only the standalone Turbo Post Processing extraction in
ComfyUI Lokken VideoTools. No other Elvax nodes are included.

## Included code

| Portion | Origin and applicable terms |
| --- | --- |
| Post-processing backend, excluding the grain-derived portion | Elvax Nodes `nodes/post_processing.py`; GPL-3.0-or-later, as declared by the upstream README. |
| Frontend controls | Elvax Nodes `web/post_processing.js`; GPL-3.0-or-later. |
| Grain-derived portion (`PostProcessing._grain_chunk`) | Elvax credits Fast Film Grain from Jean Thompson (VRGameDevGirl). The corresponding channel-weighted Gaussian-grain routine is present in the historical AGPLv3 source linked below. AGPL-3.0-only applies to this portion. |
| Lokken registration, tests and modifications | Copyright (C) 2026 LordLocksley; GPL-3.0-or-later, subject to the combined-work terms below. |

Sources:

- [Elvax Nodes and its license/credits declaration](https://github.com/younestft/Elvax-nodes#license-and-credits).
- [Local fork's encoder-control branch](https://github.com/LordLocksley/Elvax-nodes/tree/codex/h264-encoder-controls).
- [Fast Film Grain source, historical revision 3b2a449](https://github.com/vrgamegirl19/comfyui-vrgamedevgirl/blob/3b2a44947769fc04909b282a3e996bb9f01bda7a/nodes.py).
- [Accompanying historical license declaration](https://github.com/vrgamegirl19/comfyui-vrgamedevgirl/blob/3b2a44947769fc04909b282a3e996bb9f01bda7a/LICENSE).

The historical source includes the same distinctive red/blue channel weighting
and green-channel saturation mix retained by Elvax's adapted grain routine.
This attribution is limited to that routine, not the other nodes in the source
repository. The later VRGameDevGirl custom license is not adopted here; the
identified historical AGPLv3 grant is retained.

## Combined-work terms

The GPLv3 text and upstream notice in LICENSE are preserved verbatim. GPLv3
section 13 permits combining GPLv3 code with AGPLv3 code: GPL terms remain on
the GPL-covered portion, and AGPLv3 section 13's network-interaction requirements
apply to the combination. LICENSE-AGPL-3.0.txt contains the full official AGPLv3
text. These are combined obligations, not an option to choose GPL alone for the
grain-derived portion.

The inherited LICENSE begins with `Copyright (C) 2026 NikoDemon80`. That line is
retained as an existing upstream notice; it is not a new claim that NikoDemon80
authored this standalone node. No Elvax H3 sampler, LLM or other unrelated
functionality is included or credited as part of this extraction.

## Runtime references, not bundled source

- [ComfyUI / Comfy Org](https://github.com/Comfy-Org/ComfyUI): native Lanczos
  scaling and video containers are called through ComfyUI's existing APIs.
- [Fill Nodes / filliptm](https://github.com/filliptm/ComfyUI_Fill-Nodes):
  optional `FL_RIFE` interpolation and `rife49` loading are accessed at runtime.

No ComfyUI implementation, Fill Nodes implementation or RIFE model weights are
redistributed in this repository. Their own licenses remain applicable to them.

## Modifications — 2026-10-21

LordLocksley's extraction retains the fork's H.264 preset/profile controls,
introduces the unique `LokkenVideoPostProcessing` registration and frontend
namespace, changes the category/search aliases and temporary-object branding,
and changes the encoder-preset default from `ultrafast` to `medium`. Standalone
registration, tests and documentation were added. The inherited grain math was
not changed by this extraction.

## Preserved historical grain-source notice

The following is the historical repository's license declaration, reproduced
verbatim. The complete AGPLv3 terms it references are supplied separately in
LICENSE-AGPL-3.0.txt.

```text
GNU Affero General Public License v3.0

Copyright (c) 2026 Jean Thompson

This ComfyUI custom node is licensed under the GNU Affero General Public License v3.0.

You may use, modify, and distribute this software only under the terms of the GNU Affero General Public License v3.0.

Commercial use is allowed only if the user follows the AGPL-3.0 license terms.

This means anyone who modifies, redistributes, hosts, or uses this code as part of a public app, paid service, or network-accessible tool must provide the complete corresponding source code under the same AGPL-3.0 license.

You may not use this code in a closed-source paid app, private hosted service, SaaS product, or commercial wrapper without complying with AGPL-3.0.

Full license text:
https://www.gnu.org/licenses/agpl-3.0.en.html
```
