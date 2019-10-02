import datetime
import re
import sys
import time
from argparse import ArgumentParser

import requests
from plumbum import cmd
from twilio.rest import Client

PRESENT = "present"
ABSENT = "absent"
ATTENDANCE_FILE = "/tmp/attendance"
WORKTIME_URL_FORMAT = "{worktime_url}/json?userName={user}&action=GETATTENDANCE"


def send_sms(args, body):
    client = Client(args.twilio_account_sid, args.twilio_auth_token)
    client.messages.create(from_=args.twilio_sender, body=body, to=args.wife)


def main(args):

    if args.force:
        send_sms(args, args.sms_content)
        return

    resp = requests.get(WORKTIME_URL_FORMAT.format(user=args.login, worktime_url=args.worktime_url))
    users = str(resp.content).split("\\n")

    my_entry = [user for user in users if re.match(f"^{args.login},.*(Work time)", user)]
    assert len(my_entry) <= 1
    pretty_now = datetime.datetime.fromtimestamp(int(time.time()))

    if len(my_entry) == 1:

        print(f"{pretty_now} I'm present")
        (cmd.echo[PRESENT] > ATTENDANCE_FILE)()

    else:

        print(f"{pretty_now} I'm absent")
        previous_status = cmd.cat[ATTENDANCE_FILE](retcode=None).strip()

        if previous_status == PRESENT:
            (cmd.echo[ABSENT] > ATTENDANCE_FILE)()
            print(f"{pretty_now} Sending SMS with changing status notification", file=sys.stderr)
            send_sms(args, f"{pretty_now} {args.sms_content}")


def parse_cmdline():
    parser = ArgumentParser()
    parser.add_argument(
        "--twilio-account-sid",
        "--account-sid",
        type=str,
        required=True,
        help="twilio account sid that can be obtained on twilio account at twilio.com",
    )
    parser.add_argument(
        "--twilio-auth-token",
        "--auth-token",
        type=str,
        required=True,
        help="twilio auth token that can be obtained on twilio account at twilio.com",
    )
    parser.add_argument(
        "--twilio-sender",
        "--sender",
        type=str,
        required=True,
        help="phone number that is registered as sender at twilio account (that with sid and token)",
    )
    parser.add_argument(
        "--force", action="store_true", default=False, help="send sms unconditionally (even if at work)"
    )
    parser.add_argument("--wife", type=str, required=True, help="actual number to your wife")
    parser.add_argument("--login", type=str, required=True, help="worktime login")
    parser.add_argument("--worktime-url", type=str, required=True, help="full url to worktime internal service")
    parser.add_argument("sms_content", metavar="SMS")
    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main(parse_cmdline()))
