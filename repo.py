from git import Repo
import shutil


class Repository(object):

    def __init__(self, url, dest='/tmp', branch='master'):

        self.url = url
        dest = dest.rstrip('/') + '/' + url.split('/')[-1]
        self.dest = dest
        self.branch = branch

    def remove_local_repository(self):

        try:
            shutil.rmtree(self.local_path)
        except Exception as e:
            raise

        return True


class GitRepository(Repository):

    def __init__(self, url, dest='/tmp', branch='master'):
        super().__init__(url, dest, branch)

    def clone_url(self):

        self.remove_local_repository()

        try:
            Repo.clone_from(
                self.url,
                self.local_path,
                branch=self.branch,
            )
            self.is_cloned = True
        except:
            self.remove_local_repository()
            self.local_path = ''
            self.is_cloned = False

        return self.local_path


class HgRepository(Repository):

    def __init__(self, url, to_dir='/tmp/', branch='master'):
        super().__init__(url, to_dir, branch)

    def clone_url(self):
        pass

class SvnRepository(Repository):

    def __init__(self, url, to_dir='/tmp/', branch='master'):
        super().__init__(url, to_dir, branch)

    def clone_url(self):
        pass
