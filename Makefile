.PHONY: po mo


po:
	xgettext -Lpython --output=messages.pot main.py libs/baseclass/settings_screen.py libs/kv/settings_screen.kv libs/kv/about.kv libs/kv/impexp.kv libs/kv/root_screen.kv libs/kv/impexp_screen.kv libs/baseclass/kassa_screen.py libs/kv/kassa_screen.kv libs/baseclass/asetting_screen.py libs/kv/asetting_screen.kv libs/baseclass/fr_widget.py libs/baseclass/buttonlib.py libs/baseclass/eqsetting_screen.py libs/kv/eqsetting_screen.kv libs/applibs/eq.py
	msgmerge --update --no-fuzzy-matching --backup=off data/locales/po/ru.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off data/locales/po/en.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off data/locales/po/es.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off data/locales/po/de.po messages.pot

mo:
	mkdir -p data/locales/ru/LC_MESSAGES
	mkdir -p data/locales/en/LC_MESSAGES
	mkdir -p data/locales/es/LC_MESSAGES
	mkdir -p data/locales/de/LC_MESSAGES
	msgfmt -c -o data/locales/ru/LC_MESSAGES/ecopos.mo data/locales/po/ru.po
	msgfmt -c -o data/locales/en/LC_MESSAGES/ecopos.mo data/locales/po/en.po
	msgfmt -c -o data/locales/es/LC_MESSAGES/ecopos.mo data/locales/po/es.po
	msgfmt -c -o data/locales/de/LC_MESSAGES/ecopos.mo data/locales/po/de.po
