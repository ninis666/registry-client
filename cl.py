#!/usr/bin/env python

import json
import sys

import requests

HEADERS = {
    'Accept': "application/vnd.docker.distribution.manifest.v2+json"
}

DEFAULT_HOST = "localhost:5000"
DEFAULT_PROTO = "https"

class docker_registry:

    _base_url = None

    def __init__(self, host=None, proto=None):

        if host is None:
            h = DEFAULT_HOST
        else:
            h = host

        if proto is None:
            p = DEFAULT_PROTO
        else:
            p = proto

        self._base_url = p + "://" + h + "/v2/"

    def get_repo(self):
        r = requests.get(self._base_url + "_catalog", headers=HEADERS)
        if not r.ok:
            r.raise_for_status()
        return json.loads(r.text)['repositories']

    def get_tags(self, name):
        r = requests.get(self._base_url + name + "/tags/list", headers=HEADERS)
        if not r.ok:
            r.raise_for_status()
        return json.loads(r.text)['tags']

    def get_manifest(self, name, ref):
        r = requests.get(self._base_url + name + "/manifests/" + ref, headers=HEADERS)
        if not r.ok:
            r.raise_for_status()
        return json.loads(r.text)

    def del_layer(self, name, digest):
        r = requests.delete(self._base_url + name + "/blobs/" + ref, headers=HEADERS)
        if not r.ok:
            r.raise_for_status()

    def get_digest(self, name=None, tag=None):

        if name is None:
            repo = self.get_repo()
        else:
            repo = [ name ]

        res = list()

        for r in repo:

            if tag is None:
                tags = self.get_tags(r)
            else:
                tags = [ tag ]

            for t in tags:
                m = self.get_manifest(r, t)
                layers = m['layers']
                for l in layers:
                    res.append([ r, t, l['digest'] ])
        return res

    def dump_repo(self, name=None, tag=None):
        for i in self.get_digest(name, tag):
            print "%s %s %s" % (i[0], i[1], i[2])
        return 0

    def del_repo(self, name=None, tag=None):
        table = self.get_digest(name, tag)
        return 0

def main(av):

    if len(av) >= 2:
        host = av[1]
    else:
        host = None

    if len(av) >= 3:
        cmd = av[2]
    else:
        cmd = None

    if len(av) >= 4:
        name = av[3]
    else:
        name = None

    if len(av) >= 5:
        tag = av[4]
    else:
        tag = None

    registry = docker_registry(host)

    if (cmd is None) or (cmd == "dump"):
        return registry.dump_repo(name, tag)

    if cmd == "delete":
        return registry.del_repo(name, tag)

    return 0

if __name__ == "__main__":
    main(sys.argv)
