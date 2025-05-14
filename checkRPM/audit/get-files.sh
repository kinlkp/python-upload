
IFS=$'\n'
xxx="cat /etc/shadow
logins –axo
cat /etc/login.defs
cat /etc/pam.d/system-auth
cat /etc/pamd.conf
cat /etc/hosts.equiv
cat .rhosts
cat /etc/passwd
cat /etc/group
cat /var/log/secure
cat /etc/sudoers"

for w in ${xxx[@]}
do
echo "<p>${w}</p>"
echo "<pre>"
eval $w
echo "</pre>"
done
