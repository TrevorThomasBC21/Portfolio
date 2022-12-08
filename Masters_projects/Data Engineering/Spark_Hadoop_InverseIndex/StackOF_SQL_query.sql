-- The following SQL Query was used on data.stackexchange.com to obtain the data for the inverse index project

SELECT id, Tags, CreationDate FROM Posts
WHERE CreationDate LIKE '%2018%' AND Tags IS NOT NULL;

-- The first line takes the post id, Tags, and CreationDate features from the Posts table
-- The second line filters the results to posts created in 2018 and omits posts without a tag
