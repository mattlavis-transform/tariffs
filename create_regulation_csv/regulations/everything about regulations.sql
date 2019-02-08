-- ###############################################
-- Fully characterise a regulation
-- ###############################################

-- Get a regulation
SELECT v5.measure_sid, v5.regulation_id, v5.goods_nomenclature_item_id, v5.additional_code_type_id, v5.additional_code_id, v5.measure_type_id, v5.geographical_area_id, v5.validity_start_date, v5.validity_end_date, v5.ordernumber,
mtd.description as measure_type_description, ga.description as geographical_area_description
FROM v5, measure_type_descriptions mtd, ml_geographical_areas ga
WHERE regulation_id = 'R120978'
AND v5.measure_type_id = mtd.measure_type_id
AND v5.geographical_area_id = ga.geographical_area_id
LIMIT 10;

-- Get its measure components
SELECT mc.*, de.description as duty_expression_description, mucd.description as mucd_description
FROM duty_expression_descriptions de, measure_components mc LEFT OUTER JOIN measurement_unit_qualifier_descriptions mucd ON mc.measurement_unit_qualifier_code = mucd.measurement_unit_qualifier_code
WHERE measure_sid IN (SELECT measure_sid FROM v5 WHERE regulation_id = 'R120978')
AND mc.duty_expression_id = de.duty_expression_id
ORDER BY measure_sid, duty_expression_id
LIMIT 10;

-- Get its footnotes
SELECT fam.measure_sid, fam.footnote_type_id, fam.footnote_id, f.description FROM footnote_association_measures fam, ml_footnotes f
WHERE f.footnote_id = fam.footnote_id
AND f.footnote_type_id = fam.footnote_type_id
AND fam.measure_sid IN (SELECT measure_sid FROM v5 WHERE regulation_id = 'R120978')
ORDER BY fam.measure_sid, fam.footnote_type_id, fam.footnote_id



-- Get its conditions & condition components
SELECT mc.measure_sid, mc.measure_condition_sid, mc.condition_code, mc.condition_duty_amount, 
mc.condition_measurement_unit_code, mc.condition_measurement_unit_qualifier_code, mc.action_code, mc.certificate_type_code, mc.certificate_code,
mcc.duty_expression_id, mcc.duty_amount, mcc.monetary_unit_code, mcc.measurement_unit_code, measurement_unit_qualifier_code,
mccd.description as condition_code_description, mad.description as action_code_description, cc.description as certificate_description
FROM 
measure_action_descriptions mad, measure_condition_code_descriptions mccd, ml_certificate_codes cc
RIGHT OUTER JOIN measure_conditions mc ON cc.certificate_code = mc.certificate_code AND cc.certificate_type_code = mc.certificate_type_code
LEFT OUTER JOIN measure_condition_components mcc ON mc.measure_condition_sid = mcc.measure_condition_sid
WHERE mccd.condition_code = mc.condition_code
AND mad.action_code = mc.action_code
AND mc.measure_sid IN (SELECT measure_sid FROM v5 WHERE regulation_id = 'R120978')
ORDER BY mc.measure_sid, mc.component_sequence_number, mcc.duty_expression_id
LIMIT 10

-- Get its conditions only
SELECT mc.measure_sid, mc.measure_condition_sid, mc.condition_code, mc.condition_duty_amount, 
mc.condition_measurement_unit_code, mc.condition_measurement_unit_qualifier_code, mc.action_code, mc.certificate_type_code, mc.certificate_code,
mccd.description as condition_code_description, mad.description as action_code_description, cc.description as certificate_description
FROM 
measure_action_descriptions mad, measure_condition_code_descriptions mccd, ml_certificate_codes cc
RIGHT OUTER JOIN measure_conditions mc ON cc.certificate_code = mc.certificate_code AND cc.certificate_type_code = mc.certificate_type_code
WHERE mccd.condition_code = mc.condition_code
AND mad.action_code = mc.action_code
AND mc.measure_sid IN (SELECT measure_sid FROM v5 WHERE regulation_id = 'R120978')
ORDER BY mc.measure_sid, mc.component_sequence_number
LIMIT 10



-- Get its condition components
SELECT mc.measure_sid, mcc.measure_condition_sid, mcc.duty_expression_id, mcc.duty_amount, mcc.monetary_unit_code, mcc.measurement_unit_qualifier_code
FROM measure_conditions mc, measure_condition_components mcc
WHERE mc.measure_condition_sid = mcc.measure_condition_sid 
AND mc.measure_sid IN (SELECT measure_sid FROM v5 WHERE regulation_id = 'R120978')
ORDER BY 1, 2, 3
LIMIT 10;

SELECT * FROM measure_components WHERE measure_sid = 3330034


SELECT * FROM measurement_unit_qualifiers

SELECT DISTINCT condition_code FROM measure_conditions