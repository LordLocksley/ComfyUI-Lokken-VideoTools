# CPU checks

`test_post_processing.py` exercises pack registration, encoder defaults and
profiles, batching, grain input preservation, optional upscaling/interpolation,
segment stitching with audio and workflow timing event forwarding. RIFE is
replaced by a small deterministic stand-in; no model is downloaded or loaded.

Set `COMFYUI_PATH` to the ComfyUI source directory and run the test file with
ComfyUI's Python interpreter. For Windows portable, from the pack directory:

```powershell
$env:COMFYUI_PATH = (Resolve-Path '..\..').Path
& '..\..\..\python_embeded\python.exe' -s '.\tests\test_post_processing.py'
```

The checks select CPU execution before importing ComfyUI. They run in a separate
process and do not connect to, restart or queue work in a running ComfyUI server.
They do not establish GPU performance, actual RIFE quality or live frontend loading.
