SELECT t_ProgettiPagamentiCompensiOneri.IDcompensi,
    (CASE WHEN MONTH(DataPagatoFine)>=9 THEN (CAST(YEAR(DataPagatoFine) AS VARCHAR) + '/' + CAST(YEAR(DataPagatoFine) + 1 AS VARCHAR)) ELSE (CAST(YEAR(DataPagatoFine) - 1 AS VARCHAR) + '/' + CAST(YEAR(DataPagatoFine) AS VARCHAR)) END) AS AnnoAmm,
    IDincarico,
    t_Docenti.IDdocente,
    FK_Azienda,
    IDedizione,
    SiglaSede,
    t_ProgettiPagamentiCompensiOneri.FK_ParFiscaleAttuale,
    (CASE WHEN FK_Azienda IS NULL THEN (Cognome + ' ' + Nome) ELSE DescrAzienda END) AS Prestatore,
    (CASE WHEN FK_Azienda IS NULL THEN (CAPresidenza + ' ' + ComResidenza + ' (' + ProvResidenza + ') ' + IndirResidenza) ELSE NULL END) AS Residenza,
    (CASE WHEN FK_Azienda IS NULL THEN t_Docenti.CodFiscale ELSE (CASE WHEN t_Aziende.PIVA IS NOT NULL THEN t_Aziende.PIVA ELSE t_Aziende.CodFiscale END) END) AS CF_PIVA,
    CodiceParFiscale,
    t_ProgettiPagamentiCompensiOneri.DescrParFiscale,
    t_ProgettiPagamentiCompensiOneri.FK_AliquotaPrevSepa,
    CodiceTributo,
    DescrProgetto,
    CodiceProgetto,
    TipoProgetto,
    IDmwp,
    DescrEdizione,
    CodiceEdizione,
    TipoAttivita,
    TotOreFatte,
    QuotaOraIncarico,
    sngCostoInc,
    sngRiva,
    sngCassaPrev,
    sngCostiAnticipo,
    sngCostiViaggio,
    sngCostiVitto,
    sngCostiAggiuntivi,
    sngIVA,
    sngINPS,
    sngINPS23,
    sngTotale,
    sngINPS13,
    sngRiteAcc,
    sngNettoInc,
    DataPagatoInizio,
    DataPagatoFine,
    t_ProgettiPagamentiCompensiOneri.DataPagamento
    
FROM t_ProgettiPagamenti
INNER JOIN t_ProgettiPagamentiCompensiOneri ON t_ProgettiPagamenti.IDprogpagamento = t_ProgettiPagamentiCompensiOneri.FK_ProgettoPagamento
INNER JOIN t_Progetti ON t_ProgettiPagamenti.FK_Progetto = t_Progetti.IDprogetto
INNER JOIN t_TipoProgetto ON t_Progetti.FK_TipoProgetto = t_TipoProgetto.IDtprogetto
INNER JOIN t_DecodificatoreParametroFiscale ON t_ProgettiPagamentiCompensiOneri.FK_ParFiscaleAttuale = t_DecodificatoreParametroFiscale.IDparfisc
LEFT OUTER JOIN t_Docenti ON t_ProgettiPagamentiCompensiOneri.IDdocente = t_Docenti.IDdocente
LEFT OUTER JOIN t_Aziende ON t_ProgettiPagamentiCompensiOneri.FK_Azienda = t_Aziende.IDazienda
LEFT OUTER JOIN t_Sedi ON FK_SedeEdizione = t_Sedi.IDsede

WHERE Reso = 0
AND DataPagatoFine >= '01/01/2016'