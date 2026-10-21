// SPDX-License-Identifier: GPL-3.0-or-later
// Derived from Elvax Nodes' web/post_processing.js; see NOTICE.md.
// Modifications Copyright (C) 2026 LordLocksley.
// Modified 2026-10-21: Lokken node identifier and frontend hook names.
import { app } from "/scripts/app.js";

const NODE_TYPE = "LokkenVideoPostProcessing";

function installToggle(node, toggleName, label, dependentNames, refresh) {
  const toggle = node.widgets?.find((widget) => widget.name === toggleName);
  const dependents = dependentNames
    .map((name) => node.widgets?.find((widget) => widget.name === name))
    .filter(Boolean);
  if (!toggle || toggle.__lokkenDisableInstalled) return;

  toggle.label = label;
  toggle.__lokkenDisableInstalled = true;
  const update = () => {
    for (const widget of dependents) widget.disabled = !toggle.value;
    refresh();
  };
  const callback = toggle.callback;
  toggle.callback = function (...args) {
    const result = callback?.apply(this, args);
    update();
    return result;
  };
  update();
}

function hideFixedWidget(node, name, value) {
  const widget = node.widgets?.find((item) => item.name === name);
  if (!widget) return;
  widget.value = value;
  widget.hidden = true;
  widget.type = "hidden";
  widget.computeSize = () => [0, -4];
  const inputIndex = node.inputs?.findIndex((input) => input.name === name) ?? -1;
  if (inputIndex !== -1) node.removeInput(inputIndex);
}

function labelAudioInput(node) {
  const input = node.inputs?.find((item) => item.name === "audio_pass");
  if (input) input.label = "audio";
}

function updateBatchSize(node) {
  const mode = node.widgets?.find((widget) => widget.name === "batching_mode");
  const batchSize = node.widgets?.find((widget) => widget.name === "custom_batch_size");
  const dualPass = node.widgets?.find((widget) => widget.name === "dual_pass_rife");
  const interpolate = node.widgets?.find((widget) => widget.name === "interpolate");
  const modeValue = String(mode?.value ?? "").toLowerCase();
  if (mode && ["full sequence", "normal (64)", "low vram (16)", "custom"].includes(modeValue)) {
    mode.value = modeValue;
  }
  if (batchSize) batchSize.disabled = modeValue !== "custom";
  if (dualPass) {
    dualPass.label = "dual_pass_rife";
    dualPass.disabled = !interpolate?.value;
  }
  node.graph?.setDirtyCanvas(true, true);
}

app.registerExtension({
  name: "Lokken.PostProcessing",
  beforeRegisterNodeDef(nodeType, nodeData) {
    if (nodeData.name !== NODE_TYPE) return;
    const optional = nodeData.input?.optional;
    const required = nodeData.input?.required;
    if (!optional?.audio_pass || !required?.images) return;

    const audioInput = optional.audio_pass;
    delete optional.audio_pass;
    const requiredInputs = Object.entries(required);
    requiredInputs.splice(requiredInputs.findIndex(([name]) => name === "images") + 1, 0, ["audio_pass", audioInput]);
    nodeData.input.required = Object.fromEntries(requiredInputs);

    const inputOrder = nodeData.input_order ??= {};
    inputOrder.optional = (inputOrder.optional ?? []).filter((name) => name !== "audio_pass");
    const requiredOrder = (inputOrder.required ?? Object.keys(required)).filter((name) => name !== "audio_pass");
    requiredOrder.splice(Math.max(0, requiredOrder.indexOf("images") + 1), 0, "audio_pass");
    inputOrder.required = requiredOrder;
  },
  nodeCreated(node) {
    if (node.type !== NODE_TYPE && node.comfyClass !== NODE_TYPE) return;
    const refresh = () => node.graph?.setDirtyCanvas(true, true);
    labelAudioInput(node);
    hideFixedWidget(node, "upscale_method", "lanczos");
    installToggle(node, "upscale", "UPSCALE (lanczos)", ["upscale_by"], refresh);
    installToggle(node, "interpolate", "INTERPOLATE (rife49)", ["interpolate_by", "dual_pass_rife"], refresh);
    installToggle(node, "grain", "FILM GRAIN", ["grain_intensity", "saturation_mix"], refresh);
    installToggle(node, "compress", "COMPRESS", ["crf"], refresh);
    const mode = node.widgets?.find((widget) => widget.name === "batching_mode");
    if (mode && !mode.__lokkenBatchModeInstalled) {
      mode.__lokkenBatchModeInstalled = true;
      const callback = mode.callback;
      mode.callback = function (...args) {
        const result = callback?.apply(this, args);
        updateBatchSize(node);
        return result;
      };
    }
    updateBatchSize(node);
    if (!node.__lokkenPostProcessingConfigureHook) {
      node.__lokkenPostProcessingConfigureHook = true;
      const onConfigure = node.onConfigure;
      node.onConfigure = function (...args) {
        const values = args[0]?.widgets_values;
        const compressIndex = this.widgets?.findIndex((widget) => widget.name === "compress") ?? -1;
        if (compressIndex >= 0 && typeof values?.[compressIndex] === "string") {
          values.splice(compressIndex, 0, false, 18);
          for (let index = compressIndex; index < values.length; index++) {
            if (this.widgets[index]) this.widgets[index].value = values[index];
          }
        }
        const result = onConfigure?.apply(this, args);
        requestAnimationFrame(() => {
          labelAudioInput(this);
          updateBatchSize(this);
          for (const [toggleName, names] of [
            ["upscale", ["upscale_by"]],
            ["interpolate", ["interpolate_by", "dual_pass_rife"]],
            ["grain", ["grain_intensity", "saturation_mix"]],
            ["compress", ["crf"]],
          ]) {
            const enabled = Boolean(this.widgets?.find((widget) => widget.name === toggleName)?.value);
            for (const name of names) {
              const widget = this.widgets?.find((item) => item.name === name);
              if (widget) widget.disabled = !enabled;
            }
          }
          hideFixedWidget(this, "upscale_method", "lanczos");
          refresh();
        });
        return result;
      };
    }
  },
});
