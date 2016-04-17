# featherduster
A featherduster. Duh.

## TODO
1. Figure out how violations/reporting work:
	- what do linter functions do/return when there's an infraction?
		- if this is a fairly idiomatic format, how feasible is it to build shims for "common" lint function styles?
	- how should infraction severity work?
		- someone making a linter will inevitably want the notion of different infraction levels/severity
		- some downstream consumer will inevitably want to increase/reduce the severity of an infraction to cause/not-cause CI failures
	- how are useful infraction locations reported when chunkers are modular?
2. Document/text loaders
3. Plugin loader for linter/chunker functions
