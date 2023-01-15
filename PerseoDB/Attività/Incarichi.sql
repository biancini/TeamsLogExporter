SELECT
    (CASE WHEN MONTH(t_PianoServizi.DataAvvio)>=9 THEN (CAST(YEAR(t_PianoServizi.DataAvvio) AS VARCHAR) + '/' + CAST(YEAR(t_PianoServizi.DataAvvio) + 1 AS VARCHAR)) ELSE (CAST(YEAR(t_PianoServizi.DataAvvio) - 1 AS VARCHAR) + '/' + CAST(YEAR(t_PianoServizi.DataAvvio) AS VARCHAR)) END) AS AnnoAmm,
    SiglaSede AS Sede,
    Cognome, Nome,
    (CASE WHEN FK_Tipo=1 THEN 'Generico' WHEN FK_Tipo=2 THEN 'Interno' ELSE 'Esterno' END) AS StrTipo,
    --CodFiscale,
    --DescrTitoloStudio,
    --DATEDIFF(year, t_Docenti.DataRec, GETDATE()) AS AnniEsperienzaEnaip,
    --CodiceEdizione,
    DescrEdizione,
    --CodiceProgetto,
    DescrProgetto,
    TipoFormativoInterno AS TipoFormativo,
    DataAvvio, DataFine,
    DataInizioFA, DataFineFA,
    Durata,
    TipoAttivita, Aula, ContrattoAula,
    --DescrArgomento,
    OreAssegnate,
    (CASE WHEN FK_Tipo<=2 THEN OreAssegnate ELSE (SELECT SUM(OreSvolgere) FROM t_IncarichiEdizioniContratti WHERE FK_IncaricoEdizione=IDincarico AND ApprovaIncarico=1) END) AS OreApprovate,
    IncaricoBloccato,
    IncaricoGenericoGratuito
    --DescrIncarico,
    
FROM t_Docenti
INNER JOIN t_IncarichiEdizioni ON t_Docenti.IDdocente = t_IncarichiEdizioni.FK_Docente
INNER JOIN t_PianoServizi ON t_IncarichiEdizioni.FK_Edizione = t_PianoServizi.IDedizione
INNER JOIN t_Sedi ON t_PianoServizi.FK_SedeEdizione = t_Sedi.IDsede
INNER JOIN t_Azioni ON t_PianoServizi.FK_Azione = t_Azioni.IDazione
INNER JOIN t_Progetti ON t_Azioni.FK_Progetto = t_Progetti.IDprogetto
INNER JOIN t_Bandi ON t_Progetti.FK_Bando = t_Bandi.IDbando
INNER JOIN t_AttivitaEdizioni ON t_IncarichiEdizioni.FK_Attivita = t_AttivitaEdizioni.IDattedi
INNER JOIN t_TipoAttivitaEdizione ON t_AttivitaEdizioni.FK_TipoAttivita = t_TipoAttivitaEdizione.IDtattivita
LEFT OUTER JOIN t_TipoFormativoInterno ON t_PianoServizi.FK_TipoFormativoInterno = t_TipoFormativoInterno.IDtformaint
LEFT OUTER JOIN t_ArgomentiModuli ON t_IncarichiEdizioni.FK_Argomento = t_ArgomentiModuli.IDargomento

WHERE AnnoBando IN ( '2018/2019', '2019/2020', '2021/2022' )
AND FK_Tipo > 1

AND SedeTest=0
