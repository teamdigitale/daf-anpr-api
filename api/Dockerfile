#
# Base python container to run various jobs
#
FROM python:3.6
RUN pip install tox
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh |  bash &&  apt -y install git-lfs

