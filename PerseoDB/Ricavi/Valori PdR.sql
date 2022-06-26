SELECT 
  (CASE WHEN MONTH(serv.DataAvvio)>=9 THEN (CAST(YEAR(serv.DataAvvio) AS VARCHAR) + '/' + CAST(YEAR(serv.DataAvvio) + 1 AS VARCHAR)) ELSE (CAST(YEAR(serv.DataAvvio) - 1 AS VARCHAR) + '/' + CAST(YEAR(serv.DataAvvio) AS VARCHAR)) END) AS AnnoAmm,
  form.TipoFormativoInterno,
  sedi.SiglaSede,
  serv.DescrEdizione,
  serv.CodiceEdizione,
  sett.TipoSettoreInt,
  tp.TipoProgetto,
  serv.Durata,
  (SELECT COUNT(IDiscrizione) FROM t_Iscrizioni WHERE FK_Edizione = serv.IDedizione AND DataRitiro IS NULL) AS NIscr,
  (SELECT COUNT(IDiscrizione) FROM t_Iscrizioni INNER JOIN t_Utenti ON t_Utenti.IDutente = t_Iscrizioni.FK_Utente WHERE FK_Edizione = serv.IDedizione AND Disabile = 1) AS NDisabili,
  (SELECT COUNT(ImportoTotaleDote) FROM t_StudentiDoti AS doti LEFT JOIN t_Iscrizioni AS iscr ON iscr.FK_DoteStudente = doti.IDdotestud WHERE FK_Edizione = serv.IDedizione AND ImportoTotaleDote > 0) AS NumeroDoti,
  (SELECT ROUND(SUM(ImportoTotaleDote), 2) FROM t_StudentiDoti AS doti LEFT JOIN t_Iscrizioni AS iscr ON iscr.FK_DoteStudente = doti.IDdotestud WHERE FK_Edizione = serv.IDedizione) AS ImportoDoti,
  (SELECT ROUND(SUM(Quota), 2) FROM t_IscrizioniVersamenti AS iv INNER JOIN t_Iscrizioni AS i ON iv.FK_Iscrizione = i.IDiscrizione WHERE FK_Edizione = serv.IDedizione) AS QuotaTotaleVersata,
  IDprogetto,
  BudgetProgetto

FROM t_PianoServizi AS serv
  LEFT JOIN t_Sedi AS sedi ON sedi.IDsede = serv.FK_SedeEdizione
  LEFT JOIN t_Azioni AS az ON az.IDazione = serv.FK_Azione
  LEFT JOIN t_Progetti AS pr ON pr.IDprogetto = az.FK_Progetto
  LEFT JOIN t_TipoProgetto AS tp ON pr.FK_TipoProgetto = tp.IDtprogetto
  LEFT JOIN t_Bandi AS b ON b.IDbando = pr.FK_Bando
  LEFT JOIN t_TipoFormativoInterno AS form ON serv.FK_TipoFormativoInterno = form.IDtformaint
  LEFT JOIN t_TipoSettoreInterno AS sett ON serv.FK_SettoreEdizione = sett.IDtsettin

WHERE (CASE WHEN MONTH(serv.DataAvvio)>=9 THEN (CAST(YEAR(serv.DataAvvio) AS VARCHAR) + '/' + CAST(YEAR(serv.DataAvvio) + 1 AS VARCHAR)) ELSE (CAST(YEAR(serv.DataAvvio) - 1 AS VARCHAR) + '/' + CAST(YEAR(serv.DataAvvio) AS VARCHAR)) END) IN ('2018/2019', '2019/2020', '2020/2021')
