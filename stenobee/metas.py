# stenobee/metas.py

import inflect

def pluralize(ctx, _):
  p = inflect.engine()

  last_word = ctx.last_fragments()[0]

  action = ctx.copy_last_action()
  action.prev_replace = last_word
  action.text = p.plural(last_word)
  action.prev_attach = True

  return action
