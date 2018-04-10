#!/bin/bash
# reference: https://gohugo.io/hosting-and-deployment/hosting-on-github/#host-github-user-or-organization-pages

set -e

echo -e "\033[0;32mDeploying updates to GitHub...\033[0m"

# Go To Public folder and ensure we are on master
echo "Update submodule"
cd public
# ensure we are at head
git checkout -- ./*
git clean -f -d
git clean -f -x
git checkout master
git pull origin master

# Build the project.
cd ..
echo "Build website with hugo"
hugo 


# add changes
echo  "Add changes to submodule"
cd  public
git add .

# Commit changes.
msg="rebuilding site `date`"
if [ $# -eq 1 ]
  then msg="$1"
fi
git commit -m "$msg"

# Push source and build repos.
git push origin master

# Come Back up to the Project Root
cd ..

# Update submodule
git add public
git commit -m "deployed site `date`"

echo "Make sure to push your current commit to repo"
