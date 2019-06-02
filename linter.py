import os
from SublimeLinter.lint import Linter


class Standardrb(Linter):
    defaults = {
        'selector': 'source.ruby - text.html - text.haml'
    }
    regex = (
        r'^.+?:(?P<line>\d+):(?P<col>\d+): '
        r'(:?(?P<warning>[RCW])|(?P<error>[EF])): '
        r'(?P<message>.+)'
    )

    def cmd(self):
        """Build command, using STDIN if a file path can be determined."""

        settings = self.get_view_settings()

        command = []

        if settings.get('use_bundle_exec', False):
            command.extend(['bundle', 'exec'])

        command.extend(['standardrb', '--format', 'emacs'])

        # Set tempfile_suffix so by default a tempfile is passed onto rubocop:
        self.tempfile_suffix = 'rb'

        path = self.filename
        if path:
            folders = self.view.window().folders()
            if folders:
                gemfile_lock = os.path.join(folders[0], 'Gemfile.lock')
                if ' standard ' in open(gemfile_lock).read():
                    # The 'force-exclusion' overrides rubocop's behavior of ignoring
                    # global excludes when the file path is explicitly provided:
                    command += ['--force-exclusion', '--stdin', path]
                    # Ensure the files contents are passed in via STDIN:
                    self.tempfile_suffix = None

                    return command
