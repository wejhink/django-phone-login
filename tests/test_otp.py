# Here is where we check the Creation and Generation of OTP.
#
# Creating and Validating OTP
# 1. Success - When phone_number, otp are given and timestamp is within PHONE_LOGIN_OTP_LENGTH limit or 6.
# 2. Failure - When phone_number is not given or class isn't defined
# 3. Failure - When attempts are more more than PHONE_LOGIN_ATTEMPTS or 10.
# 4. Failure - When time range is greater than PHONE_LOGIN_OTP_LENGTH.
# 5. Failure - When OTP is not given.
