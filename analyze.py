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


error_str = r"==(\w+)==ERROR"
match_str = r"pc (\w+) bp (\w+) sp (\w+)"
fuzzgoat_line = r"/src/fuzzgoat.c:(\w+)"
main_line = r"/src/main.c:(\w+)"
regex = re.compile(match_str)
error_regex = re.compile(error_str)
main_regex = re.compile(main_line)
fuzzgoat_regex = re.compile(fuzzgoat_line)

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
                print(output.stdout.decode())
                print(output.stderr.decode())
                error_data = output.stderr
                data = error_data.decode()
                main_line_match = main_regex.search(data)
                fuzzgoat_line_match = fuzzgoat_regex.search(data)
                match = regex.search(data)
                error_match = error_regex.search(data)
                if error_match:
                    (error_num,) = error_match.groups()
                    line = "unknown"
                    if fuzzgoat_line_match:
                        (fuzzgoat_line,) = fuzzgoat_line_match.groups()
                        line = f"fuzzgoat.c:{fuzzgoat_line}"
                    if main_line_match:
                        (main_line,) = main_line_match.groups()
                        line = f"main.c:{main_line}"
                    # if main_line_match:
                    # main_line = main_line_match.groups()
                    # pc, bp, sp = match.groups()
                    # err = ASANError(pc, bp, sp)
                    d[line].append(error_num)
                else:
                    print("No match")
                print("------")
    for k, v in d.items():
        print("(", k, "):", ", ".join(v))

        # cmd = f"./fuzzgoat_ASAN {file}"
        # output = subprocess.run(cmd, shell=True, capture_output=True)
        # print(output.stdout)
