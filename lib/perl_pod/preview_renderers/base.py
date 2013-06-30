# -*- coding: utf-8 -*-


class PerlPodBasePreviewRenderer(object):

    """Base POD preview renderer class."""

    def __init__(self, view, input, **options):
        self.view = view
        self.input = input
        self.options = options
        self.output = None
        self.output_syntax = None
        self.errors = []

        if 'logger' in options:
            self.logger = options['logger']
        if 'filename' in options:
            self.filename = options['filename']

    def get_output(self):
        return self.output

    def get_output_name(self):
        return "FIXME in PerlPodBasePreviewRenderer"

    def get_output_syntax(self):
        return self.output_syntax

    def render(self):
        return True

    def set_output_syntax(self, syntax):
        self.output_syntax = syntax
