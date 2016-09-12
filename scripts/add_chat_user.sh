#!/bin/bash
set -e
USERNAME=$1

if [ -f /var/lib/prosody/${XMPP_DOMAIN_NAME}%2elocal/accounts/${USERNAME}.dat ]
    then
    exit 1
fi


prosodyctl register ${USERNAME} ${XMPP_DOMAIN_NAME}.local ${XMPP_DEFAULT_PASS} > /system-manager/system-manager.log


cd /var/lib/prosody/${XMPP_DOMAIN_NAME}%2elocal/


if [ ! -d roster ]
    then
    mkdir roster
fi

cd roster
if [ ! -f ${XMPP_HOST}.dat ]; then
    touch ${XMPP_HOST}.dat
    printf "return {
        [false] = {
		    [\"version\"] = 3;
	    };
	};" > ${XMPP_HOST}.dat
    touch ${USERNAME}.dat
    printf "return {
        [false] = {
                    [\"version\"] = 3;
        	};
	};" > ${USERNAME}.dat
else
	touch ${USERNAME}.dat
    printf "return {
        [false] = {
		    [\"version\"] = 3;
	    };
	};" > ${USERNAME}.dat
fi

sed -i "$ d" ${XMPP_HOST}.dat
sed -i "$ d" ${USERNAME}.dat

printf "\t[\""${USERNAME}@${XMPP_DOMAIN_NAME}.local"\"] = {\n\t\t\t[\"subscription\"] = \"to\";\n\t\t\t[\"groups\"] = {};\n\t};\n};" >> ${XMPP_HOST}.dat
printf "\t[\""${XMPP_HOST}@${XMPP_DOMAIN_NAME}.local"\"] = {\n\t\t\t[\"subscription\"] = \"from\";\n\t\t\t[\"groups\"] = {};\n\t\t};\n};" >> ${USERNAME}.dat

