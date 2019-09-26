#!/usr/bin/env python3
#
# Copyright (C) 2019 by Confidential Technologies GmbH
# Copyright (C) 2016 by Intevation GmbH
# Authors:
# Dominik Schürmann <dominik@cotech.de>
# Thomas Arendsen Hein <thomas@intevation.de>
# Andre Heinecke <aheinecke@intevation.de>
#
# This program is free software under the GNU GPL (>=v2)

"""
deploy-wkd

Generate contents of /.well-known/openpgpkey/hu/ for OpenPGP Web Key Service
"""

import sys
import os
import shutil
import hashlib

def zb32_encode(data):
    """Return data in zbase 32 encoding.

    Data must be convertible to a bytearray.

    Implementation is derived from GnuPG's common/zb32.c
    as published in gnupg-2.1.15.
    """
    zb32asc = "ybndrfg8ejkmcpqxot1uwisza345h769"

    data = bytearray(data)
    databits = len(data) * 8
    datalen = int((databits + 7) / 8)

    output = ""

    while datalen >= 5:
        output += zb32asc[((data[0]      ) >> 3)                  ]
        output += zb32asc[((data[0] &   7) << 2) | (data[1] >> 6) ]
        output += zb32asc[((data[1] &  63) >> 1)                  ]
        output += zb32asc[((data[1] &   1) << 4) | (data[2] >> 4) ]
        output += zb32asc[((data[2] &  15) << 1) | (data[3] >> 7) ]
        output += zb32asc[((data[3] & 127) >> 2)                  ]
        output += zb32asc[((data[3] &   3) << 3) | (data[4] >> 5) ]
        output += zb32asc[((data[4] &  31)     )                  ]
        data = data[5:]
        datalen -= 5

    if datalen == 4:
        output += zb32asc[((data[0]      ) >> 3)                  ]
        output += zb32asc[((data[0] &   7) << 2) | (data[1] >> 6) ]
        output += zb32asc[((data[1] &  63) >> 1)                  ]
        output += zb32asc[((data[1] &   1) << 4) | (data[2] >> 4) ]
        output += zb32asc[((data[2] &  15) << 1) | (data[3] >> 7) ]
        output += zb32asc[((data[3] & 127) >> 2)                  ]
        output += zb32asc[((data[3] &   3) << 3)                  ]
    elif datalen == 3:
        output += zb32asc[((data[0]      ) >> 3)                  ]
        output += zb32asc[((data[0] &   7) << 2) | (data[1] >> 6) ]
        output += zb32asc[((data[1] &  63) >> 1)                  ]
        output += zb32asc[((data[1] &   1) << 4) | (data[2] >> 4) ]
        output += zb32asc[((data[2] &  15) << 1)                  ]
    elif datalen == 2:
        output += zb32asc[((data[0]      ) >> 3)                  ]
        output += zb32asc[((data[0] &   7) << 2) | (data[1] >> 6) ]
        output += zb32asc[((data[1] &  63) >> 1)                  ]
        output += zb32asc[((data[1] &   1) << 4)                  ]
    elif datalen == 1:
        output += zb32asc[((data[0]      ) >> 3)                  ]
        output += zb32asc[((data[0] &   7) << 2)                  ]

    # Need to strip some bytes if not a multiple of 40.
    output = output[:int((databits + 5 - 1) / 5)]
    return output

def main(src, relDst, domain):
    wellKnownDst = relDst + "/.well-known/openpgpkey/" + domain + "/"
    keysDst = wellKnownDst + "hu/"
    policyFile = wellKnownDst + "policy"
    os.makedirs(keysDst, exist_ok=True)

    open(policyFile, 'w').close()

    for filename in os.listdir(keysDst):
        os.remove(os.path.join(keysDst, filename))

    for filename in os.listdir(src):
        fullFilename = os.path.join(src, filename)
        if os.path.isfile(fullFilename):
            shutil.copy(fullFilename, keysDst)

    for filename in os.listdir(keysDst):
        localpart = filename.split("@")[0]
        sha1Hash = hashlib.sha1(localpart.encode('utf-8')).digest()
        zb32Filename = zb32_encode(sha1Hash)
        os.rename(os.path.join(keysDst, filename), os.path.join(keysDst, zb32Filename))

if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) > 4:
        sys.stdout.write("usage: %s <keys-dir> <destination-for-well-known> <domain>\n"
                         % sys.argv[0])
        sys.exit(1)
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])

