import ldap
import logging

import api.config.config as config
from api.models.users import UserType, LdapUserInfo


class LdapAuth:
    """A class to authenticate users against an LDAP server.

    :param app: The Flask app instance
    :type app: Flask
    """

    logger = logging.getLogger(__name__)

    def __init__(self):
        ldap.set_option(ldap.OPT_REFERRALS, 0)
        ldap.protocol_version = 3

        try:
            self.conn = ldap.initialize(config.LDAP_URI)
            self.conn.simple_bind_s(config.LDAP_USERNAME, config.LDAP_PASSWORD)
            LdapAuth.logger.info(f"LDAP connection successful.")
        except Exception as e:
            LdapAuth.logger.error(f"Error connecting to LDAP: {e}")

    def check_creds(self, username, password, retry=3):
        """A function to check the credentials of a user against the LDAP server.

        :param username: The username to check.
        :type username: str
        :param password: The password to check.
        :type password: str

        :return: True if the credentials are correct, False otherwise
        :rtype: bool
        """
        if self.conn is None:
            LdapAuth.logger.error(
                f"Error checking LDAP credentials: LDAP connection is not initialized"
            )
            raise Exception("Error checking LDAP credentials")

        try:
            temp_conn = ldap.initialize(config.LDAP_URI)
            temp_conn.simple_bind_s(f"{username}@{config.LDAP_DOMAIN}", password)
        except Exception as e:
            LdapAuth.logger.error(f"Failed to LDAP authenticate {username}: {e}")
            return None

        try:
            res = self.conn.search_s(
                config.LDAP_DN, ldap.SCOPE_SUBTREE, "(objectClass=User)"
            )
            for dn, entry in res:
                name = entry["userPrincipalName"][0].decode("ASCII").split("@")[0]
                if name == username:
                    LdapAuth.logger.info(f"Authenticated user {username} with LDAP")

                    display_name = entry["cn"][0].decode("ASCII")

                    if (
                        b"CN=Users - Global Admins,OU=Groups,OU=All Users,DC=CTULABS,DC=local"
                        in entry["memberOf"]
                    ):
                        usertype = UserType.ADMIN
                    elif (
                        b"CN=Users - Staff Access,OU=Groups,OU=All Users,DC=CTULABS,DC=local"
                        in entry["memberOf"]
                    ):
                        usertype = UserType.STAFF
                    elif (
                        b"CN=Users - Student Access,OU=Groups,OU=All Users,DC=CTULABS,DC=local"
                        in entry["memberOf"]
                    ):
                        usertype = UserType.STUDENT

                    return LdapUserInfo(
                        username=username, display_name=display_name, usertype=usertype
                    )

            raise Exception("User not found in DN")
        except Exception as e:
            LdapAuth.logger.error(f"Error checking LDAP credentials: {e}")

            if retry > 0:
                LdapAuth.logger.info("Attempting to reconnect to LDAP.")
                self.conn = ldap.initialize(config.LDAP_URI)
                self.conn.simple_bind_s(config.LDAP_USERNAME, config.LDAP_PASSWORD)
                return self.check_creds(username, password, retry=retry - 1)

    def get_display_name(self, username, retry=3) -> str:
        """A function to get the display name of a user from LDAP.

        :param username: The username to get the display name for.
        :type username: str

        :return: The display name of the user.
        :rtype: str
        """
        if self.conn is None:
            LdapAuth.logger.error(
                f"Error getting display name for user: LDAP connection is not initialized"
            )
            return False

        try:
            res = self.conn.search_s(
                self.app.config["LDAP_DN"], ldap.SCOPE_SUBTREE, "(objectClass=User)"
            )
            for dn, entry in res:
                name = entry["userPrincipalName"][0].decode("ASCII").split("@")[0]
                if name == username:
                    return entry["cn"][0].decode("ASCII")
            return username
        except Exception as e:
            LdapAuth.logger.error(f"Error getting display name for user: {e}")
            if retry > 0:
                LdapAuth.logger.info("Attempting to reconnect to LDAP.")
                self.conn = ldap.initialize(self.app.config["LDAP_URI"])
                self.conn.simple_bind_s(
                    self.app.config["LDAP_USER"], self.app.config["LDAP_PASS"]
                )
                return self.get_display_name(username, retry=retry - 1)

            return username


LDAP = LdapAuth()
