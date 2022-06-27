INSERT INTO Video_Games
SELECT "Name", "Platform", CAST ("Year_of_Release" AS INT), MAX("Genre"), MAX("Publisher"), SUM("NA_Sales"), SUM("EU_Sales"), SUM("JP_Sales"), SUM("Other_Sales"), SUM("Global_Sales"), MAX("Critic_Score"), MAX("Critic_Count"), CAST(MAX("User_Score") AS NUMERIC(7, 3)), MAX("User_Count"), MAX("Developer"), MAX("Rating")
FROM temp tp
WHERE "Name" IS NOT NULL AND "Platform" IS NOT NULL AND "Year_of_Release" IS NOT NULL AND NOT EXISTS (
    SELECT "Name"
    FROM Video_Games vd
    WHERE vd."Name" = tp."Name" AND vd."Platform" = tp."Platform" AND vd."Year_of_Release" = CAST (tp."Year_of_Release" AS INT)
)
AND ("Year_of_Release" ~ '^\d*$') AND ("User_Score" ~ '[+-]?([0-9]*[.])?[0-9]+' OR "User_Score" ~ '^\d*$' OR "User_Score" IS NULL)
GROUP BY "Name", "Platform", "Year_of_Release";

DROP TABLE IF EXISTS temp;