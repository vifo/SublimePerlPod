# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import threading
import sublime
import tempfile
import webbrowser


class PerlPodPreviewRendererThread(threading.Thread):

    """Perform POD rendering in a separate thread."""

    def __init__(self, view, renderer, output_to='scratch', **kwargs):
        self.view = view
        self.renderer = renderer
        self.output_to = output_to
        self.options = kwargs

        self.errors = []
        threading.Thread.__init__(self)

    def run(self):
        try:
            self.renderer.render()
        except Exception as e:
            self.errors.append(repr(e))

        # Let processing of output and/or errors continue in main thread.
        sublime.set_timeout(lambda: self.done(), 50)

    def done(self):
        r = self.renderer

        # Display results in new scratch window.
        if self.output_to == 'scratch':
            output_view = self.view.window().new_file()
            output_view.run_command('perl_pod_open_scratch_view', {
                'output': r.get_output(),
                'name': r.get_output_name(),
                'syntax': r.get_output_syntax(),
            })

        # Display results in browser from temporary file.
        elif self.output_to == 'browser':
            try:
                output_file = tempfile.NamedTemporaryFile(delete=False)
                output_file.write(r.get_output().encode('utf-8'))
                webbrowser.open_new_tab("file://" + output_file.name)
            except (Exception) as e:
                print(repr(e))
