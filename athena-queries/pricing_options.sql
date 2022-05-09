CREATE OR REPLACE VIEW pricing_options AS
SELECT
    pc.pricingkey AS po_key,
    reduce(pc.hrc['OnDemand'], 0.0, (s,x) -> x, s -> s)  "On Demand Hourly",
    reduce(pc.hrc['OnDemand'], 0.0, (s,x) -> x * 24 * 30.5, s -> s)  "On Demand Monthly",
    reduce(pc.hrc['OnDemand'], 0.0, (s,x) -> x * 24 * 30.5 * 12, s -> s)  "On Demand One Year",
    reduce(pc.hrc['OnDemand'], 0.0, (s,x) -> x * 24 * 30.5 * 12 * 3, s -> s)  "On Demand Three Year",

    -- Standard
    reduce(pc.oyc['1yr Std All Upfront'], 0.0, (s,x) -> x, s -> s) AS "1yr Std All Upfront One Year",
    reduce(pc.tyc['1yr Std All Upfront'], 0.0, (s,x) -> x, s -> s) AS "1yr Std All Upfront Three Year",
    reduce(pc.oyc['3yr Std All Upfront'], 0.0, (s,x) -> x, s -> s) AS "3yr Std All Upfront One Year",
    reduce(pc.tyc['3yr Std All Upfront'], 0.0, (s,x) -> x, s -> s) AS "3yr Std All Upfront Three Year",
    reduce(pc.oyc['1yr Std No Upfront'], 0.0, (s,x) -> x, s -> s) AS "1yr Std No Upfront One Year",
    reduce(pc.tyc['1yr Std No Upfront'], 0.0, (s,x) -> x, s -> s) AS "1yr Std No Upfront Three Year",
    reduce(pc.oyc['3yr Std No Upfront'], 0.0, (s,x) -> x, s -> s) AS "3yr Std No Upfront One Year",
    reduce(pc.tyc['3yr Std No Upfront'], 0.0, (s,x) -> x, s -> s) AS "3yr Std No Upfront Three Year",
    reduce(pc.oyc['1yr Std Partial Upfront'], 0.0, (s,x) -> s + x, s -> s) AS "1yr Std Partial Upfront One Year",
    reduce(pc.tyc['1yr Std Partial Upfront'], 0.0, (s,x) -> s + x, s -> s) AS "1yr Std Partial Upfront Three Year",
    reduce(pc.oyc['3yr Std Partial Upfront'], 0.0, (s,x) -> s + x, s -> s) AS "3yr Std Partial Upfront One Year",
    reduce(pc.tyc['3yr Std Partial Upfront'], 0.0, (s,x) -> s + x, s -> s) AS "3yr Std Partial Upfront Three Year",

    -- Convertible
    reduce(pc.oyc['1yr Cnvt All Upfront'], 0.0, (s,x) -> x, s -> s) AS "1yr Cnvt All Upfront One Year",
    reduce(pc.tyc['1yr Cnvt All Upfront'], 0.0, (s,x) -> x, s -> s) AS "1yr Cnvt All Upfront Three Year",
    reduce(pc.oyc['3yr Cnvt All Upfront'], 0.0, (s,x) -> x, s -> s) AS "3yr Cnvt All Upfront One Year",
    reduce(pc.tyc['3yr Cnvt All Upfront'], 0.0, (s,x) -> x, s -> s) AS "3yr Cnvt All Upfront Three Year"
FROM (


SELECT
    pcf.pricingkey,
    multimap_agg("leaseandpurchase", "hourfactor") hrc,
    multimap_agg("leaseandpurchase", "oneyearcost") oyc,
    multimap_agg("leaseandpurchase", "threeyearcost") tyc
FROM
    pricing_cube_final pcf
GROUP BY
    pcf.pricingkey
) pc