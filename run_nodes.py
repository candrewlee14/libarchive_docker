#!/usr/bin/env python3

import os
import subprocess
import random
import time

# Got information about these options from this page:
# https://aflplus.plus/docs/fuzzing_in_depth/

extra_fuzz_options = [
    [
        (0.9, []),
        (0.1, ["-L", "0"]),
    ],
    [
        (0.9, []),
        (0.1, ["-Z"]),
    ],
    [
        (0.3, []),
        (0.3, ["-a", "ascii"]),
        (0.4, ["-a", "binary"]),
    ],
    [
        (0.1, ["-p", "fast"]),
        (0.1, ["-p", "explore"]),
        (0.1, ["-p", "coe"]),
        (0.1, ["-p", "lin"]),
        (0.1, ["-p", "quad"]),
        (0.1, ["-p", "exploit"]),
        (0.1, ["-p", "rare"]),
    ],
]
random.seed(42)


# Run zellij action go-to-tab-name "fuzz-nodes"
subprocess.run(
    [
        "zellij",
        "action",
        "go-to-tab-name",
        "fuzz-nodes",
    ],
)
cores = os.cpu_count() or 8
# We want to leave 3 cores free for the rest of the system
# 1 main node, 1 ubsan node, 1 left for user
num_workers = cores - 3
for i in range(num_workers):
    extra_options = []
    for option_sets in extra_fuzz_options:
        weights, args = zip(*option_sets)
        extra_options.extend(*random.choices(args, weights=weights, k=1))
    print(extra_options)
    # zellij action new-pane -- afl-fuzz -i in -o sync_dir -S f0$i ./fuzzgoat @@
    cmd = [
        "zellij",
        "action",
        "new-pane",
        "--",
        "afl-fuzz",
        "-i",
        "in",
        "-o",
        "sync_dir",
        "-S",
        "s{:0>{}}".format(i, 2),
        *extra_options,
        "./fuzzgoat",
        "@@",
    ]
    print(" ".join(cmd))
    subprocess.run(
        cmd,
    )
    time.sleep(0.5)

subprocess.run(
    [
        "zellij",
        "action",
        "go-to-tab-name",
        "sh",
    ],
)
