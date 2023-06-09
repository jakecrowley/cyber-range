#!/bin/bash
podman run -d -p 127.0.0.1:6379:6379 --name cyberrange-redis redis