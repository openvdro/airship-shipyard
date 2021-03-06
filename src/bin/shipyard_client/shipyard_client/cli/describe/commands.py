# Copyright 2017 AT&T Intellectual Property.  All other rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Describe command

import click

from click_default_group import DefaultGroup

from shipyard_client.cli.describe.actions import DescribeAction
from shipyard_client.cli.describe.actions import DescribeNotedetails
from shipyard_client.cli.describe.actions import DescribeStep
from shipyard_client.cli.describe.actions import DescribeValidation
from shipyard_client.cli.describe.actions import DescribeWorkflow
from shipyard_client.cli.input_checks import check_id, check_workflow_id


@click.group(cls=DefaultGroup, default='describe_default_command')
@click.pass_context
def describe(ctx):
    """
    Describe the action, step, note details or validation. \n
    For more information on describe commands
    please enter the describe command followed by '--help' \n
    Example: shipyard describe action --help \n

    FOR NAMESPACE ENTRIES: \n
        COMMAND: (no sub command) \n
        DESCRIPTION: Retrieves the detailed information about the supplied
        namespaced item. \n
        FORMAT: shipyard describe <namespace item> \n
        EXAMPLE: shipyard describe action/01BTG32JW87G0YKA1K29TKNAFX | shipyard
    describe step/01BTG32JW87G0YKA1K29TKNAFX/preflight | shipyard describe
    validation/01BTG32JW87G0YKA1K29TKNAFX/01BTG3PKBS15KCKFZ56XXXBGF2 | shipyard
    describe notedetails/01BTG32JW87G0YKA1KA9AKAAB3
    """


@describe.command('describe_default_command', short_help="")
@click.argument('namespace_item')
@click.pass_context
def describe_default_command(ctx, namespace_item):
    try:
        namespace = namespace_item.split("/")
        if namespace[0] == 'action':
            ctx.invoke(describe_action, action_id=namespace[1])
        elif namespace[0] == 'step':
            ctx.invoke(
                describe_step, step_id=namespace[2], action=namespace[1])
        elif namespace[0] == 'validation':
            ctx.invoke(
                describe_validation,
                validation_id=namespace[1],
                action=namespace[2])
        elif namespace[0] == 'workflow':
            ctx.invoke(
                describe_workflow,
                workflow_id=namespace[1])
        elif namespace[0] == 'notedetails':
            ctx.invoke(
                describe_notedetails,
                note_id=namespace[1])
        else:
            raise Exception('Invalid namespaced describe action')
    except Exception:
        ctx.fail("Invalid namespace item. Please utilize one of the following "
                 "formats for the namespace item.\n"
                 "action: action/action id\n"
                 "step: step/action id/step id\n"
                 "validation: validation/validation id/action id\n"
                 "workflow: workflow/workflow id\n"
                 "notedetails: notedetails/note_id")


DESC_ACTION = """
COMMAND: describe action \n
DESCRIPTION: Retrieves the detailed information about the supplied action
id. \n
FORMAT: shipyard describe action <action id> \n
EXAMPLE: shipyard describe action 01BTG32JW87G0YKA1K29TKNAFX
"""

SHORT_DESC_ACTION = ("Retrieves the detailed information about the supplied"
                     "action id.")


@describe.command('action', help=DESC_ACTION, short_help=SHORT_DESC_ACTION)
@click.argument('action_id')
@click.pass_context
def describe_action(ctx, action_id):

    if not action_id:
        ctx.fail("An action id argument must be passed.")

    check_id(ctx, action_id)

    click.echo(DescribeAction(ctx, action_id).invoke_and_return_resp())


DESC_NOTEDETAILS = """
COMMAND: describe notedetials \n
DESCRIPTION: Retrieves the detailed information that is associated with the
specified note id. \n
FORMAT: shipyard describe notedetails <note id> \n
EXAMPLE: shipyard describe notedetails 01BTG32JW87G0YKA1KA9AKAAB3
"""

SHORT_DESC_NOTEDETAILS = (
    "Retrieves the detailed information about the supplied action id.")


@describe.command('notedetails',
    help=DESC_NOTEDETAILS, short_help=SHORT_DESC_NOTEDETAILS)
@click.argument('note_id')
@click.pass_context
def describe_notedetails(ctx, note_id):

    if not note_id:
        ctx.fail("A note id argument must be passed.")

    check_id(ctx, note_id)

    click.echo(DescribeNotedetails(ctx, note_id).invoke_and_return_resp())


DESC_STEP = """
COMMAND: describe step \n
DESCRIPTION: Retrieves the step details associated with an action and step. \n
FORMAT: shipyard describe step <step id> --action=<action id> \n
EXAMPLE: shipyard describe step preflight
--action=01BTG32JW87G0YKA1K29TKNAFX 786d416c-bf70-4705-a9bd-6670a4d7bb60
"""

SHORT_DESC_STEP = ("Retrieves the step details associated with an action and "
                   "step.")


@describe.command('step', help=DESC_STEP, short_help=SHORT_DESC_STEP)
@click.argument('step_id')
@click.option(
    '--action',
    '-a',
    help='The action id that provides the context for this step')
@click.pass_context
def describe_step(ctx, step_id, action):

    check_id(ctx, action)

    click.echo(DescribeStep(ctx, action, step_id).invoke_and_return_resp())


DESC_VALIDATION = """
COMMAND: describe validation \n
DESCRIPTION: Retrieves the validation details assocaited with an action and
validation id. \n
FORMAT: shipyard describe validation <validation id> --action=<action id>\n
EXAMPLE: shipyard describe validation 01BTG3PKBS15KCKFZ56XXXBGF2
--action=01BTG32JW87G0YKA1K29TKNAFX
"""

SHORT_DESC_VALIDATION = ("Retrieves the validation details assocaited with an "
                         "action and validation id.")


@describe.command(
    'validation', help=DESC_VALIDATION, short_help=SHORT_DESC_VALIDATION)
@click.argument('validation_id')
@click.option(
    '--action',
    '-a',
    help='The action id that provides the context for this validation')
@click.pass_context
def describe_validation(ctx, validation_id, action):

    check_id(ctx, validation_id)
    check_id(ctx, action)

    click.echo(
        DescribeValidation(ctx, validation_id, action)
        .invoke_and_return_resp())


DESC_WORKFLOW = """
COMMAND: describe workflow \n
DESCRIPTION: Retrieves the detailed information about the supplied workflow
id. \n
FORMAT: shipyard describe workflow <workflow id> \n
EXAMPLE: shipyard describe workflow deploy_site__2017-10-09T21:19:03.000000
"""

SHORT_DESC_WORKFLOW = ("Retrieves the detailed information about the supplied"
                       " workflow id.")


@describe.command(
    'workflow',
    help=DESC_WORKFLOW,
    short_help=SHORT_DESC_WORKFLOW)
@click.argument('workflow_id')
@click.pass_context
def describe_workflow(ctx, workflow_id):

    if not workflow_id:
        ctx.fail("An action id argument must be passed.")

    check_workflow_id(ctx, workflow_id)

    click.echo(DescribeWorkflow(ctx, workflow_id).invoke_and_return_resp())
