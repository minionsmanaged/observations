#!/bin/bash

git config user.name "${GIT_NAME}"
git config user.email "${GIT_EMAIL}"

temp_branch=$(uuidgen --random)
git checkout -b ${temp_branch}
git add $1
git commit -m $2
git format-patch master --stdout > ${temp_branch}.patch
git checkout master
git pull
if git apply --stat ${temp_branch}.patch && git apply --check ${temp_branch}.patch; then
  git apply ${temp_branch}.patch
  git push --quiet "https://${GH_TOKEN}@github.com/minionsmanaged/observations.git" master:master
fi
