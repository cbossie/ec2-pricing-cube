CREATE OR REPLACE VIEW instance_pricing AS
SELECT
    i.*,
    p.*
FROM
    "instance_finder" i
LEFT OUTER JOIN
    pricing_options p ON
    p."po_key" = i."pricing key"
    