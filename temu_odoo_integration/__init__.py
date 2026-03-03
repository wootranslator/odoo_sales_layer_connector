from . import models
from . import wizard

def post_init_hook(env):
    """Trigger the dummy data wizard after installation."""
    # We create a 'To-do' action that pops up for the user
    # In modern Odoo, we can also use a redirect or just a flag
    # For simplicity, we can create a record in ir.actions.todo (if it exists)
    # or just make sure the user sees it.
    # An easier way is to set a config parameter and show a banner.
    # But for a direct "ask", let's use the todo approach if supported or equivalent.
    todo = env['ir.actions.todo'].create({
        'action_id': env.ref('temu_odoo_integration.action_temu_dummy_wizard').id,
        'name': 'Install Temu Dummy Data',
        'state': 'open',
    })
