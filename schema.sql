-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : sam. 27 juin 2026 à 08:07
-- Version du serveur : 10.4.27-MariaDB
-- Version de PHP : 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `locagest_db`
--

-- --------------------------------------------------------

--
-- Structure de la table `chambres`
--

CREATE TABLE `chambres` (
  `id` int(11) NOT NULL,
  `numero` varchar(20) NOT NULL,
  `superficie` float NOT NULL,
  `loyer_mensuel` decimal(10,2) NOT NULL,
  `description` text DEFAULT NULL,
  `statut` enum('disponible','occupee') NOT NULL DEFAULT 'disponible',
  `proprietaire_id` int(11) DEFAULT NULL,
  `date_creation` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `chambres`
--

INSERT INTO `chambres` (`id`, `numero`, `superficie`, `loyer_mensuel`, `description`, `statut`, `proprietaire_id`, `date_creation`) VALUES
(1, 'chambre 001', 50, '40000.00', 'Chambre moderne a logbessou', 'occupee', 1, '2026-06-27 03:53:41'),
(2, 'Chambre 002', 50, '40000.00', 'Chambre moderne a logbessou', 'occupee', 1, '2026-06-27 03:54:04'),
(3, 'chambre 003', 50, '40000.00', 'Chambre moderne a logbessou', 'occupee', 1, '2026-06-27 03:54:16'),
(4, 'chambre 004', 50, '40000.00', 'Chambre moderne a logbessou', 'occupee', 1, '2026-06-27 03:54:31'),
(5, 'chambre 005', 50, '50000.00', 'Chambre ultra moderne Ange raphael, proche du campus 2\r\n', 'disponible', 1, '2026-06-27 05:08:19');

-- --------------------------------------------------------

--
-- Structure de la table `locataires`
--

CREATE TABLE `locataires` (
  `id` int(11) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) NOT NULL,
  `telephone` varchar(20) NOT NULL,
  `email` varchar(150) DEFAULT NULL,
  `cni` varchar(50) NOT NULL,
  `adresse` varchar(255) DEFAULT NULL,
  `date_creation` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `locataires`
--

INSERT INTO `locataires` (`id`, `nom`, `prenom`, `telephone`, `email`, `cni`, `adresse`, `date_creation`) VALUES
(1, 'Dohou djomo', 'leila', '658784596', 'leila@gmail.com', 'CMR01248756', 'Bellavie-Ndokito', '2026-06-27 03:55:31'),
(3, 'Jiongo ', 'Merveille', '687598674', 'Merveille@gmail.com', 'CMR01248778', 'yassa', '2026-06-27 03:57:19'),
(4, 'Tamba', 'eric', '698754872', 'eric@gmail.com', 'CMR012487e5', 'PK17', '2026-06-27 05:09:52');

-- --------------------------------------------------------

--
-- Structure de la table `locations`
--

CREATE TABLE `locations` (
  `id` int(11) NOT NULL,
  `locataire_id` int(11) NOT NULL,
  `chambre_id` int(11) NOT NULL,
  `date_debut` date NOT NULL,
  `date_fin` date DEFAULT NULL,
  `statut` enum('active','terminee') NOT NULL DEFAULT 'active',
  `date_creation` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `locations`
--

INSERT INTO `locations` (`id`, `locataire_id`, `chambre_id`, `date_debut`, `date_fin`, `statut`, `date_creation`) VALUES
(1, 1, 1, '2026-06-01', NULL, 'active', '2026-06-27 03:58:11'),
(2, 1, 3, '2026-05-01', NULL, 'active', '2026-06-27 03:58:46'),
(4, 3, 2, '2026-04-01', NULL, 'active', '2026-06-27 04:41:45'),
(5, 4, 4, '2026-03-01', NULL, 'active', '2026-06-27 05:10:27');

-- --------------------------------------------------------

--
-- Structure de la table `paiements`
--

CREATE TABLE `paiements` (
  `id` int(11) NOT NULL,
  `location_id` int(11) NOT NULL,
  `mois` date NOT NULL,
  `date_echeance` date NOT NULL,
  `montant` decimal(10,2) NOT NULL,
  `date_paiement` date DEFAULT NULL,
  `statut` enum('en_attente','paye','en_retard') NOT NULL DEFAULT 'en_attente',
  `mode_paiement` varchar(50) DEFAULT NULL,
  `numero_recu` varchar(30) DEFAULT NULL,
  `date_creation` datetime DEFAULT current_timestamp(),
  `numero_recu_groupe` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `paiements`
--

INSERT INTO `paiements` (`id`, `location_id`, `mois`, `date_echeance`, `montant`, `date_paiement`, `statut`, `mode_paiement`, `numero_recu`, `date_creation`, `numero_recu_groupe`) VALUES
(1, 1, '2026-06-01', '2026-06-05', '40000.00', '2026-06-27', 'paye', 'especes', 'RECU-1-1-20260627', '2026-06-27 03:58:11', NULL),
(2, 2, '2026-06-01', '2026-06-05', '40000.00', '2026-06-27', 'paye', 'especes', 'RECU-2-2-20260627', '2026-06-27 03:58:46', NULL),
(6, 4, '2026-06-01', '2026-06-05', '40000.00', NULL, 'en_retard', NULL, NULL, '2026-06-27 04:41:45', NULL),
(7, 4, '2026-05-01', '2026-05-05', '40000.00', '2026-06-27', 'paye', 'especes', 'RECU-4-7-20260627', '2026-06-27 04:41:52', NULL),
(8, 5, '2026-06-01', '2026-06-05', '40000.00', '2026-06-27', 'paye', 'especes', 'RECU-5-8-20260627', '2026-06-27 05:10:27', 'RECU-G-5-10-20260627'),
(9, 5, '2026-07-01', '2026-07-05', '40000.00', NULL, 'en_attente', NULL, NULL, '2026-06-27 05:10:32', NULL),
(10, 5, '2026-05-01', '2026-05-05', '40000.00', '2026-06-27', 'paye', 'especes', 'RECU-5-10-20260627', '2026-06-27 05:27:40', 'RECU-G-5-10-20260627'),
(13, 5, '2026-04-01', '2026-04-05', '40000.00', '2026-06-27', 'paye', 'especes', 'RECU-5-13-20260627', '2026-06-27 05:29:57', NULL);

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `mot_de_passe_hash` varchar(255) NOT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `date_creation` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `users`
--

INSERT INTO `users` (`id`, `nom`, `email`, `mot_de_passe_hash`, `telephone`, `date_creation`) VALUES
(1, 'Apoussie pezemo', 'apoussie@gmail.com', 'scrypt:32768:8:1$fF4qKauBIclgWJxs$7981b27e178278d24ae588c08aa4d1d1a2619c5efb468d9c69300a98dbb36e1860694a63c1d26f86ae9420b30289a3996aaaade3e9841c3ac7f7a35cbf2c1e24', '698024380', '2026-06-27 03:52:40');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `chambres`
--
ALTER TABLE `chambres`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero` (`numero`),
  ADD KEY `proprietaire_id` (`proprietaire_id`),
  ADD KEY `idx_chambres_statut` (`statut`);

--
-- Index pour la table `locataires`
--
ALTER TABLE `locataires`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `cni` (`cni`);

--
-- Index pour la table `locations`
--
ALTER TABLE `locations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `locataire_id` (`locataire_id`),
  ADD KEY `chambre_id` (`chambre_id`),
  ADD KEY `idx_locations_statut` (`statut`);

--
-- Index pour la table `paiements`
--
ALTER TABLE `paiements`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_recu` (`numero_recu`),
  ADD KEY `location_id` (`location_id`),
  ADD KEY `idx_paiements_statut` (`statut`),
  ADD KEY `idx_paiements_mois` (`mois`);

--
-- Index pour la table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `chambres`
--
ALTER TABLE `chambres`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `locataires`
--
ALTER TABLE `locataires`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `locations`
--
ALTER TABLE `locations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `paiements`
--
ALTER TABLE `paiements`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT pour la table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `chambres`
--
ALTER TABLE `chambres`
  ADD CONSTRAINT `chambres_ibfk_1` FOREIGN KEY (`proprietaire_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Contraintes pour la table `locations`
--
ALTER TABLE `locations`
  ADD CONSTRAINT `locations_ibfk_1` FOREIGN KEY (`locataire_id`) REFERENCES `locataires` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `locations_ibfk_2` FOREIGN KEY (`chambre_id`) REFERENCES `chambres` (`id`) ON DELETE CASCADE;

--
-- Contraintes pour la table `paiements`
--
ALTER TABLE `paiements`
  ADD CONSTRAINT `paiements_ibfk_1` FOREIGN KEY (`location_id`) REFERENCES `locations` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
