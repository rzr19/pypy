import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append( os.path.join( SCRIPT_DIR, '..' ) )

import traceback

try:
    from git.GitProvider import git, get_git_repos
except ImportError:
    from GitProvider import git, get_git_repos

from Utils import sendemail

SATELLITES_FOLDER = '/home/git/gitlab-satellites'

DEFAULT_EMAIL_ADDRESS = None

def _handle_err_of_git_cmd ( git_cmd, repo, rc, out, err ):

    subject = "[Gitlab] git '%s' command failed" % git_cmd
    traceback_out = traceback.format_exc()
    message = ("git '%s' command failed for repo '%s'" % (git_cmd, repo) ) + \
              ("\n\n[stdout]\n%s\n\n[stderr]\n%s\n\n%s" % (out, err, traceback_out) )
    sendemail( message, subject, to_addr = DEFAULT_EMAIL_ADDRESS )


def check_satellites():
    repos = get_git_repos( SATELLITES_FOLDER )

    print "Found %d satellites" % len(repos)
    for repo in repos:
        print ("Looking in repo '%s'" % repo),
        repo = os.path.join( SATELLITES_FOLDER, repo )
        rc, out, err = git ( [ 'status' ], cwd = repo, exit_on_error = False)
        if (rc != 0):
            _handle_err_of_git_cmd ( 'status', repo, rc, out, err )
            print "got error during git 'status' command; email sent"
        elif (out.find('\nnothing to commit') < 0) and (out.find('\n#Untracked files:') > -1):
            subject = "[Gitlab] Satellite needs attention"
            message = ("Satellite repo '%s' needs to be cleaned up" % (repo) ) + \
                      ("\n\nFor details, see https://gitlab.com") + \
                      ("\n\nOutput for git status command is below" ) + \
                      ("\n\n[stdout]\n%s\n\n[stderr]\n%s" % (out, err) )
            sendemail( message, subject, to_addr = DEFAULT_EMAIL_ADDRESS )
            print "is unclean; email sent"
        else:
            print "is OK"
        sys.stdout.flush()
            

if __name__ == '__main__':
    check_satellites()
