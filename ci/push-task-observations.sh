#!/bin/bash

git config user.name "${GIT_NAME}"
git config user.email "${GIT_EMAIL}"

random_uuid=$(uuidgen --random)
temp_branch=${random_uuid:(-12)}
git checkout -b ${temp_branch}
git add workers/${pool}
git commit -m "tc queue observations for ${pool}"
git format-patch master --stdout > ${temp_branch}.patch
git checkout master
git pull
git apply ${temp_branch}.patch --stat
git apply ${temp_branch}.patch --check
git apply ${temp_branch}.patch
git push --quiet "https://${GH_TOKEN}@github.com/minionsmanaged/observations.git" master:master
