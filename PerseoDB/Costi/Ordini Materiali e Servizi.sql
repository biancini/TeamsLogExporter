SELECT ordini.IDordine AS PKord,
    (SELECT COUNT(IDordprog) FROM t_RichiesteOrdiniProgetti WHERE FK_RichiestaOrdine=ordini.IDordine) AS NProg,
    sedi.SiglaSede,
    (CASE WHEN MONTH(ordini.DataRichiesta)>=9 THEN (CAST(YEAR(ordini.DataRichiesta) AS VARCHAR) + '/' + CAST(YEAR(ordini.DataRichiesta) + 1 AS VARCHAR)) ELSE (CAST(YEAR(ordini.DataRichiesta) - 1 AS VARCHAR) + '/' + CAST(YEAR(ordini.DataRichiesta) AS VARCHAR)) END) AS AnnoAmm,
    (CASE WHEN NumeroOrdLab=0 THEN CAST(NumeroRichiesta AS VARCHAR) ELSE (CAST(NumeroRichiesta AS VARCHAR) + '/Lab.' + CAST(NumeroOrdLab AS VARCHAR)) END) AS NOrd,
    ordini.DataRichiesta,
    ordini.DescrRichiedente,
    ordini.DescrOrdine,
    ordini.DescrCausale,
    ordini.DescrConsegna,
    ordini.NoteScadenzaPagamenti,
    tipordine.TipoOrdine,
    ts.TipoSpesa,
    ordini.DataAutorizzazione,
    ordini.NoteRespinto,
    (CASE WHEN (SELECT COUNT(IDordprog) FROM t_RichiesteOrdiniProgetti WHERE FK_RichiestaOrdine=ordini.IDordine)=1 THEN (SELECT CodiceCIG FROM t_RichiesteOrdiniProgetti INNER JOIN t_Progetti ON t_RichiesteOrdiniProgetti.FK_Progetto = t_Progetti.IDprogetto WHERE FK_RichiestaOrdine=ordini.IDordine) ELSE NULL END) AS ProgettoCIG,
    (CASE WHEN (SELECT COUNT(IDordprog) FROM t_RichiesteOrdiniProgetti WHERE FK_RichiestaOrdine=ordini.IDordine)=1 THEN (SELECT CodiceCUP FROM t_RichiesteOrdiniProgetti INNER JOIN t_Progetti ON t_RichiesteOrdiniProgetti.FK_Progetto = t_Progetti.IDprogetto WHERE FK_RichiestaOrdine=ordini.IDordine) ELSE NULL END) AS ProgettoCUP,
    (CASE WHEN ordini.Respinto=1 THEN 'non approvato' WHEN ordini.RespintoSCO=1 THEN 'non autorizzato' WHEN (ordini.AutorizzatoSCO=1 AND ordini.Autorizzato=1) THEN 'approvato' WHEN (ordini.AutorizzatoSCO=1 AND ordini.Autorizzato=0) THEN 'autorizzato' WHEN (ordini.RichiestaPronta=1 AND ordini.AutorizzatoSCO=0 AND ordini.Autorizzato=0) THEN 'richiesta' WHEN (ordini.RichiestaPronta=0 AND ordini.AutorizzatoSCO=0 AND ordini.Autorizzato=0 AND ordini.SospesoRevisionare=0) THEN 'preparazione' WHEN (ordini.RichiestaPronta=0 AND ordini.AutorizzatoSCO=0 AND ordini.Autorizzato=0 AND ordini.SospesoRevisionare=1) THEN 'sospeso' ELSE '???' END) AS Stato,
    (SELECT DescrAzienda FROM t_Aziende WHERE IDazienda=ordini.FK_Fornitore) AS DescrAzienda,
    (SELECT COUNT(IDrigaord) FROM t_RichiesteOrdiniRighe WHERE FK_RichiestaOrdine=ordini.IDordine) AS NumVoci,
    (SELECT SUM(CostoUnitario*QuantRiga) FROM t_RichiesteOrdiniRighe WHERE FK_RichiestaOrdine=ordini.IDordine) AS TotaleImponibile,
    (SELECT SUM(TotaleIMponibile) FROM t_RichiesteOrdiniFatture WHERE FK_ordine=ordini.IDordine) AS TotaleImponibileFatture,
    ordini.DataOrdineEvaso
    
FROM t_RichiesteOrdini AS ordini
INNER JOIN t_Sedi AS sedi ON ordini.FK_Sede = sedi.IDsede
INNER JOIN t_TipoSpesa AS ts ON ordini.FK_TipoOrdineSpesa = ts.IDtipospesa
INNER JOIN t_TipoOrdine AS tipordine ON ts.FK_TipoOrdine = tipordine.IDtordine

WHERE (CASE WHEN MONTH(ordini.DataRichiesta)>=9 THEN (CAST(YEAR(ordini.DataRichiesta) AS VARCHAR) + '/' + CAST(YEAR(ordini.DataRichiesta) + 1 AS VARCHAR)) ELSE (CAST(YEAR(ordini.DataRichiesta) - 1 AS VARCHAR) + '/' + CAST(YEAR(ordini.DataRichiesta) AS VARCHAR)) END) IN ('2019/2020', '2020/2021', '2021/2022')

ORDER BY ordini.DataOrdineEvaso