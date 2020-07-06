FROM debian:bullseye-slim

ARG DEBIAN_FRONTEND=noninteractive

# install just enough system
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
	procps iproute2 \
	curl ca-certificates gpg sudo \
	fakeroot gpg-agent

# language and tools
RUN apt-get install -y --no-install-recommends \
	build-essential \
	python3 python3-dev python3-pip python3-wheel \
	python3-setuptools \
	python3-autopep8 \
	python3-flake8 python3-flake8-docstrings \
	python3-mccabe \
	python3-pytest
RUN python3 -m pip install -U 'python-language-server[all]'

# ensure that we have a clean installation
RUN apt-get install -f
RUN apt-get clean && rm -rf /tmp/* /var/lib/apt/lists/* /var/cache/apt/archives/partial

# --- create user and workarea --- #
# change user so application does not run as root
ENV USER  user
ENV PASS  user
RUN useradd -d /home/user -m -s /bin/bash $USER
RUN mkdir -p /workspace && chown -R $USER: /workspace

COPY . /workspace

# --- from now on run as user --- #
USER $USER
WORKDIR /workspace
CMD [ "./jd_app" ]

