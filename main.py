# This is the file that will run on repl.it
import json
import sys
from processor import usage, process_events
if len(sys.argv) > 3:
    usage()

# default to these files in cwd
event_stream_file = "eventStream.json"
rules_file = "rules.json"

if len(sys.argv) == 3:
    event_stream_file = sys.argv[2]
if len(sys.argv) == 2:
    rules_file = sys.argv[1]

event_stream = json.load(open(event_stream_file))
rules = json.load(open(rules_file))
process_events(event_stream, rules)