#!/usr/bin/python3

import sem6000

import datetime
import sys

def _format_minutes_as_time(minutes):
    hour = minutes // 60
    minute = minutes - hour*60

    return "{:02}:{:02}".format(hour, minute)


def _format_hour_and_minute_as_time(hour, minute):
    return "{:02}:{:02}".format(hour, minute)


def _parse_boolean(boolean_string):
    boolean_value = False

    if str(boolean_string).lower() == "true":
        boolean_value = True
    if str(boolean_string).lower() == "on":
        boolean_value = True
    if str(boolean_string).lower() == "1":
        boolean_value = True

    return boolean_value


if __name__ == '__main__':
    if len(sys.argv) == 1:
        devices = sem6000.SEM6000.discover()
        for device in devices:
            print(device['name'] + '\t' + device['address'])
    else:
        deviceAddr = sys.argv[1]
        pin = sys.argv[2]
        cmd = sys.argv[3]

        sem6000 = sem6000.SEM6000(deviceAddr, pin, debug=True)

        if cmd != 'reset_pin':
            sem6000.authorize()

        if cmd == 'change_pin':
            sem6000.change_pin(sys.argv[4])
        if cmd == 'reset_pin':
            sem6000.reset_pin()
        if cmd == 'power_on':
            sem6000.power_on()
        if cmd == 'power_off':
            sem6000.power_off()
        if cmd == 'led_on':
            sem6000.led_on()
        if cmd == 'led_off':
            sem6000.led_off()
        if cmd == 'set_date_and_time':
            sem6000.set_date_and_time(sys.argv[4])
        if cmd == 'synchronize_date_and_time':
            sem6000.set_date_and_time(datetime.datetime.now().isoformat())
        if cmd == 'request_settings':
            response = sem6000.request_settings()
            assert isinstance(response, RequestedSettingsNotification)

            print("Settings:")
            if response.is_reduced_mode_active:
                print("\tReduced mode:\t\tOn")
            else:
                print("\tReduced mode:\t\tOff")

            print("\tNormal price:\t\t{:.2f} EUR".format(response.normal_price_in_cent/100))
            print("\tReduced price:\t\t{:.2f} EUR".format(response.reduced_price_in_cent/100))

            print("\tRecuced mode start:\t{} minutes ({})".format(response.reduced_mode_start_time_in_minutes, _format_minutes_as_time(response.reduced_mode_start_time_in_minutes)))
            print("\tRecuced mode end:\t{} minutes ({})".format(response.reduced_mode_end_time_in_minutes, _format_minutes_as_time(response.reduced_mode_end_time_in_minutes)))

            if response.is_led_active:
                print("\tLED state;\t\tOn")
            else:
                print("\tLED state;\t\tOff")

            print("\tPower limit:\t\t{} W".format(response.power_limit_in_watt))
        if cmd == 'set_power_limit':
            sem6000.set_power_limit(power_limit_in_watt=sys.argv[4])
        if cmd == 'set_prices':
            sem6000.set_prices(normal_price_in_cent=sys.argv[4], reduced_price_in_cent=sys.argv[5])
        if cmd == 'set_reduced_period':
            sem6000.set_reduced_period(is_active=sys.argv[4], start_isotime=sys.argv[5], end_isotime=sys.argv[6])
        if cmd == 'request_timer_status':
            response = sem6000.request_timer_status()
            assert isinstance(response, RequestedTimerStatusNotification)

            original_timer_length = datetime.timedelta(seconds=response.original_timer_length_in_seconds)

            print("Timer Status:")
            if response.is_timer_running:
                now = datetime.datetime.now()
                now = datetime.datetime(now.year % 100, now.month, now.day, now.hour, now.minute, now.second)

                dt = datetime.datetime(response.target_year, response.target_month, response.target_day, response.target_hour, response.target_minute, response.target_second)
                time_left = (dt - now)

                print("\tTimer state:\t\tOn")
                print("\tTime left:\t\t" + str(time_left))
                if response.is_action_turn_on:
                    print("\tAction:\t\t\tTurn On")
                else:
                    print("\tAction:\t\t\tTurn Off")
            else:
                print("\tTimer state:\t\tOff")

            print("\tOriginal timer length:\t" + str(original_timer_length))
        if cmd == 'set_timer':
            sem6000.set_timer(False, sys.argv[4], sys.argv[5])
        if cmd == 'reset_timer':
            sem6000.set_timer(True, False, "00:00")
        if cmd == 'request_scheduler':
            response = sem6000.request_scheduler()

            print("Schedulers:")
            for i in range(len(response.schedulers)):
                scheduler = response.schedulers[i]

                print("\t#" + str(i+1))

                if scheduler.is_active:
                    print("\tActive:\tOn")
                else:
                    print("\tActive:\tOff")

                if scheduler.is_action_turn_on:
                    print("\tAction:\tTurn On")
                else:
                    print("\tAction:\tTurn Off")

                if scheduler.repeat_on_weekdays:
                    repeat_on_weekdays = ""
                    is_first_value = True
                    for weekday in scheduler.repeat_on_weekdays:
                        if not is_first_value:
                            repeat_on_weekdays += ", "
                        repeat_on_weekdays += weekday.name
                        is_first_value = False

                    print("\tRepeat on:\t" + repeat_on_weekdays)
                else:
                    date = datetime.date(year=scheduler.year, month=scheduler.month, day=scheduler.day)
                    print("\tDate:\t" + str(date))

                print("\tTime:\t" + _format_hour_and_minute_as_time(scheduler.hour, scheduler.minute))
                print("")

