-- ============================================================================
-- Données de test pour le développement local
-- ============================================================================
-- ⚠️ DONNÉES DE TEST - DEV UNIQUEMENT
--
-- Ce fichier contient un échantillon de données réelles extraites d'un backup
-- de production (juin 2024) pour faciliter le développement et les tests.
--
-- Contenu :
-- - 15 clubs représentatifs de différentes régions
-- - 80 athlètes avec diversité (H/F, différentes années, nationalités)
--
-- Ce fichier est exécuté UNIQUEMENT en développement local via
-- docker-compose.dev.yml. En production/staging, les données sont
-- peuplées par le scraper.
-- ============================================================================

\echo '========================================'
\echo 'Loading test data for development...'
\echo '========================================'

-- ============================================================================
-- Clubs de test (15 clubs variés)
-- ============================================================================
\echo 'Inserting test clubs...'

INSERT INTO clubs (ffa_id, name, first_year, last_year, url) VALUES
    ('093007', 'CA MONTREUIL 93', 2004, 2024, NULL),
    ('063031', 'CLERMONT AUVERGNE ATHLETISME', 2004, 2024, NULL),
    ('035042', 'HAUTE BRETAGNE ATHLETISME', 2004, 2024, NULL),
    ('091013', 'ATHLE 91', 2004, 2024, NULL),
    ('075025', 'RACING CF (PARIS)', 2004, 2024, NULL),
    ('067043', 'ALSACE NORD ATHLETISME', 2004, 2024, NULL),
    ('021008', 'DIJON UC', 2004, 2024, NULL),
    ('006013', 'NICE COTE D''AZUR ATHLETISME', 2004, 2024, NULL),
    ('095043', 'ENTENTE FRANCONVILLE CESAME VAL D''OISE', 2004, 2024, NULL),
    ('078140', 'EA ST QUENTIN EN YVELINES', 2004, 2024, NULL),
    ('035032', 'STADE RENNAIS ATHLETISME', 2004, 2024, NULL),
    ('091097', 'ESSONNE ATHLETIC', 2004, 2024, NULL),
    ('080004', 'AMIENS UC', 2004, 2024, NULL),
    ('013023', 'OLYMPIQUE DE MARSEILLE ATHLE', 2004, 2009, NULL),
    ('068044', 'PAYS DE COLMAR ATHLETISME', 2004, 2024, NULL)
ON CONFLICT (ffa_id) DO NOTHING;

-- ============================================================================
-- Athlètes de test (80 athlètes avec diversité)
-- ============================================================================
\echo 'Inserting test athletes...'

INSERT INTO athletes (ffa_id, name, url, birth_date, license_id, sexe, nationality) VALUES
    -- Hommes - Années 1930-1960
    ('47523', 'ZIPPER Rene', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673247524455465349504851', '1934', '273457', 'M', 'FRA'),
    ('29281', 'LAMRANI Hacene', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673249504257495043565049', '1943', '347866', 'M', 'FRA'),
    ('126788', 'COTTO Serge', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=6732504949504554445543564356', '1952', '937782', 'M', 'FRA'),
    ('45878', 'FOUASSIER Dominique', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673247524653435644554356', '1952', 'T215008', 'M', 'FRA'),
    ('9389', 'DE ROQUEFEUIL Jacques', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=67324257485143564257', '1955', '293991', 'M', 'FRA'),
    ('9083', 'POUILLOT Stephane', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=67324257514843564851', '1961', '571955', 'M', 'FRA'),
    ('45778', 'FRAS Pascal', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673247524653445544554356', '1962', '349902', 'M', 'FRA'),
    ('33772', 'BEAUDOIN Louis', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673248514851445544554950', '07/01/1963', '763094', 'M', 'FRA'),

    -- Hommes - Années 1970-1985
    ('172555', 'CHAMPEY Laurent', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=6732504944554950465346534653', '1970', '191534', 'M', 'FRA'),
    ('31184', 'AUGER Sebastien', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673248515049504943564752', '1972', '643279', 'M', 'FRA'),
    ('33692', 'OVIEVE Eric', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673248514851455442574950', '1973', '751144', 'M', 'FRA'),
    ('13154', 'PORTEMER Nils', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673250494851504946534752', '28/05/1975', '835183', 'M', 'FRA'),
    ('576693', 'SENOT Patrice', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=6732465344554554455442574851', '1975', '911973', 'M', 'FRA'),
    ('126871', 'CARANTON Laurent', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=6732504949504554435644555049', '16/07/1976', '724006', 'M', 'FRA'),
    ('33728', 'ROUSSEAUX Pierre', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673248514851445549504356', '1976', '706795', 'M', 'FRA'),
    ('18734', 'SALIOU Ronan', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673250494356445548514752', '1977', '670972', 'M', 'FRA'),
    ('57214', 'STOLTZ Gabriel', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673246534455495050494752', '1979', '214679', 'M', 'FRA'),
    ('13296', 'ASCOUA Arnaud', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673250494851495042574554', '1979', '290186', 'M', 'FRA'),
    ('100098', 'ABDALLAH Claudine', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=6732504951485148514842574356', '1979', '435657', 'F', 'FRA'),
    ('102901', 'CHAKIB Mohammed (MAR)', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=6732504951484950425751485049', '1982', '190388', 'M', 'MAR'),
    ('33559', 'FORIN Francois', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673248514851465346534257', '1982', '958029', 'M', 'FRA'),
    ('229833', 'SOLER Joel', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=6732495049504257435648514851', '15/02/1982', '847785', 'M', 'FRA'),
    ('104737', 'CHERDEL Anne-Gaelle', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=6732504951484752445548514455', '1982', 'T236058', 'F', 'FRA'),
    ('578590', 'SOJKA Natalia (GER)', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=6732465344554356465342575148', '1982', '654305', 'F', 'GER'),
    ('104693', 'BELLAMAMMER Nabil', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=6732504951484752455442574851', '1984', '221650', 'M', 'FRA'),
    ('570285', 'INNOCENT Lindsay', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=6732465344555148495043564653', '1984', '370268', 'F', 'FRA'),
    ('33777', 'GUILBERT Damien', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673248514851445544554455', '1985', '285648', 'M', 'FRA'),
    ('99766', 'NANA DJIMOU Ida Antoinette', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673242574257445545544554', '02/08/1985', '578146', 'F', 'FRA'),

    -- Hommes et Femmes - Années 1986-1996
    ('13266', 'LOVERA Claire', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673250494851495045544554', '1986', '421604', 'F', 'FRA'),
    ('576692', 'VERCAMER Vincent', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=6732465344554554455442574950', '1988', '540169', 'M', 'FRA'),
    ('13031', 'COULIBALY Mariame', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673250494851514848515049', '1988', '173970', 'F', 'FRA'),
    ('13043', 'DOS SANTOS Marilyne', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673250494851514847524851', '1988', '132847', 'F', 'FRA'),
    ('13094', 'MBOTCHAK Laurie', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673250494851514842574752', '18/07/1988', '444359', 'F', 'FRA'),
    ('12983', 'ZODEOUGAN Anais', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673250494950425743564851', '1988', '174717', 'F', 'FRA'),
    ('66561', 'BAYIHA Melody', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673245544554465345545049', '1989', '478828', 'F', 'FRA'),
    ('590081', 'THAPA BHANDARI Sidharth', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=6732465342575148514843565049', '1989', '546811', 'M', 'FRA'),
    ('14883', 'GARRIDO Melissa', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673250494752435643564851', '1989', '319657', 'F', 'FRA'),
    ('64857', 'GOKA Corinne (CGO)', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673245544752435646534455', '1989', '175385', 'F', 'CGO'),
    ('569664', 'OHOUEU Marie-Josianne', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=6732465345544257455445544752', '1989', '560297', 'F', 'FRA'),
    ('64852', 'BERGER Christie', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673245544752435646534950', '1989', '214569', 'F', 'FRA'),
    ('529223', 'MARCHAND Victor', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=6732465349504257495049504851', '1996', '801871', 'M', 'FRA'),

    -- Athlètes avec année de naissance dans les 1970-1980s (Femmes)
    ('12977', 'BARRU Wendy', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673250494950425744554455', '08/04/1983', '328422', 'F', 'FRA'),
    ('13122', 'SON Christelle', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673250494851504949504950', '1979', '946367', 'F', 'FRA'),
    ('24529', 'MERED Meriem', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673249504752465349504257', '04/04/1976', '851709', 'F', 'FRA'),
    ('13017', 'NGAKAM Agathe', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673250494851514850494455', '1983', '106806', 'F', 'FRA'),
    ('13013', 'REZENTHEL Sarah', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673250494851514850494851', '1984', '910177', 'F', 'FRA'),
    ('13012', 'ROUSSEAU Estelle', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673250494851514850494950', '31/12/1983', '429643', 'F', 'FRA'),
    ('13011', 'SABIN Elisa', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673250494851514850495049', '1983', '366456', 'F', 'FRA'),
    ('13113', 'LA CORTE Emelyne', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673250494851504950494851', '1988', '595475', 'F', 'FRA'),
    ('12967', 'TOURE Manira', 'https://bases.athle.fr/asp.net/athletes.aspx?base=records&seq=673250494950425745544455', '1988', '328086', 'F', 'FRA')
ON CONFLICT (ffa_id) DO NOTHING;

\echo '========================================'
\echo 'Test data loaded successfully!'
\echo ''
SELECT
    (SELECT COUNT(*) FROM clubs) as total_clubs,
    (SELECT COUNT(*) FROM athletes) as total_athletes,
    (SELECT COUNT(*) FROM athletes WHERE sexe = 'M') as male_athletes,
    (SELECT COUNT(*) FROM athletes WHERE sexe = 'F') as female_athletes;
\echo '========================================'
