#!/usr/bin/python
# -*-python-*-

# punch-clock version 2010-07-29 (same as version 2008-09-23 but the
# file names and the database directory name have changed)

# Tracks your time as you start and stop work on a project.  See the
# end of the file for the copyright and license.

# Daniel S. Wilkerson

import sys, os
import optparse
import datetime

default_db = '%s/punch-clock-db' % os.environ.get('HOME')

usage = """
punch-clock is a program for tracking your time.

The syntax is:
    punch-clock OPTIONS

Where OPTIONS are:
    --proj=project-name ; project name to file this entry under ; required
    --com=start|stop|note ; what command is this?               ; required
    --note='a note'     ; an note to append to the entry        ; optional
    --db=database-name  ; database dir [%s] ; optional
    --debug             ; if given, print to stdout instead     ; optional

Examples:
    punch-clock --proj=whitherspoon --com=start --note="Feeding Whitherspoon"
    punch-clock --proj=whitherspoon --com=note --note="Cat vomited"
    punch-clock --proj=whitherspoon --com=stop --note="Killed cat"
""" % default_db

def abort(message=None):
    print
    if message:
        print message
    print usage
    exit(1)

# configuration
class Config:

    def parse_arguments(self):
        if len(sys.argv) <= 1: abort()
        parser = optparse.OptionParser()
        parser.add_option('--proj')
        parser.add_option('--com')
        parser.add_option('--note')
        parser.add_option('--db', default=default_db)
        parser.add_option('--debug', action='store_true')
        self.opt, self.arguments = parser.parse_args(sys.argv)
        self.arguments = self.arguments[1:]

    def assert_integrity(self):
        if self.opt.proj == None:
            abort("A proj argument is required.")
        if not (self.opt.com == 'start'
                or self.opt.com == 'stop'
                or self.opt.com == 'note'
                ):
            abort("Bad --com argument '%s'." % self.opt.com)
        if len(self.arguments) > 0:
            abort("Spurious arguments found: %s" % self.arguments)

# routines
def get_now():
    now = datetime.datetime.utcnow()
    now = now.replace(microsecond=0) # don't need them
    return now

def append_to_file(filename, line):
    dbfile = open(filename, 'a')
    dbfile.write(line)
    dbfile.close()

def record():
    now = get_now()

    # construct line
    com = config.opt.com
    note = config.opt.note
    if note: note = ": %s" % note
    else: note = ""
    now_str = now.isoformat('/')
    line = "UTC-%s %s%s\n" % (now_str, com, note)
    if com == "stop": line += "\n"

    # output line
    if config.opt.debug:
        print line
        return
    filename = "%s/%s-%04d-%02d" % (
        config.opt.db,
        config.opt.proj,
        now.year,
        now.month)
    append_to_file(filename, line)

# main
config = Config()
def main():
    config.parse_arguments()
    config.assert_integrity()
    record()

if __name__ == '__main__':
    main()

# License:
#
# Copyright (c) 2008, Daniel S. Wilkerson
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#   Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
#
#   Neither the name of the Daniel S. Wilkerson nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.