#! /usr/bin/env python

import requests
import hashlib
import gzip
import os

class Archiver:

  def __init__(self):
    self.protocol = "http"
    self.addr = "192.168.99.100"
    self.port = 5000
    self.base_url = "{0}://{1}:{2}".format(self.protocol, self.addr, str(self.port))

  def check_and_make_dir(self, directory):
    if os.path.isdir(directory):
      print "Directory: {0} already exists. Continuing without creation of directory.".format(directory)
    else:
      os.makedirs(directory)

  def write_to_file(self, path, contents):
    if os.path.isfile(path):
      print "File: {0} already exists. Continuing without creating new file.".format(path)
    else:
      f = open(path, "w+")
      f.write(contents)
      f.close()

  def get_repos(self):
    try:
      r = requests.get("{0}/v2/_catalog".format(self.base_url))

      if r.status_code != 200:
        print "Did not receive 200 OK from _catalog, perhaps access denied? status_code = {0}".format(r.status_code)
        return None

      j = r.json()
      repos = []
      for repo in j['repositories']:
        print repo
        repos.append(repo)

      return repos

    except:
      print "foobarz"

  def get_tags_for_repo(self, repo):
    try:
      r = requests.get("{0}/v2/{1}/tags/list".format(self.base_url, repo))
      if r.status_code != 200:
        print "Did not receive 200 OK from {0}/tags/list, perhaps access denied? status_code = {1}".format(repo, r.status_code)
        return None

      j = r.json()
      tags = []
      for tag in j['tags']:
        tags.append(tag)

      return tags

    except:
      print "oops"

  def get_image_manifest(self, repo, tag):
    try:
      r = requests.get("{0}/v2/{1}/manifests/{2}".format(self.base_url, repo, tag))
      if r.status_code != 200:
        print "Did not receive 200 OK from {0}/manifests/{1}, perhaps access denied? status_code = {2}".format(repo, tag, r.status_code)
        return None

      j = r.json()
      return r.json()
    except:
      print "oops"

  def get_blobs_from_manifest(self, manifest_json):
    blobs = []
    for layer in manifest_json['fsLayers']: 
      print layer['blobSum']
      blobs.append(layer['blobSum'])
    return blobs

  def fetch_blob_file(self, repo, blobsum):
    # blobsum = sha256:derpderp
    print "foo"
    # GET /v2/<name>/blobs/<digest>
    try:
      r = requests.get("{0}/v2/{1}/blobs/{2}".format(self.base_url, repo, blobsum))
      if r.status_code != 200:
        print "Something went wrong trying to get blobsum: {0}".format(blobsum)
        return None
      else:
        return r.content
    except:
      print "oops"

  def create_layer_json_manifest(self, manifest_json):
    try:
      manifest = {}
      manifest['id'] = ""
      manifest['created'] ="" 
      manifest['container'] = ""
      manifest['container_config'] = ""
      manifest['config'] = ""
      manifest['architecture'] = ""
      manifest['os'] = ""
      manifest['Size'] = ""
      manifest['layer_id'] = ""

    except:
      print "oops"

  def get_all_images(self):
    repos = self.get_repos()
    if (repos is not None):
      # we have repos to get! 
      for repo in repos:
        self.check_and_make_dir("./{0}".format(repo))
        tags = self.get_tags_for_repo(repo)
        if(tags is not None):
          for tag in tags:
            self.check_and_make_dir("./{0}/{1}".format(repo, tag))
            # we have image tags:
            manifest = self.get_image_manifest(repo, tag)
            blobs = self.get_blobs_from_manifest(manifest)
            # get a list of all blobs.
            for blobhash in blobs:
              contents = self.fetch_blob_file(repo, blobhash)
              just_the_hash = blobhash.split(":")[1]
              self.write_to_file("./{0}/{1}/{2}".format(repo, tag, just_the_hash), contents)


archiver = Archiver()
archiver.get_all_images()
