SELECT AnnoBando, SiglaSede,
    CodiceEdizione, DescrEdizione,
    CodiceProgetto, DescrProgetto, 
    Cognome, Nome, CodFiscale, 
    (DataIscr) AS DataIscrizione, DataRitiro, Disabile, (Svantaggio) AS DSA
FROM t_TipoDoteStudente
RIGHT OUTER JOIN t_StudentiDoti ON t_TipoDoteStudente.IDtdote = t_StudentiDoti.FK_TipoDote
RIGHT OUTER JOIN t_Utenti
INNER JOIN t_Iscrizioni ON t_Utenti.IDutente = t_Iscrizioni.FK_Utente
INNER JOIN t_TipoNazionalita ON t_Utenti.FK_Nazionalita = t_TipoNazionalita.IDtnaz
INNER JOIN t_PianoServizi ON t_Iscrizioni.FK_Edizione = t_PianoServizi.IDedizione
INNER JOIN t_TipoFormativoInterno ON t_PianoServizi.FK_TipoFormativoInterno = t_TipoFormativoInterno.IDtformaint
INNER JOIN t_Sedi ON t_PianoServizi.FK_SedeEdizione = t_Sedi.IDsede
INNER JOIN t_Azioni ON t_PianoServizi.FK_Azione = t_Azioni.IDazione
INNER JOIN t_Progetti ON t_Azioni.FK_Progetto = t_Progetti.IDprogetto
INNER JOIN t_Bandi ON t_Progetti.FK_Bando = t_Bandi.IDbando
LEFT OUTER JOIN t_TipoSettoreInterno ON t_PianoServizi.FK_SettoreEdizione = t_TipoSettoreInterno.IDtsettin
LEFT OUTER JOIN t_TipoAnnualita ON t_PianoServizi.FK_Anno = t_TipoAnnualita.IDtanno
LEFT OUTER JOIN t_TipoMotivoRitiro ON t_Iscrizioni.FK_MotivoRitiro = t_TipoMotivoRitiro.IDtritiro
LEFT OUTER JOIN t_TipoStatoLav ON t_Utenti.FK_StatoLav = t_TipoStatoLav.IDtslav ON t_StudentiDoti.IDdotestud = t_Iscrizioni.FK_DoteStudente 
WHERE AnnoBando = '2020/2021'
AND SedeTest=0
ORDER BY Cognome, Nome, SiglaSede, TipoFormativoInterno, TipoAnnualita, Gruppo, DescrEdizione 