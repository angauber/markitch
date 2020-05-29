CREATE TABLE `{}` (
	`id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`word1` varchar(255) NOT NULL,
	`word2` varchar(255) NOT NULL,
	`nb` BIGINT UNSIGNED NOT NULL,
	PRIMARY KEY (`id`),
	INDEX `word1_index` (`word1`),
	INDEX `word2_index` (`word2`),
	UNIQUE `unique_words_index` (`word1`, `word2`)
);
