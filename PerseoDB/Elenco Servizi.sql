SELECT b.AnnoBando, tb.TipoBando, sedi.SiglaSede, serv.DescrEdizione, serv.CodiceEdizione,
       ed.OreAttivita, ie.OreAssegnate, iec.QuotaOraIncarico
  FROM [CSF].[dbo].[t_AttivitaEdizioni] AS ed
  LEFT JOIN [CSF].[dbo].[t_PianoServizi] AS serv ON serv.IDedizione = ed.FK_Edizione
  LEFT JOIN [CSF].[dbo].[t_Sedi] AS sedi ON sedi.IDsede = serv.FK_SedeEdizione
  LEFT JOIN [CSF].[dbo].[t_Azioni] AS az ON az.IDazione = serv.FK_Azione
  LEFT JOIN [CSF].[dbo].[t_Progetti] AS pr ON pr.IDprogetto = az.FK_Progetto
  LEFT JOIN [CSF].[dbo].[t_bandi] AS b ON b.IDbando = pr.FK_Bando
  LEFT JOIN [CSF].[dbo].[t_TipoBando] AS tb ON tb.IDtbando = b.FK_TipoBando
  LEFT JOIN [CSF].[dbo].[t_IncarichiEdizioni] AS ie ON ie.FK_Attivita = ed.IDattedi
  LEFT JOIN [CSF].[dbo].[t_IncarichiEdizioniContratti] AS iec ON iec.FK_IncaricoEdizione = ie.IDincarico
  WHERE b.AnnoBando = '2020/2021'
