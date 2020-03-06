# Web Key Directory (WKD) for Netlify

1. Fork this repo
2. Export your public key and make sure the filename is your email address with ``pgp`` file ending:  
   ``gpg --export-options export-minimal --export dominik@cotech.de > dominik@cotech.de.pgp``
3. Add the exported key file(s) to your fork.
4. Edit the ``Makefile`` and change ``example.com`` to your domain.
5. Deploy your repo to Netlify: [![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/cotechde/netlify-wkd)
6. Add the ``openpgpkey`` subdomain to Netlify's domain management, such as ``openpgpkey.example.com``, and point your DNS to it.
7. Enable TLS using Let's Encrypt in Netlify's domain management

# Verify

https://metacode.biz/openpgp/web-key-directory can be used to verify that the advanced lookup method works.
