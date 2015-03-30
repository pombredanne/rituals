# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation
""" Shell command calls.
"""
# Copyright ⓒ  2015 Jürgen Hermann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# The full LICENSE file and source are available at
#    https://github.com/jhermann/rituals
from __future__ import absolute_import, unicode_literals, print_function

import os
import sys

from invoke import run as invoke_run
from invoke import exceptions

from . import notify


def capture(cmd, **kw):
    """Run a command and return its stripped captured output."""
    kw = kw.copy()
    kw['hide'] = 'out'
    if not kw.get('echo', False):
        kw['echo'] = False
    try:
        return invoke_run(cmd, **kw).stdout.strip()
    except exceptions.Failure as exc:
        notify.error("Command `{}` failed with RC={}!".format(cmd, exc.result.return_code,))
        raise


def run(cmd, **kw):
    """Run a command and flush its output."""
    kw = kw.copy()
    if 'warn' not in kw:
        kw['warn'] = False  # make extra sure errors don't get silenced
    if os.name == 'posix':
        cmd += ' 2>&1'  # ensure ungarbled output

    report_error = True
    if 'report_error' in kw:
        report_error = kw['report_error']
        del kw['report_error']

    try:
        return invoke_run(cmd, **kw)
    except exceptions.Failure as exc:
        sys.stdout.flush()
        sys.stderr.flush()
        if report_error:
            notify.error("Command `{}` failed with RC={}!".format(cmd, exc.result.return_code,))
        raise
    finally:
        sys.stdout.flush()
        sys.stderr.flush()
