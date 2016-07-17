# Installs translation files for dutch

xgettext -L python -f filelist -j mdrrc-editor.po
msgfmt messages.po
mkdir C:\Python27\share\locale\nl\LC_MESSAGES
move messages.mo C:\Python27\share\locale\nl\LC_MESSAGES\mdrrc-editor.mo
