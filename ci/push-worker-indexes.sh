#!/bin/bash

git config user.name "${GIT_NAME}"
git config user.email "${GIT_EMAIL}"

random_uuid=$(uuidgen --random)
temp_branch=${random_uuid:(-12)}
git checkout -b ${temp_branch}
git add ./*.json
git commit -m "worker index"
git_ref=$(git rev-parse --verify HEAD)
git checkout master
git pull
git cherry-pick ${git_ref}
git push --quiet "https://${GH_TOKEN}@github.com/minionsmanaged/observations.git" master:master
