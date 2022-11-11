SELECT 
    (CASE WHEN MONTH(serv.DataAvvio)>=9 THEN (CAST(YEAR(serv.DataAvvio) AS VARCHAR) + '/' + CAST(YEAR(serv.DataAvvio) + 1 AS VARCHAR)) ELSE (CAST(YEAR(serv.DataAvvio) - 1 AS VARCHAR) + '/' + CAST(YEAR(serv.DataAvvio) AS VARCHAR)) END) AS AnnoAmm,
    serv.IDedizione,
    sedi.SiglaSede,
    'Collaboratore' AS Tipo,
    (CASE WHEN compensi.FK_Azienda IS NULL THEN (docenti.Cognome + ' ' + docenti.Nome) ELSE aziende.DescrAzienda END) AS Collaboratore,
    (CASE WHEN compensi.FK_Azienda IS NULL THEN docenti.CodFiscale ELSE (CASE WHEN aziende.PIVA IS NOT NULL THEN aziende.PIVA ELSE aziende.CodFiscale END) END) AS CF_PIVA,
    tp.TipoProgetto,
    form.TipoFormativoInterno,
    compensi.TipoAttivita,
    compensi.TotOreFatte,
    compensi.sngTotale
    
FROM t_ProgettiPagamenti AS pagamenti
LEFT OUTER JOIN t_ProgettiPagamentiCompensiOneri AS compensi ON pagamenti.IDprogpagamento = compensi.FK_ProgettoPagamento
LEFT OUTER JOIN t_PianoServizi AS serv ON serv.IDedizione = compensi.IDedizione
LEFT OUTER JOIN t_TipoFormativoInterno AS form ON form.IDtformaint = serv.FK_TipoFormativoInterno
LEFT OUTER JOIN t_Progetti AS progetti ON pagamenti.FK_Progetto = progetti.IDprogetto
LEFT OUTER JOIN t_TipoProgetto AS tp ON progetti.FK_TipoProgetto = tp.IDtprogetto
LEFT OUTER JOIN t_Docenti AS docenti ON compensi.IDdocente = docenti.IDdocente
LEFT OUTER JOIN t_Aziende AS aziende ON compensi.FK_Azienda = aziende.IDazienda
LEFT OUTER JOIN t_Sedi AS sedi ON compensi.FK_SedeEdizione = sedi.IDsede

WHERE compensi.Reso = 0
AND (CASE WHEN MONTH(serv.DataAvvio)>=9 THEN (CAST(YEAR(serv.DataAvvio) AS VARCHAR) + '/' + CAST(YEAR(serv.DataAvvio) + 1 AS VARCHAR)) ELSE (CAST(YEAR(serv.DataAvvio) - 1 AS VARCHAR) + '/' + CAST(YEAR(serv.DataAvvio) AS VARCHAR)) END) IN ('2018/2019', '2019/2020', '2020/2021', '2021/2022')

UNION

SELECT
    (CASE WHEN MONTH(ordini.DataParcella)>=9 THEN (CAST(YEAR(ordini.DataParcella) AS VARCHAR) + '/' + CAST(YEAR(ordini.DataParcella) + 1 AS VARCHAR)) ELSE (CAST(YEAR(ordini.DataParcella) - 1 AS VARCHAR) + '/' + CAST(YEAR(ordini.DataParcella) AS VARCHAR)) END) AS AnnoAmm,
    serv.IDedizione,
    sedi.SiglaSede,
    'Parcella' AS Tipo,
    (CASE WHEN aziende.IDazienda IS NOT NULL THEN aziende.DescrAzienda ELSE (docenti.Cognome + ' ' + docenti.Nome) END) AS Collaboratore,
    (CASE WHEN aziende.IDazienda IS NULL THEN docenti.CodFiscale ELSE (CASE WHEN aziende.PIVA IS NOT NULL THEN aziende.PIVA ELSE aziende.CodFiscale END) END) AS CF_PIVA,
    tp.TipoProgetto,
    form.TipoFormativoInterno,
    causali.TipoCausaleParcella,
    NULL AS TotOreFatte,
    ordini.sngTotale

FROM t_DocentiParcelle AS ordini 
LEFT OUTER JOIN t_Progetti AS progetti ON ordini.FK_Progetto = progetti.IDprogetto
LEFT OUTER JOIN t_TipoProgetto AS tp ON progetti.FK_TipoProgetto = tp.IDtprogetto
LEFT OUTER JOIN t_TipoCausaleParcella AS causali ON ordini.FK_Causale = causali.IDtcausaparce
LEFT OUTER JOIN t_PianoServizi AS serv ON ordini.FK_Edizione = serv.IDedizione
LEFT OUTER JOIN t_TipoFormativoInterno AS form ON form.IDtformaint = serv.FK_TipoFormativoInterno
LEFT OUTER JOIN t_CommissioniEsameComponenti AS componenti ON ordini.FK_Commissione = componenti.IDcomponente
LEFT OUTER JOIN t_Docenti AS docenti ON ordini.FK_Docente = docenti.IDdocente
LEFT OUTER JOIN t_Sedi AS sedi ON ordini.FK_Sede = sedi.IDsede
LEFT OUTER JOIN t_Azioni AS azioni ON ordini.FK_Azione = azioni.IDazione
LEFT OUTER JOIN t_Aziende AS aziende ON ordini.FK_Azienda = aziende.IDazienda

WHERE ordini.DataPagamento IS NOT NULL
AND (CASE WHEN MONTH(ordini.DataParcella)>=9 THEN (CAST(YEAR(ordini.DataParcella) AS VARCHAR) + '/' + CAST(YEAR(ordini.DataParcella) + 1 AS VARCHAR)) ELSE (CAST(YEAR(ordini.DataParcella) - 1 AS VARCHAR) + '/' + CAST(YEAR(ordini.DataParcella) AS VARCHAR)) END) IN ('2018/2019', '2019/2020', '2020/2021', '2021/2022')

