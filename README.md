# C-SATS MDM

This package provides end-user device management for C-SATS Ubuntu GNU/Linux workstations.

## Synopsis

```bash
sudo dpkg -i python3-csats-mdm*.deb
test-csats-mdm
```

The second command performs a dry run to preview the data that would be sent to papertrail during an actual run. Use this to check if your system is compliant (e.g. has a 5-minute screen saver timeout).

## Rationale

HITRUST requires a 5-minute screen saver timeout. This package provides a job that will periodically log the current screen saver timeout to confirm a workstation is compliant.

## Prerequisites

None -- all tools should be included in a standard C-SATS developer workstation.

This software will run on (at least) Ubuntu 16.04 and 18.04 64-bit LTS desktop. The Debian package format is used for convenience and consistency with other operating system packages.

## Development

Use a C-SATS Ubuntu 18.04 developer workstation to hack on this code. Any Ubuntu 18.04 computer will do, as would several other flavors of GNU/Linux. The one external dependency is a [log server](https://hub.docker.com/r/meonkeys/pt-log) (really a proxy) listening on localhost port 12004. [Netcat](https://packages.debian.org/stretch/netcat-openbsd) would do just as well (e.g. `nc -v -l 12004`).

Install dev/build/test prerequisites with

```bash
sudo apt install dh-make devscripts python3-all python3-setuptools
```

Here's an example test script. Place it in the parent directory first, then run it from there.

```bash
#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

isDebianPackageInstalled() {
    dpkg-query -W -f='${Status}' "$1" 2>/dev/null | grep -q 'ok installed'
}

set -o xtrace

# clean / prep
package=python3-csats-mdm
if isDebianPackageInstalled $package
then
    sudo apt-get --assume-yes --ignore-missing autoremove --purge $package
fi
rm -rf build
mkdir build
cp -a src build

# build
pushd build/src
time debuild -i -us -uc -b
popd

# install
pushd build
sudo dpkg -i python3-csats-mdm_0.0.2_all.deb
popd
```

## Build/Release

To cut a new release:

1. Build/test locally. The test script (above) is helpful for this.
1. Manually version number to, for example, `0.0.2` in `../test.sh` and `./setup.py`.
1. Add a changelog message. In the dir with this README.md, run something like `dch --package "csats-mdm" --newversion "0.0.2" --distribution stable "Add support for Ubuntu 20.04 LTS."` using the new version number you specified in the previous step. Commit changes to `debian/changelog`.
1. Commit all changes and complete code review per standard C-SATS [software development lifecycle](https://jnj.sharepoint.com/teams/team-csats/_layouts/15/Doc.aspx?sourcedoc=%7B44E9C46D-66E9-4706-B706-B73240E6A54E%7D&file=C-SATS%20Engineering%20Risk%20Management%20-%20SDLC.docx&action=default&mobileredirect=true&DefaultItemOpen=1&cid=f504dfa9-d65c-421c-a37e-5c76062a3caa).
1. Upload `build/python3-csats-mdm_*_all.deb` to `s3://csats.com/mdm/`.

## Backburner: future feature ideas

* host .deb file in an actual private or J&J Debian package repository (J&J already has JFrog artifactory) -- each dev would add it as a package source or "PPA"
* add linting and unit/integration tests
    * shellcheck for checking Bash code
    * lintian for checking Debian package code
    * python linter
    * build/install test
* set up Jenkins CI job, we can download the latest .deb package from there
* add debian/install file to get main script into a sensible location to normalize potential path differences at runtime
