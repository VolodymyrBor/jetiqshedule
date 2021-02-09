-- upgrade --
CREATE TABLE IF NOT EXISTS `subject` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(200) NOT NULL UNIQUE,
    `teacher` VARCHAR(200) NOT NULL,
    `meet_url_name` VARCHAR(200)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `lesson` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `time` DATETIME(6) NOT NULL,
    `weekday` VARCHAR(9) NOT NULL  COMMENT 'MONDAY: monday\nTUESDAY: tuesday\nWEDNESDAY: wednesday\nthursday: thursday\nfriday: friday',
    `week_slug` VARCHAR(200) NOT NULL,
    `subject_id` INT NOT NULL,
    CONSTRAINT `fk_lesson_subject_8aecf416` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `scheduledvisit` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `date` DATE NOT NULL,
    `login` VARCHAR(200) NOT NULL,
    `password` VARCHAR(200) NOT NULL,
    `status` VARCHAR(10) NOT NULL  COMMENT 'CREATED: created\nRUNNING: running\nSUCCESSFUL: successful\nFAILED: failed' DEFAULT 'created',
    `error_message` VARCHAR(200),
    `visit_start` DATETIME(6),
    `visit_finish` DATETIME(6),
    `lesson_id` INT NOT NULL,
    CONSTRAINT `fk_schedule_lesson_5d860b5f` FOREIGN KEY (`lesson_id`) REFERENCES `lesson` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(20) NOT NULL,
    `content` TEXT NOT NULL
) CHARACTER SET utf8mb4;
