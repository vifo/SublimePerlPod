# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import base64
import json
import subprocess
import sublime
import os

from perl_pod import *
from perl_pod.preview_renderers.base import PerlPodBasePreviewRenderer
from perl_pod.utils import save_and_prepare_env, restore_env, get_default_subprocess_args


POD_HTML_RENDERER_PATH = os.path.join(
    sublime.packages_path(), PLUGIN_NAME, 'lib', 'perl_pod', 'preview_renderers', 'perl', 'bin', 'pod_html.pl')


class PerlPodPodHtmlPreviewRenderer(PerlPodBasePreviewRenderer):

    def __init__(self, view, input, **options):
        super(PerlPodPreviewPodTextRenderer, self).__init__(view, input, **options)
        self.set_output_syntax('text')

    def render(self):
        # Prepare JSON data structure for external renderer
        out_data = {
            "schema_version": "1.0",
            "input": self.input,
            "options": {
            },
        }
        out_data = base64.b64encode(json.dumps(out_data)) + "\n"
        in_data = {}

        cmd_final = ['perl', POD_TEXT_RENDERER_PATH]

        # Show time!
        success, output, error_output, error_hints = False, None, None, []
        # logger.log(1, 'Running command: ' + pp(cmd_final))
        orig_env = save_and_prepare_env()

        try:
            subprocess_args = get_default_subprocess_args()
            p = subprocess.Popen(cmd_final, **subprocess_args)
            output, error_output = p.communicate(out_data)

            if output:
                output = output.decode('ascii')
            if error_output:
                error_output = error_output.decode('iso-8859-1')
                print(repr(error_output))

            # logger.log(2, 'Command exited with code: {0}'.format(p.returncode))

            # Decode error output (if any), otherwise clear it and set
            # success.
            if not error_output:
                in_data = json.loads(base64.b64decode(output))
                self.output = in_data['output']
                success = True

        except (Exception) as e:
            print(repr(e))
            self.errors.append(repr(e))

        finally:
            restore_env(orig_env)

        return success
