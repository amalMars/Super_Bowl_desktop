-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : jeu. 20 juil. 2023 à 18:57
-- Version du serveur : 8.0.31
-- Version de PHP : 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `super_bowl`
--

-- --------------------------------------------------------

--
-- Structure de la table `commentaire`
--

DROP TABLE IF EXISTS `commentaire`;
CREATE TABLE IF NOT EXISTS `commentaire` (
  `id_commentaire` int UNSIGNED NOT NULL,
  `utilisateur_id` int NOT NULL,
  `match_id` int NOT NULL,
  `commentaire` text NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `commentaire`
--

INSERT INTO `commentaire` (`id_commentaire`, `utilisateur_id`, `match_id`, `commentaire`) VALUES
(0, 0, 0, 'BRAVO !!'),
(1, 0, 6, 'BRAVOO§§!!');

-- --------------------------------------------------------

--
-- Structure de la table `cote`
--

DROP TABLE IF EXISTS `cote`;
CREATE TABLE IF NOT EXISTS `cote` (
  `id_cote` int UNSIGNED NOT NULL,
  `match_id` int NOT NULL,
  `equipe_id` int NOT NULL,
  `valeur` int NOT NULL,
  `utilisateur_id` int NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `cote`
--

INSERT INTO `cote` (`id_cote`, `match_id`, `equipe_id`, `valeur`, `utilisateur_id`) VALUES
(0, 0, 1, 100, 0),
(0, 0, 1, 120, 0),
(1, 11, 1, 30, 0);

-- --------------------------------------------------------

--
-- Structure de la table `equipe`
--

DROP TABLE IF EXISTS `equipe`;
CREATE TABLE IF NOT EXISTS `equipe` (
  `id_equipe` int UNSIGNED NOT NULL,
  `nom_equipe` varchar(60) NOT NULL,
  `pays` varchar(60) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `equipe`
--

INSERT INTO `equipe` (`id_equipe`, `nom_equipe`, `pays`) VALUES
(0, 'TUN', 'TUNISIE'),
(1, 'FR', 'FRANCE'),
(2, 'ALG', 'algerie');

-- --------------------------------------------------------

--
-- Structure de la table `historique`
--

DROP TABLE IF EXISTS `historique`;
CREATE TABLE IF NOT EXISTS `historique` (
  `historique_id` int UNSIGNED NOT NULL,
  `utilisateur_id` int NOT NULL,
  `equipe_id` int NOT NULL,
  `match_id` int NOT NULL,
  `valeur` int NOT NULL,
  `date` datetime NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `joueur`
--

DROP TABLE IF EXISTS `joueur`;
CREATE TABLE IF NOT EXISTS `joueur` (
  `id_joueur` int UNSIGNED NOT NULL,
  `equipe_id` int NOT NULL,
  `nom_joeur` varchar(60) NOT NULL,
  `prenom_joueur` varchar(60) NOT NULL,
  `numero_joeur` int NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `joueur`
--

INSERT INTO `joueur` (`id_joueur`, `equipe_id`, `nom_joeur`, `prenom_joueur`, `numero_joeur`) VALUES
(0, 0, 'jihed', 'saa', 11),
(1, 1, 'amel', 'ma', 12),
(1, 1, 'amel', 'ma', 12),
(3, 1, 'SABA', 'SAA', 13),
(5, 0, 'jouman', 'saa', 50);

-- --------------------------------------------------------

--
-- Structure de la table `matchs`
--

DROP TABLE IF EXISTS `matchs`;
CREATE TABLE IF NOT EXISTS `matchs` (
  `id_match` int UNSIGNED NOT NULL,
  `equipe1_id` int NOT NULL,
  `equipe2_id` int NOT NULL,
  `heur_debut` time NOT NULL,
  `heur_fin` time NOT NULL,
  `statut` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `score` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `meteo` int DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `matchs`
--

INSERT INTO `matchs` (`id_match`, `equipe1_id`, `equipe2_id`, `heur_debut`, `heur_fin`, `statut`, `score`, `meteo`) VALUES
(8, 0, 1, '06:35:00', '07:35:00', 'clos', NULL, NULL),
(9, 0, 1, '06:35:00', '07:35:00', 'clos', NULL, NULL),
(11, 0, 2, '00:18:13', '02:18:13', 'clos', 'En cours', 40),
(12, 0, 1, '00:21:22', '01:51:22', 'a venir', 'En cours', 40);

-- --------------------------------------------------------

--
-- Structure de la table `mise`
--

DROP TABLE IF EXISTS `mise`;
CREATE TABLE IF NOT EXISTS `mise` (
  `id_mise` int UNSIGNED NOT NULL,
  `utilisateur_id` int NOT NULL,
  `match_id` int NOT NULL,
  `equipe_id` int NOT NULL,
  `montant` int NOT NULL,
  `date_mise` date NOT NULL,
  `montant_gagner` int NOT NULL,
  `montant_perdu` int NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `mise`
--

INSERT INTO `mise` (`id_mise`, `utilisateur_id`, `match_id`, `equipe_id`, `montant`, `date_mise`, `montant_gagner`, `montant_perdu`) VALUES
(0, 0, 6, 1, 100, '2023-07-12', 0, 0),
(1, 0, 11, 0, 33, '2023-07-13', 0, 0),
(2, 0, 12, 1, 50, '2023-07-13', 0, 0);

-- --------------------------------------------------------

--
-- Structure de la table `utilisateur`
--

DROP TABLE IF EXISTS `utilisateur`;
CREATE TABLE IF NOT EXISTS `utilisateur` (
  `id_utilisateur` int UNSIGNED NOT NULL,
  `nom` varchar(60) NOT NULL,
  `prenom` varchar(60) NOT NULL,
  `email` varchar(60) NOT NULL,
  `mot_passe` varchar(60) NOT NULL,
  `email_val` int DEFAULT NULL,
  `est_admin` int DEFAULT NULL,
  `est_commentateur` int DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `utilisateur`
--

INSERT INTO `utilisateur` (`id_utilisateur`, `nom`, `prenom`, `email`, `mot_passe`, `email_val`, `est_admin`, `est_commentateur`) VALUES
(0, 'amel', 'ma', 'amelma@gmail.com', 'aaaa', NULL, NULL, NULL),
(2, 'SAA', 'jou', 'saajou@gmail.com', 'aaaa', NULL, NULL, NULL),
(3, 'souad', 'ma', 'souadma@gmail.com', 'aaaa', NULL, NULL, NULL),
(4, 'amel', 'SAA', 'amelma@gmail.com', 'aaaa1', NULL, NULL, 1);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
