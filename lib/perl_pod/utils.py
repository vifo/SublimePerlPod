# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import re


def save_and_prepare_env():
    orig_env = {}

    # On Windows, ensure, that we have CYGWIN environment variables set, even
    # if we don't known, whether we actually are using Cygwin.
    if sys.platform.startswith('win'):
        if 'CYGWIN' in os.environ and not re.match(r'\bnodosfilewarning\b', os.environ['CYGWIN']):
            orig_env['CYGWIN'] = os.environ['CYGWIN']
            os.environ['CYGWIN'] += ' nodosfilewarning'
        else:
            os.environ['CYGWIN'] = 'nodosfilewarning'

        if 'LANG' in os.environ:
            orig_env['LANG'] = os.environ['LANG']

        os.environ['LANG'] = 'C'

    return orig_env


def restore_env(orig_env={}):
    if sys.platform.startswith('win'):

        # Restore environment variables.
        if 'CYGWIN' in orig_env:
            os.environ['CYGWIN'] = orig_env['CYGWIN']
        else:
            del os.environ['CYGWIN']

        if 'LANG' in orig_env:
            os.environ['LANG'] = orig_env['LANG']
        else:
            del os.environ['LANG']

    return True


def get_default_subprocess_args():
    # Prepare arguments for subprocess call.
    subprocess_args = {
        'bufsize': -1,
        'shell': False,
        'stdin': subprocess.PIPE,
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE,
    }

    # Hide console window on Windows.
    if sys.platform.startswith('win'):
        subprocess_args['startupinfo'] = subprocess.STARTUPINFO()
        subprocess_args['startupinfo'].dwFlags |= subprocess.STARTF_USESHOWWINDOW

    return subprocess_args
