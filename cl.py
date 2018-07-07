#!/usr/bin/env python

import requests
import json
import sys

host = "rpi-node1:5000"
base_url = "https://" + host + "/v2/"

headers = {
    'Accept': "application/vnd.docker.distribution.manifest.v2+json"
}

def get_repo():
    r = requests.get(base_url + "_catalog", headers=headers)
    if not r.ok:
        r.raise_for_status()
    return json.loads(r.text)['repositories']

def get_tags(name):
    r = requests.get(base_url + name + "/tags/list", headers=headers)
    if not r.ok:
        r.raise_for_status()
    return json.loads(r.text)['tags']

def get_manifest(name, ref):
    r = requests.get(base_url + name + "/manifests/" + ref, headers=headers)
    if not r.ok:
        r.raise_for_status()
    return json.loads(r.text)

def del_layer(name, digest):
    r = requests.delete(base_url + name + "/blobs/" + ref, headers=headers)
    if not r.ok:
        r.raise_for_status()

def get_digest(name=None, tag=None):

    if name is None:
        repo = get_repo()
    else:
        repo = [ name ]

    res = list()

    for r in repo:

        if tag is None:
            tags = get_tags(r)
        else:
            tags = [ tag ]

        for t in tags:
            m = get_manifest(r, t)
            layers = m['layers']
            for l in layers:
                res.append([ r, t, l['digest'] ])

    return res

def dump_repo(name=None, tag=None):
    for i in get_digest(name, tag):
        print "%s %s %s" % (i[0], i[1], i[2])
    return 0

def del_repo(name=None, tag=None):
    table = get_digest(name, tag)
    return 0

def main(av):

    if len(av) >= 2:
        cmd = av[1]
    else:
        cmd = None

    if len(av) >= 3:
        name = av[2]
    else:
        name = None

    if len(av) >= 4:
        tag = av[3]
    else:
        tag = None

    if (cmd is None) or (cmd == "dump"):
        return dump_repo(name, tag)

    if cmd == "delete":
        del_repo(name, tag)

    return 0


if __name__ == "__main__":
    main(sys.argv)
