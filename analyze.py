import re
from collections import defaultdict
import sys
import subprocess
import os


class ASANError:
    def __init__(self, pc, bp, sp):
        self.pc = pc
        self.bp = bp
        self.sp = sp

    def __str__(self):
        return f"pc: {self.pc}, bp: {self.bp}, sp: {self.sp}"

    def __repr__(self):
        return f"ASANError(pc={self.pc}, bp={self.bp}, sp={self.sp})"

    def __eq__(self, other):
        return self.pc == other.pc and self.bp == other.bp and self.sp == other.sp

    def __hash__(self):
        return hash((self.pc, self.bp, self.sp))


match_str = r"==(\w+)==ERROR.*pc (\w+) bp (\w+) sp (\w+)"
main_line = r"/src/main.c:(\w+)"
regex = re.compile(match_str)
main_regex = re.compile(main_line)

d = defaultdict(list)

# read each dir in "sync_dir" and iterate over the crashes subdir
# for each crash, run "./fuzzgoat_ASAN <crash_file>" and parse the output
if __name__ == "__main__":
    for dir in os.listdir("./sync_dir"):
        for root, dirs, files in os.walk(f"./sync_dir/{dir}/crashes"):
            for file in files:
                print("------")
                cmd = f"./fuzzgoat_ASAN {root}/{file}"
                print(cmd)
                output = subprocess.run(cmd, shell=True, capture_output=True)
                print(output.stdout)
                print(output.stderr)
                error_data = output.stderr
                data = error_data.decode("utf-8")
                main_line_match = main_regex.search(data)
                match = regex.search(data)
                if match and main_line_match:
                    (main_line,) = main_line_match.groups()
                    # if main_line_match:
                    # main_line = main_line_match.groups()
                    num, pc, bp, sp = match.groups()
                    err = ASANError(pc, bp, sp)
                    d[main_line].append(num)
                    print(err)
                else:
                    print("No match")
                print("------")
    for k, v in d.items():
        print("(", k, "):", ", ".join(v))

        # cmd = f"./fuzzgoat_ASAN {file}"
        # output = subprocess.run(cmd, shell=True, capture_output=True)
        # print(output.stdout)
