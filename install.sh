#!/bin/bash
# Installs translation files for dutch

xgettext -L python -f filelist -j mdrrc-editor.po
msgfmt messages.po
sudo mv messages.mo /usr/share/locale/nl/LC_MESSAGES/mdrrc-editor.mo
