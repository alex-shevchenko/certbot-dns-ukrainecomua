#[Ukraine.com.ua](https://ukraine.com.ua) DNS Authenticator plugin for Certbot

The `certbot-dns-ukrainecomua` plugin automates the process of
completing a `dns-01` challenge by creating, and
subsequently removing, TXT records using the [Ukraine.com.ua](https://ukraine.com.ua) API.

##Named Arguments

Argument | Description
---------------------------------| -----------------
`--dns-ukrainecomua-credentials` | Ukraine.com.ua credentials_ INI file. (Required)
`--dns-ukrainecomua-propagation-seconds` | The number of seconds to wait for DNS to propagate before asking the ACME server to verify the DNS record. (Default: 180)


##Credentials

Use of this plugin requires a configuration file containing Ukraine.com.ua API
credentials, obtained at https://adm.tools/user/api/

```ini
# Example ini file
dns_ukrainecomua_token = MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAw
```

The path to this file can be provided interactively or using the
`--dns-ukrainecomua-credentials` command-line argument. Certbot records the path
to this file for use during renewal, but does not store the file's contents.

__CAUTION__ You should protect these API credentials as you would the password to your
DNSimple account. Users who can read this file can use these credentials
to issue arbitrary API calls on your behalf. Users who can cause Certbot to
run using these credentials can complete a `dns-01` challenge to acquire
new certificates or revoke existing certificates for associated domains,
even if those domains aren't being managed by this server.

Certbot will emit a warning if it detects that the credentials file can be
accessed by other users on your system. The warning reads "Unsafe permissions
on credentials configuration file", followed by the path to the credentials
file. This warning will be emitted each time Certbot uses the credentials file,
including for renewal, and cannot be silenced except by addressing the issue
(e.g., by using a command like ``chmod 600`` to restrict access to the file).


Examples
--------

```bash
#To acquire a certificate for example.com

certbot certonly \\
 --dns-ukrainecomua \\
 --dns-ukrainecomua-credentials ~/.secrets/certbot/ukrainecomua.ini \\
 -d example.com

#To acquire a single certificate for both example.com and www.example.com

certbot certonly \\
 --dns-ukrainecomua \\
 --dns-ukrainecomua-credentials ~/.secrets/certbot/ukrainecomua.ini \\
 -d example.com \\
 -d www.example.com

# To acquire a certificate for ``example.com``, waiting 60 seconds for DNS propagation

certbot certonly \\
 --dns-ukrainecomua \\
 --dns-ukrainecomua-credentials ~/.secrets/certbot/ukrainecomua.ini \\
 --dns-ukrainecomua-propagation-seconds 60 \\
 -d example.com
