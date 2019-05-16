from git import Repo
import shutil


class Repository(object):

    def __init__(self, url, dest=None, branch=None):

        self.url = url
        self.repo = url.split('/')[-1]
        if not dest:
            dest = '/tmp'
        if not branch:
            branch = 'master'
        self.dest = dest.rstrip('/') + '/' + self.repo
        self.branch = branch

    def remove_local_repository(self):

        try:
            shutil.rmtree(self.local_path)
        except Exception as e:
            raise

        return True


class GitRepository(Repository):

    def __init__(self, url, dest=None, branch=None):
        super().__init__(url, dest, branch)

    def clone_url(self):

        self.remove_local_repository()

        try:
            Repo.clone_from(
                self.url,
                self.dest,
                branch=self.branch,
            )
        except:
            self.remove_local_repository()

        return self.local_path


class HgRepository(Repository):

    def __init__(self, url, dest=None, branch=None):
        super().__init__(url, to_dir, branch)

    def clone_url(self):
        pass

class SvnRepository(Repository):

    def __init__(self, url, to_dir=None, branch=None):
        super().__init__(url, to_dir, branch)

    def clone_url(self):
        pass
