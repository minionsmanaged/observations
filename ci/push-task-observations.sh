#!/bin/bash

git config user.name "${GIT_NAME}"
git config user.email "${GIT_EMAIL}"

random_uuid=$(uuidgen --random)
temp_branch=${random_uuid:(-12)}
git checkout -b ${temp_branch}
git add workers/${pool}
git commit -m "tc queue observations for ${pool}"
git_ref=$(git rev-parse --verify HEAD)
git checkout master
git pull
if git cherry-pick ${git_ref}; then
  git push --quiet "https://${GH_TOKEN}@github.com/minionsmanaged/observations.git" master:master
fi
