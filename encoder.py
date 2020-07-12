from message import *

class MessageEncoder():
    def _encode_message(self, payload, suffix=b'\xff\xff'):
        message = b'\x0f'

        message += (len(payload)+1).to_bytes(1, 'big')
        message += payload

        message += ((1+sum(payload)) & 0xff).to_bytes(1, 'big')
        message += suffix

        return message

    def _encode_pin(self, pin):
            pin_bytes = b''
            for i in pin:
                pin_bytes += int(i).to_bytes(1, 'big')
            
            return pin_bytes

    def encode(self, message):
        if isinstance(message, AuthorizeCommand):
            encoded_pin = self._encode_pin(message.pin)
            return self._encode_message(b'\x17\x00\x00' + encoded_pin + b'\x00\x00\x00\x00')

        if isinstance(message, ChangePinCommand):
            encoded_pin = self._encode_pin(message.pin)
            encoded_new_pin = self._encode_pin(message.new_pin)
            return self._encode_message(b'\x17\x00\x01' + encoded_new_pin + encoded_pin)

        if isinstance(message, ResetPinCommand):
            return self._encode_message(b'\x17\x00\x02' + b'\x00\x00\x00\x00\x00\x00\x00\x00')

        if isinstance(message, PowerSwitchCommand):
            if message.on:
                return self._encode_message(b'\x03\x00\x01' + b'\x00\x00')
            else:
                return self._encode_message(b'\x03\x00\x00' + b'\x00\x00')

        if isinstance(message, LEDSwitchCommand):
            if message.on:
                return self._encode_message(b'\x0f\x00\x05\x01' + b'\x00\x00\x00\x00')
            else:
                return self._encode_message(b'\x0f\x00\x05\x00' + b'\x00\x00\x00\x00')

        if isinstance(message, SynchronizeDateAndTimeCommand):
            encoded_year = message.year.to_bytes(2, 'big')
            encoded_month = message.month.to_bytes(1, 'big')
            encoded_day = message.day.to_bytes(1, 'big')

            encoded_hour = message.hour.to_bytes(1, 'big')
            encoded_minute = message.minute.to_bytes(1, 'big')
            encoded_second = message.second.to_bytes(1, 'big')

            return self._encode_message(b'\x01\x00' + encoded_second + encoded_minute + encoded_hour + encoded_day + encoded_month + encoded_year + b'\x00\x00')

        if isinstance(message, AuthorizationNotification):
            was_successful = b'\x01'
            if message.was_successful:
                was_successful = b'\x00'

            return self._encode_message(b'\x17\x00' + was_successful + b'\x00\x00')

        if isinstance(message, ChangePinNotification):
            was_successful = b'\x01'
            if message.was_successful:
                was_successful = b'\x00'

            return self._encode_message(b'\x17\x00' + was_successful + b'\x01\x00')

        if isinstance(message, ResetPinNotification):
            was_successful = b'\x01'
            if message.was_successful:
                was_successful = b'\x00'

            return self._encode_message(b'\x17\x00' + was_successful + b'\x02\x00')

        if isinstance(message, PowerSwitchNotification):
            was_successful = b'\x01'
            if message.was_successful:
                was_successful = b'\x00'

            return self._encode_message(b'\x03\x00' + was_successful)

        if isinstance(message, LEDSwitchNotification):
            return self._encode_message(b'\x0f\x00' + b'\x05\x00')

        if isinstance(message, SynchronizeDateAndTimeNotification):
            was_successful = b'\x01'
            if message.was_successful:
                was_successful = b'\x00'

            return self._encode_message(b'\x01\x00' + was_successful)


        raise Exception('Unsupported message ' + str(message))
