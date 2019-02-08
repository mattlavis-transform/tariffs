REM get cookies
REM https://signon-dev.cloudapps.digital/users/sign_in

wget -qO- --no-check-certificate --keep-session-cookies --save-cookies cookies.txt --post-data "user_email=matt.lavis@digital.trade.gov.uk&user_password=Lorem ipsum" https://signon-dev.cloudapps.digital/users/sign_in