SELECT (t_DocentiParcelle.IDparcella) AS Parcella,
    (CASE WHEN IDazienda IS NOT NULL THEN DescrAzienda ELSE (Cognome + ' ' + Nome) END) AS Collaboratore,
    DescrProgetto,
    CodiceProgetto,
    CodiceCIG,
    CodiceCUP,
    DescrEdizione,
    CodiceEdizione,
    SiglaSede,
    (CASE WHEN IDcomponente IS NOT NULL THEN ('Sì') ELSE NULL END) AS CommissioneEsame,
    DataRiunionePreliminare,
    DescrCostiAggiuntivi,
    DescrParcella,
    TipoCausaleParcella,
    DescrParFiscale,
    CodiceTributo,
    DescrAmmNomina,
    DescrDatoreLavoro,
    DataParcella,
    DataPagamento,
    ImportoParcella,
    sngRiva,
    sngCassaPrev,
    sngIVA,
    (CostiAnticipo+CostiVitto+CostiViaggio) AS Costi,
    sngINPS,
    sngINPS23,
    sngTotale,
    sngINPS13,
    sngRiteAcc,
    sngNettoInc,
    NumeroFattura,
    DataFattura

FROM t_Progetti
RIGHT OUTER JOIN t_DocentiParcelle
INNER JOIN t_TipoCausaleParcella ON t_DocentiParcelle.FK_Causale = t_TipoCausaleParcella.IDtcausaparce
LEFT OUTER JOIN t_CommissioniEsameComponenti ON t_DocentiParcelle.FK_Commissione = t_CommissioniEsameComponenti.IDcomponente
LEFT OUTER JOIN t_CommissioniEsame ON t_CommissioniEsameComponenti.FK_Commissione = t_CommissioniEsame.IDcommissione
LEFT OUTER JOIN t_Docenti ON t_DocentiParcelle.FK_Docente = t_Docenti.IDdocente
LEFT OUTER JOIN t_DecodificatoreParametroFiscale ON t_DocentiParcelle.FK_PF = t_DecodificatoreParametroFiscale.IDparfisc
LEFT OUTER JOIN t_Sedi ON t_DocentiParcelle.FK_Sede = t_Sedi.IDsede ON t_Progetti.IDprogetto = t_DocentiParcelle.FK_Progetto
LEFT OUTER JOIN t_Azioni ON t_DocentiParcelle.FK_Azione = t_Azioni.IDazione
LEFT OUTER JOIN t_PianoServizi ON t_DocentiParcelle.FK_Edizione = t_PianoServizi.IDedizione
LEFT OUTER JOIN t_Aziende ON t_DocentiParcelle.FK_Azienda = t_Aziende.IDazienda

WHERE DataPagamento IS NOT NULL

ORDER BY (CASE WHEN FK_Azienda IS NOT NULL THEN DescrAzienda ELSE (Cognome + ' ' + Nome) END), DataPagamento 