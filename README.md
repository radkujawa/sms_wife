# sms_wife
send sms to wife when work ends

# usage

* ```pip install twilio requests plumbum```

* ```crontab -e``` -> add ```* * * * * python [path-to-sms_wife]/sms_wife.py --account-sid "TWILIO_SID" --auth-token "TWILIO_TOKEN" --wife "+48........." --sender "TWILIO_NUMBER" --login "WORKTIME_LOGIN" --worktime-url "URL_TO_WORKTIME" "SMS_CONTENT" > /dev/null```

* enjoy!
