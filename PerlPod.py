# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import sublime
import sublime_plugin
import sys
import os
import webbrowser

sys.path.append(os.path.join(sublime.packages_path(), 'PerlPod', 'lib'))

from perl_pod import *
from perl_pod.progress_tracker import PerlPodProgressTracker
from perl_pod.preview_renderer_thread import PerlPodPreviewRendererThread
from perl_pod.preview_renderers.cpan import PerlPodCpanPreviewRenderer


class PerlPodOpenScratchViewCommand(sublime_plugin.TextCommand):

    """
    Command class for opening scratch view.
    """

    def run(self, edit, output='', scratch=True, name=None, syntax=None):
        self.view.insert(edit, self.view.size(), output)

        if scratch:
            self.view.set_scratch(True)
        if name:
            self.view.set_name(name)
        if syntax:
            if syntax == 'html':
                self.view.set_syntax_file('Packages/HTML/HTML.tmLanguage')
            if syntax == 'text':
                self.view.set_syntax_file('Packages/Text/Plain text.tmLanguage')


class PerlPodAbstractCommand(sublime_plugin.TextCommand):

    """
    Abstract command class.
    """

    settings_prefix = None
    default_settings = {
        'enabled': 'True',
    }

    def is_enabled(self, **kwargs):
        return self.get_setting('enabled')

    def get_setting(self, name):
        return PerlPod().get_setting('%s.%s' % (self.settings_prefix, name), self.default_settings[name])


class PerlPodPreviewCpanCommand(PerlPodAbstractCommand):

    """
    Commmand class for renderering POD via CPAN.
    """

    settings_prefix = 'preview.cpan'

    # Main entry point for Sublime Text.
    def run(self, edit, **kwargs):
        try:
            region = sublime.Region(0, self.view.size())

            # Setup renderer, either cpan or pod_text for now.
            renderer_args = {
                "view": self.view,
                "input": self.view.substr(region),
                "filename": self.view.file_name(),
            }
            renderer = PerlPodCpanPreviewRenderer(**renderer_args)

            # Setup renderer thread.
            renderer_thread_args = {
                "view": self.view,
                "renderer": renderer,
                "output_to": 'browser',
            }
            if 'output_to' in kwargs:
                renderer_thread_args['output_to'] = kwargs['output_to']

            thread = PerlPodPreviewRendererThread(**renderer_thread_args)
            thread.start()

            PerlPodProgressTracker(
                thread=thread,
                message='%s: working on CPAN preview' % (PLUGIN_NAME),
                done_message='%s: CPAN preview done' % (PLUGIN_NAME)
            )

        except Exception as e:
            print(repr(e))


class PerlPodPreviewPodTextCommand(PerlPodAbstractCommand):

    """
    Command class for rendering POD locally via external Perl renderer using
    Pod::Text.
    """

    settings_prefix = 'preview.pod_text'

    def run(self, edit, **kwargs):
        sublime.error_message('Rendering POD via Pod::Text not implemented yet.')


class PerlPodPreviewPodHtmlCommand(PerlPodAbstractCommand):

    """
    Command class for rendering POD locally via external Perl renderer using
    Pod::Html.
    """

    settings_prefix = 'preview.pod_html'

    def run(self, edit, **kwargs):
        sublime.error_message('Rendering POD via Pod::HTML not implemented yet.')


class PerlPodOpenPerldocPerlpodCommand(PerlPodAbstractCommand):

    """
    Command class for opening POD documentation on perldoc.org.
    """

    settings_prefix = 'perldoc_perlpod'

    def run(self, edit, **kwargs):
        webbrowser.open_new_tab("http://perldoc.perl.org/perlpod.html")


class PerlPodOpenCheatSheetCommand(PerlPodAbstractCommand):

    """
    Command class for opening POD cheat sheet in scratch window.
    """

    settings_prefix = 'cheat_sheet'
    default_settings = {
        'enabled': True,
        'filepath': os.path.join(sublime.packages_path(), PLUGIN_NAME, 'assets', 'cheat_sheet.pod'),
    }

    def run(self, edit, **kwargs):
        filepath = self.get_setting('filepath')

        try:
            with open(filepath) as fp:
                data = fp.read()
            output_view = self.view.window().new_file()
            output_view.run_command('perl_pod_open_scratch_view', {
                'output': data,
                'name': '%s: POD cheat sheet' % (PLUGIN_GUI_NAME),
                'syntax': 'text',
            })
        except Exception as e:
            print(repr(e))
