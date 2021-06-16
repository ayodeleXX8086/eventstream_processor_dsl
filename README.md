# Goal
**NOTE** This application was inspired from the [replit event stream processor question](https://replit.com/@ayodeleXX8086/eventstreamprocessor-1#eventStream.json)

This program evaluates an event stream based on some set of rules located in the rules.json file. After the evaluation, if the evaluation turns out to be positive, then the action attached to that rule would be applied to that particular event. To keep this application simple, each event stream would be stored in eventStream.json while the rules are also stored in rules.json. The output of this event would  stored in `output.json` and compared against the `expectedOutput.json`. 
### Rules

#### Junctions

- `all(conditions)`
- `any(conditions)`

#### Operators

- `equalTo(left, right)`
- `notEqualTo(left, right)`
- `greaterThan(left, right)`
- `greaterThanEqual(left, right)`
- `lessThan(left, right)`
- `lessThanEqual(left, right)`
- `matchesRegex(left, right)`

#### Values

- a literal - eg, `1` or `"Zendesk"`
- a keyPath string prefixed with "$" - eg, `"$ui_events.n_keypress"`

#### Actions

- `arrayAppend(keyPath, value)`
- `dropEvent`
- `regexReplace(keyPath, pattern, replacement)`
- `writeField(keyPath, value, overwriteIfExists)`



