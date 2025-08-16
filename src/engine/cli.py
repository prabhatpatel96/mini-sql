
"""Mini-SQL interactive shell and command runner with input normalization."""
import argparse, sys, os, re
from .executor import create_table, insert, select

PROMPT = "mini-sql> "

def normalize_input(cmd: str) -> str:
    # strip leading pasted prompt like "MiniSQL> " or other prefixes before first SQL keyword
    m = re.search(r'\b(CREATE|INSERT|SELECT|EXIT)\b', cmd, re.I)
    if m:
        cmd = cmd[m.start():]
    # remove inline comments starting with --
    cmd = re.sub(r'--.*$', '', cmd)
    return cmd.strip()

def run_repl():
    print("Mini-SQL shell. Type EXIT; to quit.")
    while True:
        try:
            cmd = input(PROMPT)
        except KeyboardInterrupt:
            print()
            continue
        if not cmd.strip():
            continue
        cmd = normalize_input(cmd)
        if not cmd:
            continue
        if cmd.strip().upper() == "EXIT;":
            print("Bye")
            break
        try:
            if cmd.strip().upper().startswith("CREATE"):
                print(create_table(cmd))
            elif cmd.strip().upper().startswith("INSERT"):
                print(insert(cmd))
            elif cmd.strip().upper().startswith("SELECT"):
                res = select(cmd)
                for r in res:
                    print(r)
                print(f"({len(res)} rows)")
            else:
                print("Unsupported command. Supported: CREATE, INSERT, SELECT, EXIT")
        except Exception as e:
            print("Error:", e)

def run_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("--"):
                continue
            line = normalize_input(line)
            if not line.endswith(";"):
                line = line + ";"
            try:
                if line.upper().startswith("CREATE"):
                    print(create_table(line))
                elif line.upper().startswith("INSERT"):
                    print(insert(line))
                elif line.upper().startswith("SELECT"):
                    res = select(line)
                    for r in res:
                        print(r)
                    print(f"({len(res)} rows)")
            except Exception as e:
                print("Error processing line:", line, e)

def main():
    p = argparse.ArgumentParser(prog="mini-sql", description="Mini-SQL CLI")
    p.add_argument("--file", help="execute SQL file")
    args = p.parse_args()
    if args.file:
        run_file(args.file)
    else:
        run_repl()

if __name__ == "__main__":
    main()
