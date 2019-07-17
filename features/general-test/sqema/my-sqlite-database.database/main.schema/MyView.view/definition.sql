CREATE VIEW [main].[MyView](FirstName, HalfAge) AS
SELECT FirstName, Age / 2.0 as HalfAge
FROM [main].[MyTable]

