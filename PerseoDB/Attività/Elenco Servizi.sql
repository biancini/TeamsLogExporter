SELECT serv.IDedizione,
  b.AnnoBando,
  tb.TipoBando,
  form.TipoFormativoInterno,
  sedi.SiglaSede,
  serv.DescrEdizione,
  serv.CodiceEdizione,
  sett.TipoSettoreInt,
  pr.CodiceProgetto,
  pr.DescrProgetto,
  tp.TipoProgetto,
  b.CodiceBando,
  pr.DataAvvioProg,
  pr.DataFineProg,
  serv.Durata,
  (SELECT OreAttivita FROM t_AttivitaEdizioni WHERE FK_Edizione = serv.IDedizione AND FK_TipoAttivita = 1) AS OreAula,
  (SELECT OreAttivita FROM t_AttivitaEdizioni WHERE FK_Edizione = serv.IDedizione AND FK_TipoAttivita = 2) AS OreStage,
  (SELECT COUNT(IDiscrizione) FROM t_Iscrizioni WHERE FK_Edizione = serv.IDedizione) AS NIscr,
  (SELECT ROUND(SUM(ImportoTotaleDote), 2) FROM t_StudentiDoti AS doti LEFT JOIN t_Iscrizioni AS iscr ON iscr.FK_DoteStudente = doti.IDdotestud WHERE FK_Edizione = serv.IDedizione) AS ImportoDoti
  
FROM t_PianoServizi AS serv
  LEFT JOIN t_Sedi AS sedi ON sedi.IDsede = serv.FK_SedeEdizione
  LEFT JOIN t_Azioni AS az ON az.IDazione = serv.FK_Azione
  LEFT JOIN t_Progetti AS pr ON pr.IDprogetto = az.FK_Progetto
  LEFT JOIN t_TipoProgetto AS tp ON pr.FK_TipoProgetto = tp.IDtprogetto
  LEFT JOIN t_Bandi AS b ON b.IDbando = pr.FK_Bando
  LEFT JOIN t_TipoFormativoInterno AS form ON serv.FK_TipoFormativoInterno = form.IDtformaint
  LEFT JOIN t_TipoBando AS tb ON tb.IDtbando = b.FK_TipoBando
  LEFT JOIN t_TipoSettoreInterno AS sett ON serv.FK_SettoreEdizione = sett.IDtsettin

WHERE b.AnnoBando IN ('2019/2020', '2020/2021', '2021/2022')

ORDER BY IDazione
