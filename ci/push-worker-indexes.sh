#!/bin/bash

git config user.name "${GIT_NAME}"
git config user.email "${GIT_EMAIL}"

random_uuid=$(uuidgen --random)
temp_branch=${random_uuid:(-12)}
git checkout -b ${temp_branch}
git add ./*.json
git commit -m "worker index"
git format-patch master --stdout > ${temp_branch}.patch
git checkout master
git pull
if git apply --stat ${temp_branch}.patch && git apply --check ${temp_branch}.patch; then
  git apply ${temp_branch}.patch
  git push --quiet "https://${GH_TOKEN}@github.com/minionsmanaged/observations.git" master:master
fi
