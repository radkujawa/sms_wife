# sms_wife
send sms to wife when work ends

# usage

* ```pip install twilio requests plumbum```

* ```crontab -e``` -> add ```* * * * * python [path-to-sms_wife]/sms_wife.py --twilio-account-sid "TWILIO_SID" --twilio-auth-token "TWILIO_TOKEN" --wife "+48........." --twilio-sender "TWILIO_NUMBER" --login "WORKTIME_LOGIN" --worktime-url "URL_TO_WORKTIME" "SMS_CONTENT" > /dev/null```

* your personal arguments should be only `--login` and `--wife`

* enjoy!

# remarks

tested only in python 3.6.

Patches welcome!