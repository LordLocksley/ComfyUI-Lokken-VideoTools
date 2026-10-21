# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 LordLocksley.
# Created 2026-10-21. See LICENSE and NOTICE.md.

"""Small CPU checks using ComfyUI's real video implementation; no model loading."""
import importlib.util
import inspect
import io
import os
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.argv = [sys.argv[0], '--cpu']
sys.path.insert(0, os.environ['COMFYUI_PATH'])

import av
import torch
from comfy_api.latest import InputImpl, Types
from server import PromptServer

torch.set_num_threads(2)
PromptServer.instance = None


def load_pack(name):
    spec = importlib.util.spec_from_file_location(name, ROOT/'__init__.py',
                                                submodule_search_locations=[str(ROOT)])
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


PACK = load_pack('lokken_video_tools_check')
Node = PACK.NODE_CLASS_MAPPINGS['LokkenVideoPostProcessing']


class PostProcessingChecks(unittest.TestCase):
    def setUp(self):
        self.images = torch.rand((5, 32, 48, 3), generator=torch.Generator().manual_seed(123))

    def encode(self, **kwargs):
        options = dict(images=self.images, upscale=False, interpolate=False, grain=False,
                       original_fps=24, batching_mode='custom', custom_batch_size=4)
        options.update(kwargs)
        video, fps, stats = Node().process(**options)
        self.addCleanup(video._lokken_temp_dir.cleanup)
        self.assertEqual(video.get_frame_rate(), fps)
        self.assertIn('Node generation time:', stats)
        return video

    def packets(self, video):
        with av.open(video.videos[0].get_stream_source()) as container:
            stream = container.streams.video[0]
            return (stream.codec_context.extradata,
                    [bytes(packet) for packet in container.demux(video=0) if packet.size])

    def test_registration_and_medium_defaults(self):
        self.assertEqual(list(PACK.NODE_CLASS_MAPPINGS), ['LokkenVideoPostProcessing'])
        self.assertEqual(PACK.NODE_DISPLAY_NAME_MAPPINGS['LokkenVideoPostProcessing'],
                         'Video Post Processing — Lokken')
        schema = Node.INPUT_TYPES()['required']
        self.assertEqual(schema['encoder_preset'][1]['default'], 'medium')
        self.assertEqual(schema['h264_profile'][1]['default'], 'auto')
        self.assertEqual(list(schema)[-2:], ['encoder_preset', 'h264_profile'])
        self.assertEqual(inspect.signature(Node.process).parameters['encoder_preset'].default, 'medium')
        self.assertEqual(inspect.signature(Node._encode_video).parameters['encoder_preset'].default, 'medium')
        self.assertEqual(self.packets(self.encode()), self.packets(self.encode(encoder_preset='medium')))

    def test_presets_profiles_and_lossless_errors(self):
        for preset, profile in [('ultrafast','auto'), ('medium','auto'), ('slow','high')]:
            with self.subTest(preset=preset, profile=profile):
                video = self.encode(encoder_preset=preset, h264_profile=profile)
                self.assertEqual(video.get_frame_count(), 5)
                with av.open(video.videos[0].get_stream_source()) as container:
                    self.assertEqual(sum(1 for _ in container.decode(video=0)), 5)
        self.assertEqual(self.encode(compress=False).get_frame_count(), 5)
        for options in [{'compress':False}, {'crf':0}]:
            for profile in ['baseline','main','high']:
                with self.assertRaisesRegex(ValueError, 'Set h264_profile to auto'):
                    self.encode(h264_profile=profile, **options)

    def test_batching_grain_and_input_preservation(self):
        original = self.images.clone()
        reference = self.packets(self.encode())
        for mode in Node._GROUP_MODES:
            with self.subTest(mode=mode):
                self.assertEqual(self.packets(self.encode(batching_mode=mode, custom_batch_size=1)), reference)
        grain = self.encode(grain=True, grain_intensity=0.008)
        self.assertEqual(grain.get_frame_count(), 5)
        self.assertNotEqual(self.packets(grain), reference)
        self.assertTrue(torch.equal(self.images, original))

    def test_lanczos_and_interpolation_standin(self):
        class Rife:
            device = torch.device('cpu')
            model = None

            def make_inference(self, model, first, second, amount, ensemble):
                return first.lerp(second, amount)

        with patch.object(Node, '_open_rife', return_value=(Rife(), object())):
            video = self.encode(upscale=True, upscale_by=2, interpolate=True,
                                interpolate_by=2, custom_batch_size=2)
        self.assertEqual(video.get_dimensions(), (96, 64))
        self.assertEqual(video.get_frame_count(), 9)
        self.assertEqual(video.get_frame_rate(), 48)

    def test_matching_segments_and_audio_without_reencode(self):
        first, second = self.encode(), self.encode()
        audio = {'waveform':torch.zeros((1,2,20000)), 'sample_rate':48000}
        combined = InputImpl.VideoFromList([first,second], complete_audio=audio, codec=Types.VideoCodec.H264)
        output = io.BytesIO()
        with patch.object(InputImpl.VideoFromFile, '_save_transcoded',
                          side_effect=AssertionError('Unexpected additional video encoding')):
            combined.save_to(output, format=Types.VideoContainer.MP4, codec=Types.VideoCodec.H264)
        with av.open(io.BytesIO(output.getvalue())) as container:
            self.assertEqual(len(container.streams.audio), 1)
            self.assertEqual(sum(1 for _ in container.decode(video=0)), 10)

    def test_timing_hook_forwards_existing_handler(self):
        calls = []
        server = SimpleNamespace(send_sync=lambda *args: calls.append(args))
        with patch.object(PromptServer, 'instance', server):
            other = load_pack('lokken_video_tools_hook_check')
            node = other.NODE_CLASS_MAPPINGS['LokkenVideoPostProcessing']
            server.send_sync('execution_start', {}, 'local-check')
            self.assertIsInstance(node._workflow_started, float)
            server.send_sync('execution_success', {}, 'local-check')
            self.assertIsNone(node._workflow_started)
            self.assertEqual([event for event, _, _ in calls], ['execution_start','execution_success'])


if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0]], verbosity=2)
