import os
import sys

import slackweb

from pywell.entry_points import run_from_cli


DESCRIPTION = 'Send notification to Slack.'

ARG_DEFINITIONS = {
    'SLACK_WEBHOOK': 'Web hook URL for Slack.',
    'SLACK_CHANNEL': 'Slack channel to send to.',
    'TEXT': 'Text to send.'
}

REQUIRED_ARGS = [
    'SLACK_WEBHOOK', 'SLACK_CHANNEL', 'TEXT'
]

def main(args):
    slack = slackweb.Slack(url=args.SLACK_WEBHOOK)
    result = slack.notify(text=args.TEXT, channel=args.SLACK_CHANNEL)
    return result

if __name__ == '__main__':
    run_from_cli(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
