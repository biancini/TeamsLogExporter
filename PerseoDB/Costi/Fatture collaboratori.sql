SELECT compensi.IDcompensi,
    (CASE WHEN MONTH(serv.DataAvvio)>=9 THEN (CAST(YEAR(serv.DataAvvio) AS VARCHAR) + '/' + CAST(YEAR(serv.DataAvvio) + 1 AS VARCHAR)) ELSE (CAST(YEAR(serv.DataAvvio) - 1 AS VARCHAR) + '/' + CAST(YEAR(serv.DataAvvio) AS VARCHAR)) END) AS AnnoAmm,
    compensi.IDincarico,
    docenti.IDdocente,
    compensi.FK_Azienda,
    serv.IDedizione,
    sedi.SiglaSede,
    (CASE WHEN compensi.FK_Azienda IS NULL THEN (docenti.Cognome + ' ' + docenti.Nome) ELSE aziende.DescrAzienda END) AS Prestatore,
    (CASE WHEN compensi.FK_Azienda IS NULL THEN docenti.CodFiscale ELSE (CASE WHEN aziende.PIVA IS NOT NULL THEN aziende.PIVA ELSE aziende.CodFiscale END) END) AS CF_PIVA,
    progetti.IDprogetto,
    progetti.DescrProgetto,
    progetti.CodiceProgetto,
    tp.TipoProgetto,
    form.TipoFormativoInterno,
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
INNER JOIN t_PianoServizi AS serv ON serv.IDedizione = compensi.IDedizione
INNER JOIN t_TipoFormativoInterno AS form ON form.IDtformaint = serv.FK_TipoFormativoInterno
INNER JOIN t_Progetti AS progetti ON pagamenti.FK_Progetto = progetti.IDprogetto
INNER JOIN t_TipoProgetto AS tp ON progetti.FK_TipoProgetto = tp.IDtprogetto
LEFT OUTER JOIN t_Docenti AS docenti ON compensi.IDdocente = docenti.IDdocente
LEFT OUTER JOIN t_Aziende AS aziende ON compensi.FK_Azienda = aziende.IDazienda
LEFT OUTER JOIN t_Sedi AS sedi ON compensi.FK_SedeEdizione = sedi.IDsede

WHERE compensi.Reso = 0
AND (CASE WHEN MONTH(serv.DataAvvio)>=9 THEN (CAST(YEAR(serv.DataAvvio) AS VARCHAR) + '/' + CAST(YEAR(serv.DataAvvio) + 1 AS VARCHAR)) ELSE (CAST(YEAR(serv.DataAvvio) - 1 AS VARCHAR) + '/' + CAST(YEAR(serv.DataAvvio) AS VARCHAR)) END) IN ('2018/2019', '2019/2020', '2020/2021', '2021/2022')

ORDER BY compensi.DataPagamento