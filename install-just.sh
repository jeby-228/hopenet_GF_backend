#!/bin/bash -ex

curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --tag 1.42.4 ${@:---to /bin}
