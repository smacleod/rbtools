from rbtools.commands import Command, Option
from rbtools.utils.process import die


class Diff(Command):
    """Prints a diff to the terminal."""
    name = "diff"
    author = "The Review Board Project"
    args = "[changenum]"
    option_list = [
        Option("--server",
               dest="server",
               metavar="SERVER",
               config_key="REVIEWBOARD_URL",
               default=None,
               help="specify a different Review Board server to use"),
        Option("--revision-range",
               dest="revision_range",
               default=None,
               help="generate the diff for review based on given "
                    "revision range"),
        Option("--parent",
               dest="parent_branch",
               metavar="PARENT_BRANCH",
               help="the parent branch this diff should be against "
                    "(only available if your repository supports "
                    "parent diffs)"),
        Option("--tracking-branch",
               dest="tracking",
               metavar="TRACKING",
               help="Tracking branch from which your branch is derived "
                    "(git only, defaults to origin/master)"),
        Option('--svn-changelist',
               dest='svn_changelist',
               default=None,
               help='generate the diff for review based on a local SVN '
                    'changelist'),
        Option("--repository-url",
               dest="repository_url",
               help="the url for a repository for creating a diff "
                    "outside of a working copy (currently only "
                    "supported by Subversion with --revision-range or "
                    "--diff-filename and ClearCase with relative "
                    "paths outside the view). For git, this specifies"
                    "the origin url of the current repository, "
                    "overriding the origin url supplied by the git "
                    "client."),
        Option("-d", "--debug",
               action="store_true",
               dest="debug",
               config_key="DEBUG",
               default=False,
               help="display debug output"),
        Option("--username",
               dest="username",
               metavar="USERNAME",
               config_key="USERNAME",
               default=None,
               help="user name to be supplied to the Review Board server"),
        Option("--password",
               dest="password",
               metavar="PASSWORD",
               config_key="PASSWORD",
               default=None,
               help="password to be supplied to the Review Board server"),
    ]

    def get_diff(self, *args):
        """Returns a diff as a string."""
        repository_info, tool = self.initialize_scm_tool()
        server_url = self.get_server_url(repository_info, tool)
        root_resource = self.get_root(server_url)
        self.setup_tool(tool, api_root=root_resource)

        if self.options.revision_range:
            diff, parent_diff = tool.diff_between_revisions(
                self.options.revision_range,
                args,
                repository_info)
        elif self.options.svn_changelist:
            diff, parent_diff = tool.diff_changelist(
                self.options.svn_changelist)
        else:
            diff, parent_diff = tool.diff(list(args))

        return diff

    def main(self, *args):
        """Print the diff to terminal."""
        diff = self.get_diff(*args)

        if not diff:
            die("There don't seem to be any diffs!")

        print diff
