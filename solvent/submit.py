from solvent import config
from solvent import run
from solvent import label
from upseto import gitwrapper
import logging
import os


class Submit:
    def __init__(self, product, directory):
        self._product = product
        self._directory = directory
        git = gitwrapper.GitWrapper(os.getcwd())
        self._basename = git.originURLBasename()
        self._state = "officialcandidate" if config.OFFICIAL_BUILD else "cleancandidate"
        self._label = label.label(
            basename=self._basename, product=self._product, hash=git.hash(), state=self._state)
        run.run([
            "python", "-m", "upseto.main", "checkRequirements",
            "--allowNoManifest", "--unsullied", "--gitClean"])

    def go(self):
        run.run([
            "osmosis", "checkin", self._directory, self._label,
            "--MD5",
            "--objectStores=" + config.LOCAL_OSMOSIS])
        if config.WITH_OFFICIAL_OBJECT_STORE:
            run.run([
                "osmosis", "checkin", self._directory, self._label,
                "--MD5",
                "--objectStores=" + config.OFFICIAL_OSMOSIS])
        logging.info("Submitted as '%(label)s'", dict(label=self._label))