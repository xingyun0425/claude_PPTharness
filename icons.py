# -*- coding: utf-8 -*-
"""Custom icons for this paper's domain (AI self-improvement).
Maps domain-specific icon keys to built-in deckkit icons.
"""

# For this paper (AI self-improvement / recursive learning),
# we map domain concepts to available built-in icons:
# - deployment/training: use 'robot_blue' (AI agent)
# - evaluation: use 'chart' (metrics)
# - research: use 'search' (exploration)
# - verification: use 'gear_blue' (process)
# - warning: use 'warn_rose' (alert)
# - document: use 'doc_grey' (paper)
# - cycle: use 'loop' (iteration)
# - hierarchy: use 'tree' (structure)

ICONS = {
    'deployment': 'robot_blue',   # Deployment-time self-evolution -> AI agent
    'training': 'loop',            # Training-time iteration -> loop icon
    'evaluation': 'chart',         # Evaluation -> chart icon (built-in)
    'research': 'search',          # Research -> search icon (built-in)
    'verifier': 'gear_blue',       # Verification -> gear icon
    'warning': 'warn_rose',        # Warning -> alert icon
    'document': 'doc_grey',        # Document -> paper icon
    'model': 'robot_blue',         # Model -> AI agent
    'checkmark': 'check_blue',     # Success -> checkmark icon
    'cycle': 'loop',               # Cycle/iteration -> loop icon
    'hierarchy': 'folder',         # Hierarchy/structure -> folder icon (layers)
}
