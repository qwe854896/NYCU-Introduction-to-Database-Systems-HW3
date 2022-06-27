DROP TABLE IF EXISTS Video_Games;
CREATE TABLE IF NOT EXISTS Video_Games (
	"Name"                TEXT,
    "Platform"            TEXT,
    "Year_of_Release"     INT,
    "Genre"               TEXT,
    "Publisher"           TEXT,
    "NA_Sales"            NUMERIC(7, 3),
    "EU_Sales"            NUMERIC(7, 3),
    "JP_Sales"            NUMERIC(7, 3),
    "Other_Sales"         NUMERIC(7, 3),
    "Global_Sales"        NUMERIC(7, 3),
    "Critic_Score"        INT,
    "Critic_Count"        INT,
    "User_Score"          NUMERIC(7, 3),
    "User_Count"          INT,
    "Developer"           TEXT,
    "Rating"              TEXT,

    PRIMARY KEY ("Name", "Platform", "Year_of_Release")
);
ALTER TABLE IF EXISTS Video_Games
    OWNER to postgres;

CREATE INDEX indexName
ON Video_Games ("Name");

CREATE INDEX indexYear
ON Video_Games ("Year_of_Release");

CREATE INDEX indexGenre
ON Video_Games ("Genre");