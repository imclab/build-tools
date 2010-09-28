#!/usr/bin/python
"""%prog [-p|--props-file] [-r|--rev revision] [-b|--branch branch] repo [dest]

Tool to do safe operations with hg.

revision/branch on commandline will override those in props-file"""

# Import snippet to find tools lib
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../lib/python"))

from util.hg import mercurial

if __name__ == '__main__':
    from optparse import OptionParser
    import os, logging

    parser = OptionParser(__doc__)
    parser.set_defaults(
            revision=os.environ.get('HG_REV'),
            branch=os.environ.get('HG_BRANCH', 'default'),
            propsfile=os.environ.get('PROPERTIES_FILE'),
            tbox=bool(os.environ.get('PROPERTIES_FILE')),
            loglevel=logging.INFO,
            )
    parser.add_option("-r", "--rev", dest="revision", help="which revision to update to")
    parser.add_option("-b", "--branch", dest="branch", help="which branch to update to")
    parser.add_option("-p", "--props-file", dest="propsfile",
        help="build json file containing revision information")
    parser.add_option("--tbox", dest="tbox", action="store_true",
        help="output TinderboxPrint messages")
    parser.add_option("--no-tbox", dest="tbox", action="store_false",
        help="don't output TinderboxPrint messages")

    options, args = parser.parse_args()

    logging.basicConfig(level=options.loglevel, format="%(message)s")

    if len(args) not in (1, 2):
        parser.error("Invalid number of arguments")

    repo = args[0]
    if len(args) == 2:
        dest = args[1]
    else:
        dest = os.path.basename(repo)

    # Parse propsfile
    if options.propsfile:
        try:
            import json
        except ImportError:
            import simplejson as json
        js = json.load(open(options.propsfile))
        if options.revision is None:
            options.revision = js['sourcestamp']['revision']
        if options.branch is None:
            options.branch = js['sourcestamp']['branch']

    got_revision = mercurial(repo, dest, options.branch, options.revision)

    if options.tbox:
        print "TinderboxPrint: revision: %s" % got_revision
    else:
        print "Got revision %s" % got_revision
