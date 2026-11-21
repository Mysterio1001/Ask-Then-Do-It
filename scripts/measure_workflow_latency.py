"""Manually time a live workflow session and compare recorded sessions."""

import argparse
import json
import time
from pathlib import Path


SCENARIOS = {
    "button": "Change the Settings button label from Save to Save changes. Keep its click behavior.",
    "search": "Add case-insensitive substring search over template name and description. "
    "A blank query lists all templates in their original order. No matches returns an empty list.",
}
MODES = ("off", "lite", "full")


def summarize(events):
    if not events or events[0] != ["start", 0]:
        raise ValueError("Missing start")
    first = waiting = done = None
    previous = human = replies = rework = 0
    for event, seconds in events[1:]:
        if done is not None or seconds < previous:
            raise ValueError("Events must be chronological and end at completion")
        previous = seconds
        if event == "first" and first is None:
            first = seconds
        elif event == "wait" and waiting is None:
            waiting = seconds
        elif event == "reply" and waiting is not None:
            human += seconds - waiting
            replies += 1
            waiting = None
        elif event == "rework":
            rework += 1
        elif event == "done" and waiting is None:
            done = seconds
            if first is None:
                first = seconds
        else:
            raise ValueError(f"Unexpected {event!r} in the current session state")
    return first, done, human, replies, rework


def record(args):
    print(SCENARIOS[args.scenario])
    print("Press Enter when you submit the initial request. Mark first for the first usable result,")
    print("wait when the AI requires a reply, reply when you send it, rework for a correction cycle,")
    print("and done at verified delivery. Enter simultaneous marks on one line, e.g. first wait.")
    header = {"kind": "manual-live", "scenario": args.scenario, "mode": args.mode,
              "host": args.host, "model": args.model}
    with args.output.open("x", encoding="utf-8") as log:
        print(json.dumps(header, ensure_ascii=False), file=log, flush=True)
        input("Ready: ")
        start = time.monotonic()
        events = [["start", 0]]
        print(json.dumps(events[0]), file=log, flush=True)
        while True:
            marks = input("Mark: ").lower().split()
            elapsed = round(time.monotonic() - start, 3)
            additions = [[mark, elapsed] for mark in marks]
            try:
                _, done, *_ = summarize(events + additions)
            except ValueError as error:
                print(error)
                continue
            events.extend(additions)
            for event in additions:
                print(json.dumps(event), file=log, flush=True)
            if done is not None:
                return


def report(paths):
    print("host\tmodel\tscenario\tmode\tfirst_s\ttotal_s\thuman_s\tnonhuman_s\treplies\trework")
    for path in paths:
        records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        if not records or not isinstance(records[0], dict) or records[0].get("kind") != "manual-live":
            raise ValueError(f"{path}: expected a manual-live recording")
        header = records[0]
        first, done, human, replies, rework = summarize(records[1:])
        if done is None:
            raise ValueError(f"{path}: run is incomplete")
        print(header["host"], header["model"], header["scenario"], header["mode"],
              f"{first:.3f}", f"{done:.3f}", f"{human:.3f}", f"{done - human:.3f}",
              replies, rework, sep="\t")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    new = commands.add_parser("record", help="time a live session using terminal marks")
    new.add_argument("scenario", choices=SCENARIOS)
    new.add_argument("mode", choices=MODES)
    new.add_argument("--host", required=True)
    new.add_argument("--model", required=True)
    new.add_argument("--output", type=Path, required=True, help="new JSONL recording")
    results = commands.add_parser("report", help="print one comparable row per completed recording")
    results.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "record":
            record(args)
        else:
            report(args.files)
    except (OSError, ValueError, KeyError, EOFError, KeyboardInterrupt) as error:
        parser.exit(1, f"Measurement stopped: {error}\n")


if __name__ == "__main__":
    main()
