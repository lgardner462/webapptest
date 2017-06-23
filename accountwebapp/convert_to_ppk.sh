#!/usr/bin/expect

# ./expect_script.sh <KEY_PATH> <PUTTY_KEY_PATH> <PASS>

set KEY_PATH [lindex $argv 0]
set PUTTY_KEY_PATH [lindex $argv 1]
set PASS [lindex $argv 2] 

# ORIGINAL KEY FILE: username_id_rsa
# CONVERTED PUTTY FILE: username_private.ppk
eval spawn puttygen $KEY_PATH -O private -o $PUTTY_KEY_PATH 

expect "key:"
send "$PASS\r"
interact
