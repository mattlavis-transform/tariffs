-- Get distinct quota order numbers that start before EU Exit and finish after EU Exit - these will need to be end-dated and then restarted after EU exit, including with new measures
SELECT DISTINCT quota_order_number_id
FROM quota_definitions
WHERE validity_start_date < '2019-03-29' AND validity_end_date > '2019-03-29' ORDER BY 1

-- Get all quota definitions that start before EU Exit and finish after EU Exit - these will need to be end-dated and then restarted after EU exit, including with new measures
SELECT quota_definition_sid, quota_order_number_id, validity_start_date, validity_end_date, quota_order_number_sid,
volume, initial_volume, monetary_unit_code, measurement_unit_code, measurement_unit_qualifier_code, maximum_precision, critical_state, critical_threshold, description
FROM quota_definitions
WHERE validity_start_date < '2019-03-29' AND validity_end_date > '2019-03-29'

-- Get all quota definitions that start after EU Exit - these will need to be deleted
SELECT quota_definition_sid, quota_order_number_id, validity_start_date, validity_end_date, quota_order_number_sid,
volume, initial_volume, monetary_unit_code, measurement_unit_code, measurement_unit_qualifier_code, maximum_precision, critical_state, critical_threshold, description
FROM quota_definitions
WHERE validity_start_date > '2019-03-29'

-- Get all measures related to quotas that start before EU Exit and end after EU Exit - these all need end-dating on EU Exit date
SELECT measure_sid, measure_type_id, geographical_area_id, goods_nomenclature_item_id, validity_start_date, validity_end_date, measure_generating_regulation_role, measure_generating_regulation_id, justification_regulation_role, justification_regulation_id, stopped_flag, geographical_area_sid, goods_nomenclature_sid, ordernumber, additional_code_type_id, additional_code_id, additional_code_sid, reduction_indicator, export_refund_nomenclature_sid
FROM measures WHERE ordernumber IS NOT NULL
AND national IS NULL AND (validity_end_date > '2019-03-29' AND validity_start_date < '2019-03-29')
ORDER BY 1

-- Get all measures related to quotas that start before EU Exit and end after EU Exit - these all need deleting
SELECT measure_sid, measure_type_id, geographical_area_id, goods_nomenclature_item_id, validity_start_date, validity_end_date, measure_generating_regulation_role, measure_generating_regulation_id, justification_regulation_role, justification_regulation_id, stopped_flag, geographical_area_sid, goods_nomenclature_sid, ordernumber, additional_code_type_id, additional_code_id, additional_code_sid, reduction_indicator, export_refund_nomenclature_sid
FROM measures WHERE ordernumber IS NOT NULL
AND national IS NULL AND validity_start_date >= '2019-03-29'
ORDER BY 1

SELECT ordernumber, geographical_area_id, goods_nomenclature_item_id FROM measures WHERE ordernumber IN ('090043', '090052');
