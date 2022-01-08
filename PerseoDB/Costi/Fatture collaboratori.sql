SELECT compensi.IDcompensi,
    (CASE WHEN MONTH(compensi.DataPagatoFine)>=9 THEN (CAST(YEAR(compensi.DataPagatoFine) AS VARCHAR) + '/' + CAST(YEAR(compensi.DataPagatoFine) + 1 AS VARCHAR)) ELSE (CAST(YEAR(compensi.DataPagatoFine) - 1 AS VARCHAR) + '/' + CAST(YEAR(compensi.DataPagatoFine) AS VARCHAR)) END) AS AnnoAmm,
    compensi.IDincarico,
    docenti.IDdocente,
    compensi.FK_Azienda,
    compensi.IDedizione,
    sedi.SiglaSede,
    (CASE WHEN compensi.FK_Azienda IS NULL THEN (docenti.Cognome + ' ' + docenti.Nome) ELSE aziende.DescrAzienda END) AS Prestatore,
    (CASE WHEN compensi.FK_Azienda IS NULL THEN docenti.CodFiscale ELSE (CASE WHEN aziende.PIVA IS NOT NULL THEN aziende.PIVA ELSE aziende.CodFiscale END) END) AS CF_PIVA,
    progetti.IDprogetto,
    progetti.DescrProgetto,
    progetti.CodiceProgetto,
    tp.TipoProgetto,
    --(SELECT TipoFormativoInterno FROM t_TipoFormativoInterno LEFT JOIN t_PianoServizi ON t_TipoFormativoInterno.IDtformaint = t_PianoServizi.FK_TipoFormativoInterno LEFT JOIN t_Azioni ON t_Azioni.IDazione = t_PianoServizi.FK_Azione LEFT JOIN t_Progetti ON t_Progetti.IDprogetto = t_Azioni.FK_Progetto WHERE t_Progetti.IDprogetto = progetti.IDprogetto) AS TipoFormativoInterno,
    compensi.DescrEdizione,
    compensi.CodiceEdizione,
    compensi.TipoAttivita,
    compensi.TotOreFatte,
    compensi.QuotaOraIncarico,
    compensi.sngCostoInc,
    compensi.sngCassaPrev,
    compensi.sngCostiAnticipo,
    compensi.sngCostiViaggio,
    compensi.sngCostiVitto,
    compensi.sngCostiAggiuntivi,
    compensi.sngIVA,
    compensi.sngNettoInc,
    compensi.sngTotale,
    compensi.DataPagatoInizio,
    compensi.DataPagatoFine,
    compensi.DataPagamento
    
    
FROM t_ProgettiPagamenti AS pagamenti
INNER JOIN t_ProgettiPagamentiCompensiOneri AS compensi ON pagamenti.IDprogpagamento = compensi.FK_ProgettoPagamento
INNER JOIN t_Progetti AS progetti ON pagamenti.FK_Progetto = progetti.IDprogetto
INNER JOIN t_TipoProgetto AS tp ON progetti.FK_TipoProgetto = tp.IDtprogetto
LEFT OUTER JOIN t_Docenti AS docenti ON compensi.IDdocente = docenti.IDdocente
LEFT OUTER JOIN t_Aziende AS aziende ON compensi.FK_Azienda = aziende.IDazienda
LEFT OUTER JOIN t_Sedi AS sedi ON compensi.FK_SedeEdizione = sedi.IDsede

WHERE compensi.Reso = 0
AND (CASE WHEN MONTH(compensi.DataPagatoFine)>=9 THEN (CAST(YEAR(compensi.DataPagatoFine) AS VARCHAR) + '/' + CAST(YEAR(compensi.DataPagatoFine) + 1 AS VARCHAR)) ELSE (CAST(YEAR(compensi.DataPagatoFine) - 1 AS VARCHAR) + '/' + CAST(YEAR(compensi.DataPagatoFine) AS VARCHAR)) END) IN ('2019/2020', '2020/2021', '2021/2022')

ORDER BY compensi.DataPagamento