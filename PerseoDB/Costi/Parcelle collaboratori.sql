SELECT
    --ordini.IDparcella AS Parcella,
    (CASE WHEN MONTH(ordini.DataParcella)>=9 THEN (CAST(YEAR(ordini.DataParcella) AS VARCHAR) + '/' + CAST(YEAR(ordini.DataParcella) + 1 AS VARCHAR)) ELSE (CAST(YEAR(ordini.DataParcella) - 1 AS VARCHAR) + '/' + CAST(YEAR(ordini.DataParcella) AS VARCHAR)) END) AS AnnoAmm,
    serv.IDedizione,
    sedi.SiglaSede,
    progetti.DescrProgetto,
    progetti.CodiceProgetto,
    (CASE WHEN aziende.IDazienda IS NOT NULL THEN aziende.DescrAzienda ELSE (docenti.Cognome + ' ' + docenti.Nome) END) AS Collaboratore,
    (CASE WHEN aziende.IDazienda IS NULL THEN docenti.CodFiscale ELSE (CASE WHEN aziende.PIVA IS NOT NULL THEN aziende.PIVA ELSE aziende.CodFiscale END) END) AS CF_PIVA,
    --??progetti.TipoProgetto,
    form.TipoFormativoInterno,
    ---serv.DescrEdizione,
    ---serv.CodiceEdizione,
    -- TipoAttivita
    -- QuotaOraIncarico
    (CASE WHEN componenti.IDcomponente IS NOT NULL THEN ('Sì') ELSE NULL END) AS CommissioneEsame,
    ordini.DescrCostiAggiuntivi,
    ordini.DescrParcella,
    causali.TipoCausaleParcella,
    --componenti.DescrAmmNomina,
    --docenti.DescrDatoreLavoro,
    --ordini.DataParcella,       
    --ordini.DataPagamento,
    --ordini.ImportoParcella,
    --ordini.sngRiva,
    --ordini.sngCassaPrev,
    --ordini.sngIVA,
    (ordini.CostiAnticipo+ordini.CostiVitto+ordini.CostiViaggio) AS Costi,
    ordini.sngTotale
    --UNICODE(ordini.NumeroFattura) as NumeroFattura
    --ordini.DataFattura

FROM t_Progetti AS progetti
RIGHT OUTER JOIN t_DocentiParcelle AS ordini
LEFT OUTER JOIN t_TipoCausaleParcella AS causali ON ordini.FK_Causale = causali.IDtcausaparce
LEFT OUTER JOIN t_PianoServizi AS serv ON ordini.FK_Edizione = serv.IDedizione
LEFT OUTER JOIN t_TipoFormativoInterno AS form ON form.IDtformaint = serv.FK_TipoFormativoInterno
LEFT OUTER JOIN t_CommissioniEsameComponenti AS componenti ON ordini.FK_Commissione = componenti.IDcomponente
LEFT OUTER JOIN t_Docenti AS docenti ON ordini.FK_Docente = docenti.IDdocente
LEFT OUTER JOIN t_Sedi AS sedi ON ordini.FK_Sede = sedi.IDsede ON progetti.IDprogetto = ordini.FK_Progetto
LEFT OUTER JOIN t_Azioni AS azioni ON ordini.FK_Azione = azioni.IDazione
LEFT OUTER JOIN t_Aziende AS aziende ON ordini.FK_Azienda = aziende.IDazienda

WHERE ordini.DataPagamento IS NOT NULL
AND (CASE WHEN MONTH(ordini.DataParcella)>=9 THEN (CAST(YEAR(ordini.DataParcella) AS VARCHAR) + '/' + CAST(YEAR(ordini.DataParcella) + 1 AS VARCHAR)) ELSE (CAST(YEAR(ordini.DataParcella) - 1 AS VARCHAR) + '/' + CAST(YEAR(ordini.DataParcella) AS VARCHAR)) END) IN ('2018/2019', '2019/2020', '2020/2021', '2021/2022')

ORDER BY ordini.DataPagamento 