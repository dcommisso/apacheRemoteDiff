apacheRemoteDiff
===============

Tool per controllare se i file di configurazione di due Apache in cluster sono allineati.

Puo' confrontare qualsiasi file ma e' ottimizzato per Apache: ignora le linee vuote, l'identazione, i
commenti, le tabulazioni, gli spazi multipli, gli spazi alla fine della riga, le occorrenze degli indirizzi IP del server e le occorrenze dell'hostname (per escludere le differenze nei nomi dei log, ad esempio). Perché l'hostname possa essere escluso correttamente, e' necessario che il tool venga lanciato con i nomi macchina anziche' gli indirizzi IP. I file confrontati, se non esplicitamente specificato, sono: /etc/httpd/conf/httpd.conf,
etc/httpd/conf.d/ssl.conf, /etc/httpd/conf.d/workers.properties.