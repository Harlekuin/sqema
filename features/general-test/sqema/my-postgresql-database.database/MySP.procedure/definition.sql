DO
'<<first_block>>
DECLARE
  counter integer := 0;
BEGIN

    counter := counter + 1;
    RAISE NOTICE ''The current value of counter is %'', counter;

END first_block';