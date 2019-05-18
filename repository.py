from git import Repo
import shutil
import os


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
        
        if not os.path.exists(self.dest):
            return False
        
        try:
            shutil.rmtree(self.dest)
        except Exception as e:
            print(f'remove dir: {e}')
            return False

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
        except Exception as e:
            print(e)
            self.remove_local_repository()
            return None

        return self.dest


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
