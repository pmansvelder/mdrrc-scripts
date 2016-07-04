#!/bin/bash
# Installs translation files for dutch

xgettext locgrid.py
cp messages.po mdrrc-editor.pot
msgfmt mdrrc-editor.pot
sudo mv messages.mo /usr/share/locale/nl/LC_MESSAGES/mdrrc-editor.mo
