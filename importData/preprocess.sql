DROP TABLE IF EXISTS temp;
CREATE TABLE IF NOT EXISTS temp (
	"Name"                TEXT,
    "Platform"            TEXT,
    "Year_of_Release"     TEXT,  --- INT
    "Genre"               TEXT,
    "Publisher"           TEXT,
    "NA_Sales"            NUMERIC(7, 3),
    "EU_Sales"            NUMERIC(7, 3),
    "JP_Sales"            NUMERIC(7, 3),
    "Other_Sales"         NUMERIC(7, 3),
    "Global_Sales"        NUMERIC(7, 3),
    "Critic_Score"        INT,
    "Critic_Count"        INT,
    "User_Score"          TEXT,  --- NUMERIC(7, 3),
    "User_Count"          INT,
    "Developer"           TEXT,
    "Rating"              TEXT
);
ALTER TABLE IF EXISTS temp
    OWNER to postgres;

TRUNCATE Video_Games;