#!/bin/bash
podman run -dt --name cyberrange-mongo -p 127.0.0.1:27017:27017 -v '$(pwd)/data:/data/db:Z' docker.io/library/mongo:latest