SELECT (t_RichiesteOrdini.IDordine) AS PKord,
    (SELECT COUNT(IDordprog) FROM t_RichiesteOrdiniProgetti WHERE FK_RichiestaOrdine=IDordine) AS NProg,
    SiglaSede,
    (CASE WHEN MONTH(DataRichiesta)>=9 THEN (CAST(YEAR(DataRichiesta) AS VARCHAR) + '/' + CAST(YEAR(DataRichiesta) + 1 AS VARCHAR)) ELSE (CAST(YEAR(DataRichiesta) - 1 AS VARCHAR) + '/' + CAST(YEAR(DataRichiesta) AS VARCHAR)) END) AS AnnoAmm,
    (CASE WHEN NumeroOrdLab=0 THEN CAST(NumeroRichiesta AS VARCHAR) ELSE (CAST(NumeroRichiesta AS VARCHAR) + '/Lab.' + CAST(NumeroOrdLab AS VARCHAR)) END) AS NOrd,
    DataRichiesta,
    DescrRichiedente,
    DescrOrdine,
    DescrCausale,
    DescrConsegna,
    NoteScadenzaPagamenti,
    NoteSconto,
    Sconto,
    TipoOrdine,
    TipoSpesa,
    DataAutorizzazioneSCO,
    NoteRespintoSCO,
    DataAutorizzazione,
    NoteRespinto,
    TipoModoPagaOrdine,
    TipoTempiPagamento,
    (CASE WHEN (SELECT COUNT(IDordprog) FROM t_RichiesteOrdiniProgetti WHERE FK_RichiestaOrdine=IDordine)=1 THEN (SELECT CodiceCIG FROM t_RichiesteOrdiniProgetti INNER JOIN t_Progetti ON t_RichiesteOrdiniProgetti.FK_Progetto = t_Progetti.IDprogetto WHERE FK_RichiestaOrdine=IDordine) ELSE NULL END) AS ProgettoCIG,
    (CASE WHEN (SELECT COUNT(IDordprog) FROM t_RichiesteOrdiniProgetti WHERE FK_RichiestaOrdine=IDordine)=1 THEN (SELECT CodiceCUP FROM t_RichiesteOrdiniProgetti INNER JOIN t_Progetti ON t_RichiesteOrdiniProgetti.FK_Progetto = t_Progetti.IDprogetto WHERE FK_RichiestaOrdine=IDordine) ELSE NULL END) AS ProgettoCUP,
    (CASE WHEN Respinto=1 THEN 'non approvato' WHEN RespintoSCO=1 THEN 'non autorizzato' WHEN (AutorizzatoSCO=1 AND Autorizzato=1) THEN 'approvato' WHEN (AutorizzatoSCO=1 AND Autorizzato=0) THEN 'autorizzato' WHEN (RichiestaPronta=1 AND AutorizzatoSCO=0 AND Autorizzato=0) THEN 'richiesta' WHEN (RichiestaPronta=0 AND AutorizzatoSCO=0 AND Autorizzato=0 AND SospesoRevisionare=0) THEN 'preparazione' WHEN (RichiestaPronta=0 AND AutorizzatoSCO=0 AND Autorizzato=0 AND SospesoRevisionare=1) THEN 'sospeso' ELSE '???' END) AS Stato,
    (SELECT DescrAzienda FROM t_Aziende WHERE IDazienda=FK_Fornitore) AS DescrAzienda,
    (SELECT COUNT(IDrigaord) FROM t_RichiesteOrdiniRighe WHERE FK_RichiestaOrdine=IDordine) AS NumVoci,
    (SELECT SUM(CostoUnitario*QuantRiga) FROM t_RichiesteOrdiniRighe WHERE FK_RichiestaOrdine=IDordine) AS TotaleImponibile,
    (SELECT SUM(TotaleIMponibile) FROM t_RichiesteOrdiniFatture WHERE FK_ordine=IDordine) AS TotaleImponibileFatture,
    DataOrdineEvaso,
    (NULL) AS ProtocolloEvaso
FROM t_RichiesteOrdini
INNER JOIN t_Sedi ON t_RichiesteOrdini.FK_Sede = t_Sedi.IDsede
INNER JOIN t_TipoSpesa ON t_RichiesteOrdini.FK_TipoOrdineSpesa = t_TipoSpesa.IDtipospesa
INNER JOIN t_TipoOrdine ON t_TipoSpesa.FK_TipoOrdine = t_TipoOrdine.IDtordine
LEFT OUTER JOIN t_TipoModoPagamentoOrdine ON t_RichiesteOrdini.FK_ModoPagamento = t_TipoModoPagamentoOrdine.IDtmodopag
LEFT OUTER JOIN t_TipoTempiPagamentoOrdine ON t_RichiesteOrdini.FK_TempoPagamento = t_TipoTempiPagamentoOrdine.IDttempipag