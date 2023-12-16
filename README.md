# Domain Factory Webmail Admin Scraper

Dieses Stück Software loggt sich bei Domain Facatory ein und leist alle E-Mail Addressen aus und speichert sie in einer JSON Datei.

## Installation

Benötigt: Python beim Autor läuft Version 3.11.2

```bash
# Pyenv aufsetzen
./install.sh
```

Config Datei erstellen mit Namen config.yml (siehe config.yml.example), hier muss das Passwort für den Admin Zugang von Domain Factory eingetragen werden.


## Aufruf

Bitte beachte, dass wir keinerlei Gewähr für gar nichts übernehmen. Also schau dir den Code an, ob wir das Admin Passwort auf Mattermost Posten!
Rufe ihn nur auf wenn du ihn verstehst oder wenn du die Welt brennen sehen willst.


```bash
./myvenv/bin/python ./domain-factory-webscraper.py
```

## Ergebnis

Eine JSON Datei, hier ein Beispiel:

```json
[
  {
    "email": "cloud@example.com",
    "alt_email": null,
    "autoresponder": false,
    "mailfilter": false,
    "forwarder": true,
    "mailbox": false,
    "size_in_mb": null,
    "url": "https://admin.df.eu/kunde/email.php?action=edit&dn=....",
    "fwd_destinations": [
      "my.name@example.com"
    ]
  }
]
```

## Experimentell (eigentlich ist alles Experimentell): Passwort setzen

In der main Methode der Datei: domain-factory-webscraper.py
kann der folgende Code:

```python
    for mail_user in mail_users:
        if mail_user['email']=='FIXME' and mail_user['mailbox']:
            reset_password(driver,mail_user['url'], conf['new_password'])
```

angepasst werden um für einzelen oder alle Accounts das Passwort neu zu setzen.
Das kannn dann z.B. für eine Migration mit ImapSync (siehe: https://imapsync.lamiral.info/ ) genutzt werden.

# Fragen? Anregungen?

Bitte benutze Github Issues:
 https://github.com/ADFC-Hamburg/domain-factory-mail-scraper/issues/new

Code Änderungen gerne als Merge-Request.
