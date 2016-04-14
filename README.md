apacheRemoteDiff
===============

Tool per controllare se i file di configurazione di due Apache in cluster sono allineati.

Può confrontare qualsiasi file ma e' ottimizzato per Apache: ignora le linee vuote, l'identazione, i
commenti, le tabulazioni, gli spazi multipli, gli spazi alla fine della riga e le occorrenze degli indirizzi IP del
server. I file confrontati, se non esplicitamente specificato, sono: /etc/httpd/conf/httpd.conf,
etc/httpd/conf.d/ssl.conf, /etc/httpd/conf.d/workers.properties.