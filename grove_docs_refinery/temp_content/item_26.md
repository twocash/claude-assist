
# A2UI Protocol Evaluation for Grove Inspector Architecture

## Executive Summary

**Bottom Line:** The current implementation is *more compatible* with A2UI than it appears at first glance, but we're not ready to adopt A2UI now. The strategic move is **to build a thin adapter layer** that preserves optionality while we continue development.

<table header-row="true">
	<tr>
		<td>Criterion</td>
		<td>Current State</td>
		<td>A2UI Alignment</td>
	</tr>
	<tr>
		<td>Data addressing</td>
		<td>JSON Pointer (RFC 6901) ✓</td>
		<td>Full compatibility</td>
	</tr>
	<tr>
		<td>Mutation format</td>
		<td>JSON Patch (RFC 6902) ✓</td>
		<td>Full compatibility</td>
	</tr>
	<tr>
		<td>State management</td>
		<td>Imperative (useReducer)</td>
		<td>Conflict - needs reactive binding</td>
	</tr>
	<tr>
		<td>Component rendering</td>
		<td>Hardcoded React</td>
		<td>Conflict - needs schema-driven</td>
	</tr>
	<tr>
		<td>Form handling</td>
		<td>Callback-based</td>
		<td>Partial - needs userAction mapping</td>
	</tr>
</table>
