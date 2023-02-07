# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 16:51:56 2022

@author: dbh
"""
import os
import hashlib
import json

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def sha1(fname):
    hash_sha1 = hashlib.sha1()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha1.update(chunk)
    return hash_sha1.hexdigest()

def sha256(fname):
    hash_sha256 = hashlib.sha256()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def generate_hash_file(filename):
    hs_md5 = md5(filename)
    # print(h)
    hs_sha1 = sha1(filename)
    hs_sha256 = sha256(filename)
    # print(h)
    d = {'filename': filename, "md5":hs_md5, "sha1":hs_sha1, "sha256":hs_sha256}
    fn = filename[:-3]+"txt"
    with open(fn,'w') as outf:
        json.dump(d,outf)

if __name__ == "__main__":
    filename = "2023-02-07_21.54.43 DCC modified.xml"
    generate_hash_file(filename)

# os.chdir("O:\\Projects\\1901 NY-INFRA-FOT\\DCC\\Examples")