#!/bin/bash

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
${script_dir}/attempt-push.sh workers/${pool} "tc queue observations for ${pool}"
