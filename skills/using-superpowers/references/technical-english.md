# Technical English

cf-powers writes technical text in the writing rules of Simplified Technical English
(ASD-STE100). We use the rules, not the STE dictionary: code identifiers and domain
terms stay as they are. Do not call the output "STE compliant".

## Scope

| Text | Rules apply |
|---|---|
| Code comments, docstrings | yes |
| Commit messages, PR descriptions | yes |
| Analysis documents, implementation plans, review reports | yes |
| Technical `docs/`: architecture, ADRs, runbooks, API reference | yes |
| README, user guides, tutorials, marketing text | no |
| User-facing CHANGELOG entries | no |
| Chat with the user | no |

## Sentence shape

1. **One statement per sentence.** At most 20 words for an instruction, 25 for a
   description. A semicolon, a dash or a parenthesis that adds a second statement
   starts a new sentence.
2. **Active voice with a named actor.** The reader must know who does the action.
3. **Imperative for instructions and commit subjects.**
4. **One term for one thing.** Choose the noun once. Do not switch to a synonym later
   ("reservation", then "booking", then "hold").
5. **Articles and "that" stay in.** Do not write telegraph style. "It", "this" and
   "which" appear only when one noun can match.
6. **Simple verbs in full form.** No phrasal verb when a single verb exists. No
   contractions.
7. **Paragraphs carry one topic.** A description paragraph has at most six sentences.

The rules change how a sentence reads, not how many sentences there are. Full sentences
with articles are longer than telegraph style, so cut a sentence before you pad one.

## Examples

| Before | After |
|---|---|
| The event is published only after the transaction commits, so any consumer that reacts to the event and re-reads the row is guaranteed to see the committed state. | The service publishes the event after the transaction commits. Consumers read the reservation row, so they see only committed data. |
| Webhook and cron race; lock+check makes it idempotent. | The webhook and the expiry job can call this function at the same time. The row lock and the state check make the second call do nothing. |
| The row should be locked before the state is checked. | Lock the row before you check the state. |
| Soft-delete via state instead of row deletion, since refund flow still needs it. | Keep the reservation row and set its state to `released`. The refund flow reads the row later. |
| We kick off the sync when the cache doesn't have the key. | The service starts the sync when the cache does not contain the key. |

## Relation to the comment rule

The comment rule in `using-superpowers` decides *whether* a comment exists and what
it says. These rules decide how its sentences read. A comment that the comment rule
removes does not become acceptable because its English is clear.
