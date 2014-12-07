plugindir = /usr/share/enigma2/$(PLUGIN)

LANGS = ar bg ca cs da de el en en_GB es et fa fi fr fy he hr hu is it lt lv nl no nb pl pt pt_BR ro ru sv sk sl sr th tr uk
LANGMO = $(LANGS:=.mo)
LANGPO = $(LANGS:=.po)

# the TRANSLATORS: allows putting translation comments before the to-be-translated line.
$(PLUGIN)-py.pot: $(srcdir)/../src/*.py
	$(XGETTEXT) --no-wrap -L python --from-code=UTF-8 --add-comments="TRANSLATORS:" -d $(PLUGIN) -s -o $@ $^

$(PLUGIN)-xml.pot: $(top_srcdir)/xml2po.py $(srcdir)/../src/*.xml
	$(PYTHON) $^ > $@

$(PLUGIN).pot: $(PLUGIN)-py.pot $(PLUGIN)-xml.pot
	sed --in-place $(PLUGIN)-py.pot --expression=s/CHARSET/UTF-8/
	sed --in-place $(PLUGIN)-xml.pot --expression=s/CHARSET/UTF-8/
	cat $^ | $(MSGUNIQ) --no-wrap --no-location -o $@

%.po: $(PLUGIN).pot
	if [ -f $@ ]; then \
		$(MSGMERGE) --backup=none --no-wrap --no-location -s -N -U $@ $< && touch $@; \
	else \
		$(MSGINIT) -l $@ -o $@ -i $< --no-translator; \
	fi

.po.mo:
	$(MSGFMT) -o $@ $<

BUILT_SOURCES = $(LANGMO)
CLEANFILES = $(LANGMO) $(PLUGIN)-py.pot $(PLUGIN)-xml.pot $(PLUGIN).pot

dist-hook: $(LANGPO)

install-data-local: $(LANGMO)
	for lang in $(LANGS); do \
		$(mkinstalldirs) $(DESTDIR)$(plugindir)/po/$$lang/LC_MESSAGES; \
		$(INSTALL_DATA) $$lang.mo $(DESTDIR)$(plugindir)/po/$$lang/LC_MESSAGES/$(PLUGIN).mo; \
		$(INSTALL_DATA) $$lang.po $(DESTDIR)$(plugindir)/po/$$lang.po; \
	done

uninstall-local:
	for lang in $(LANGS); do \
		$(RM) $(DESTDIR)$(plugindir)/po/$$lang/LC_MESSAGES/$(PLUGIN).mo; \
	done
