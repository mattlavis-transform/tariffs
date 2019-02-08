function makeMeasureTypeDependent() {
// Called when the user changes the value of the measure type series object
  var objMeasureTypeSeries = document.getElementById("objMeasureTypeSeries");
  var idMeasureTypeSeries = objMeasureTypeSeries.options[objMeasureTypeSeries.selectedIndex].value;
  var objMeasureType = document.getElementById("objMeasureType");
  objMeasureType.selectedIndex = 0;

// Define page sections
  var objBlockQuota         = document.getElementById("blockQuota");
  var objBlockOrigin        = document.getElementById("blockOrigin");
  var objBlockValidityDates = document.getElementById("blockValidityDates");
  var objBlockGoods         = document.getElementById("blockGoods");
  var objDuties             = document.getElementById("blockDuties");
  var objConditions         = document.getElementById("blockConditions");
  var objFootnotes          = document.getElementById("blockFootnotes");
  var objButtons            = document.getElementById("blockButtons");

  //objBlockQuota.style.display = "none";
  objBlockOrigin.style.display = "none";
  objBlockValidityDates.style.display = "none";
  objBlockGoods.style.display = "none";
  objDuties.style.display = "none";
  objConditions.style.display = "none";
  objFootnotes.style.display = "none";
  objButtons.style.display = "none";

  sKeep = "";
  switch(idMeasureTypeSeries){
    case "A":
      sKeep = "277,278,485,481";
      break;
    case "B":
      sKeep = "474,475,465,473,467,072,08,092,477,478,914,710,715,725,708,706,735,705,464,716,711,717,479,740,745,718,719,724,749,746,722,410,483,482,760,747,730,713,712,751,755,750,707,709,714,770,772,771,773,774,748,420,728";
      break;
    case "C":
      sKeep = "102,103,104,105,106,112,115,117,119,122,123,140,141,142,143,144,145,146,147,901,902,903,906,907,919";
      break;
    case "D":
      sKeep = "551,552,553,554,555,561,562,563,564,565,566,570";
      break;
    case "E":
      sKeep = "670,674,680,681,682,683,684,685,686,687,688";
      break;
    case "F":
      sKeep = "672,673";
      break;
    case "J":
      sKeep = "690,695,696";
      break;
    case "M":
      sKeep = "487,488,489,490";
      break;
    case "N":
      sKeep = "430,431,440,442,445,447,450,455,456,457,460,461,462,463,466,468,469,470,471,472";
      break;
    case "S":
      sKeep = "651,652,653,654,655,656,657,658,691";
      break;
    case "O":
      sKeep = "109,110,111";
      break;
  }
  if (sKeep != "") {
    var objSplit = sKeep.split(",");
    var iCount = objMeasureType.length;
    var iCountKeep = objSplit.length;
    for (i = 0; i < iCount; i++) {
      objMeasureType.options[i].style.display = "none";
      for (j = 0; j < iCountKeep; j++) {
        if (objMeasureType.options[i].value ==objSplit[j]) {
          objMeasureType.options[i].style.display = "block";
        }
      }
    }
  }
}

function drawPageBasedOnMeasureType() {
// Generic variables
  var objMeasureType = document.getElementById("objMeasureType");

// Define page sections
  var objBlockQuota         = document.getElementById("blockQuota");
  var objBlockOrigin        = document.getElementById("blockOrigin");
  var objBlockValidityDates = document.getElementById("blockValidityDates");
  var objBlockGoods         = document.getElementById("blockGoods");
  var objBlockDuties        = document.getElementById("blockDuties");
  var objBlockConditions    = document.getElementById("blockConditions");
  var objBlockFootnotes     = document.getElementById("blockFootnotes");
  var objBlockButtons       = document.getElementById("blockButtons");


// By default hide the quota block
  objBlockQuota.style.display = "none";

// Determine whether or not to show the quota block
  var sShowQuota = "046,122,123,143,146,147,653,654,907";
  var objSplitQuota = sShowQuota.split(",");
  var iCount = objMeasureType.length;
  var iCountQuota = objSplitQuota.length;

  objBlockQuota.style.display = "none";
  objBlockOrigin.style.display = "block";
  objBlockValidityDates.style.display = "block";
  objBlockGoods.style.display = "block";
  objBlockDuties.style.display = "none";
  objBlockConditions.style.display = "block";
  objBlockFootnotes.style.display = "block";
  objBlockButtons.style.display = "block";

  var idMeasureType = objMeasureType.options[objMeasureType.selectedIndex].value;

// Determine whether to show the quota block
  for (j = 0; j < iCountQuota; j++) {
    if (idMeasureType == objSplitQuota[j]) {
      objBlockQuota.style.display = "block";
      break;
    }
  }

// Finally, work out whether to display the duty block
  var sShowDuties = "103,105,106,112,115,117,119,122,123,141,142,143,145,146,147,489,490,552,554,562,651,652,654,695";
  var objSplitDuties = sShowDuties.split(",");
  var iCountDuties = objSplitDuties.length;

  for (j = 0; j < iCountQuota; j++) {
    if (idMeasureType == objSplitDuties[j]) {
      objBlockDuties.style.display = "block";
      break;
    }
  }


}

function geoClick(opt) {
  var geo1        = document.getElementById("geo1");
  var geo2        = document.getElementById("geo2");
  var lblGeo3     = document.getElementById("lblGeo3");
  var geo2Exclude = document.getElementById("geo2Exclude");
  var geo3Exclude = document.getElementById("geo3Exclude");

  switch (opt) {
    case 1:
      geo1.removeAttribute("disabled");
      geo2.setAttribute("disabled", "disabled");
      geo2.selectedIndex = 0;
      lblGeo3.style.color = "#666";
      geo2Exclude.style.display = "none";
      geo3Exclude.style.display = "none";
      break;
    case 2:
      geo1.setAttribute("disabled", "disabled");
      geo2.removeAttribute("disabled");
      geo1.selectedIndex = 0;
      lblGeo3.style.color = "#666";
      geo2Exclude.style.display = "block";
      geo3Exclude.style.display = "none";
      break;
    case 3:
      geo1.setAttribute("disabled", "disabled");
      geo2.setAttribute("disabled", "disabled");
      geo1.selectedIndex = 0;
      geo2.selectedIndex = 0;
      lblGeo3.style.color = "#000";
      geo2Exclude.style.display = "none";
      geo3Exclude.style.display = "block";
      break;
  }
}

function updateCommodityCode() {
  var txtCommodityCode = document.getElementById("txtCommodityCode");
  var txtCommodityCodeDescription = document.getElementById("txtCommodityCodeDescription");
  var currentText = txtCommodityCode.value;

//8711609010
//3215190020
  switch (currentText) {
    case "87":
      sText = "Vehicles other than railway or tramway rolling stock, and parts and accessories thereof";
      txtCommodityCodeDescription.innerText = sText;
      break;
    case "8711":
      sText = "Motorcycles (including mopeds) and cycles fitted with an auxiliary motor, with or without side-cars; side-cars";
      txtCommodityCodeDescription.innerText = sText;
      break;
    case "871160":
      sText = "With electric motor for propulsion";
      txtCommodityCodeDescription.innerText = sText;
      break;
    case "87116090":
      sText = "Other";
      txtCommodityCodeDescription.innerText = sText;
      break;
    case "8711609010":
      sText = "Cycles, with pedal assistance, with an auxiliary electric motor";
      txtCommodityCodeDescription.innerText = sText;
      break;

      case "32":
        sText = "TANNING OR DYEING EXTRACTS; TANNINS AND THEIR DERIVATIVES; DYES, PIGMENTS AND OTHER COLOURING MATTER; PAINTS AND VARNISHES; PUTTY AND OTHER MASTICS; INKS";
        txtCommodityCodeDescription.innerText = sText;
        break;

      case "3215":
        sText = "Printing ink, writing or drawing ink and other inks, whether or not concentrated or solid";
        txtCommodityCodeDescription.innerText = sText;
        break;

      case "321519":
        sText = "Other";
        txtCommodityCodeDescription.innerText = sText;
        break;

      case "32151900":
        sText = "Other";
        txtCommodityCodeDescription.innerText = sText;
        break;

      case "3215190020":
        sText = "Ink: -|consisting of a polyester polymer and a dispersion of silver (CAS RN 7440-22-4) and silver chloride (CAS RN 7783-90-6)|in methyl propyl ketone (CAS RN 107-87-9), -|with a total solid content by weight of 55|% or more, but not more than 57|%, and -|with a specific gravity of 1,40|g/cm$3|or more, but not more than 1,60|g/cm$3, used to imprint electrodes";
        txtCommodityCodeDescription.innerText = sText;
        break;

    case "":
      sText = "Code description will appear here once you enter an additional code above.";
      txtCommodityCodeDescription.value = sText;
      break;
  }
}

function updateAdditionalCode() {
  var txtCommodityCode = document.getElementById("txtCommodityCode");
  var txtCommodityCodeDescription = document.getElementById("txtCommodityCodeDescription");
  var currentText = txtAdditionalCode.value;
  //alert (currentText);
//8711609010
  switch (currentText) {
    case "2551":
      sText = "Imported by sea and arriving via the Atlantic Ocean or the Suezcanal with the port of unloading on the Mediterranean Sea";
      txtAdditionalCodeDescription.innerText = sText;
      break;
    case "7027":
      sText = "Milk fat >= 0 < 1.5 % by weight\nStarch/Glucose >= 5 < 25 % by weight\nMilk proteins >= 2.5 < 6 % by weight\nSucrose/Invert sugar/Isoglucose >= 30 < 50 % by weight";
      txtAdditionalCodeDescription.innerText = sText;
      break;
  }
}

function showConditions() {
  var optConditionCode = document.getElementById("optConditionCode");
  var idConditionCode = optConditionCode.options[optConditionCode.selectedIndex].value;
  switch (idConditionCode) {
    case "A":
    case "I":
    case "Q":
    case "Z":
      showConditionsCertificates();
      showConditionsCertificateActions();

      hideConditionsCertificateTypes();
      hideConditionsMaxQuantity();
      hideConditionsMinQuantity();
      hideConditionsMinPrice();
      hideConditionsReferencePrice();
      hideConditionsMaxPrice();
      hideConditionsRatio();
      hideConditionsEntryPrice();
      hideConditionsActionsGeneric();

      document.getElementById('txtCertificate').focus();
      break;
    case "B":
    case "C":
    case "E3":
    case "H":
    case "I3":
      showConditionsCertificateTypes();
      showConditionsCertificates();
      showConditionsCertificateActions();

      hideConditionsMaxQuantity();
      hideConditionsMinQuantity();
      hideConditionsMinPrice();
      hideConditionsReferencePrice();
      hideConditionsMaxPrice();
      hideConditionsRatio();
      hideConditionsEntryPrice();
      hideConditionsActionsGeneric();

      document.getElementById('optConditionActionCertificateType').focus();
      break;
    case "D":
      showConditionsActionsGeneric();

      hideConditionsCertificateTypes();
      hideConditionsCertificates();
      hideConditionsCertificateActions();
      hideConditionsMaxQuantity();
      hideConditionsReferencePrice();
      hideConditionsRatio();

      document.getElementById('optConditionActionGeneric').focus();
      break;
    case "E1":
    case "I1":
      showConditionsMaxQuantity();
      showConditionsActionsGeneric();

      hideConditionsCertificateTypes();
      hideConditionsCertificates();
      hideConditionsCertificateActions();
      hideConditionsMinQuantity();
      hideConditionsMinPrice();
      hideConditionsReferencePrice();
      hideConditionsMaxPrice();
      hideConditionsRatio();
      hideConditionsEntryPrice();

      document.getElementById('txtMaximumQuantity').focus();
      break;
    case "E2":
    case "I2":
      showConditionsMaxPrice();
      showConditionsActionsGeneric();

      hideConditionsCertificateTypes();
      hideConditionsCertificates();
      hideConditionsCertificateActions();
      hideConditionsMaxQuantity();
      hideConditionsMinQuantity();
      hideConditionsMinPrice();
      hideConditionsReferencePrice();
      hideConditionsRatio();
      hideConditionsEntryPrice();

      document.getElementById('txtMaximumPricePerUnit').focus();
      break;
    case "F":
    case "G":
    case "L":
    case "M1":
    case "N":
      showConditionsMinPrice();
      showConditionsActionsGeneric();

      hideConditionsCertificateTypes();
      hideConditionsCertificates();
      hideConditionsCertificateActions();
      hideConditionsMaxQuantity();
      hideConditionsMinQuantity();
      hideConditionsReferencePrice();
      hideConditionsMaxPrice();
      hideConditionsRatio();
      hideConditionsEntryPrice();

      document.getElementById('txtMinimumPricePerUnit').focus();
      break;
    case "M2":
      showConditionsReferencePrice();
      showConditionsActionsGeneric();

      hideConditionsCertificateTypes();
      hideConditionsCertificates();
      hideConditionsCertificateActions();
      hideConditionsMaxQuantity();
      hideConditionsMinQuantity();
      hideConditionsMinPrice();
      hideConditionsMaxPrice();
      hideConditionsRatio();
      hideConditionsEntryPrice();

      document.getElementById('txtMinimumPricePerUnit').focus();
      break;
    case "R":
    case "U":
      showConditionsRatio();

      hideConditionsCertificateTypes();
      hideConditionsCertificates();
      hideConditionsCertificateActions();
      hideConditionsMaxQuantity();
      hideConditionsMinQuantity();
      hideConditionsMinPrice();
      hideConditionsReferencePrice();
      hideConditionsMaxPrice();
      hideConditionsEntryPrice();
      hideConditionsActionsGeneric();
      break;
    case "V":
      showConditionsEntryPrice();
      showConditionsActionsGeneric();

      hideConditionsCertificateTypes();
      hideConditionsCertificates();
      hideConditionsCertificateActions();
      hideConditionsMaxQuantity();
      hideConditionsMinQuantity();
      hideConditionsMinPrice();
      hideConditionsReferencePrice();
      hideConditionsMaxPrice();
      hideConditionsRatio();

      break;
    default:
      hideConditionsCertificateTypes();
      hideConditionsCertificates();
      hideConditionsCertificateActions();
      hideConditionsMaxQuantity();
      hideConditionsMinQuantity();
      hideConditionsMinPrice();
      hideConditionsReferencePrice();
      hideConditionsMaxPrice();
      hideConditionsRatio();
      hideConditionsEntryPrice();
      hideConditionsActionsGeneric();

      break;
  }

}

function showConditionsCertificateTypes() {
  var objConditionCertificateType = document.getElementById("objConditionCertificateType");
  objConditionCertificateType.style.display = "block";
}

function hideConditionsCertificateTypes() {
  var objConditionCertificateType = document.getElementById("objConditionCertificateType");
  objConditionCertificateType.style.display = "none";
}

function showConditionsCertificates() {
  var objConditionCertificate = document.getElementById("objConditionCertificate");
  objConditionCertificate.style.display = "block";
}

function hideConditionsCertificates() {
  var objConditionCertificate = document.getElementById("objConditionCertificate");
  objConditionCertificate.style.display = "none";
}

function showConditionsCertificateActions() {
  var objConditionActionCertificate = document.getElementById("objConditionActionCertificate");
  objConditionActionCertificate.style.display = "block";
}

function hideConditionsCertificateActions() {
  var objConditionActionCertificate = document.getElementById("objConditionActionCertificate");
  objConditionActionCertificate.style.display = "none";
}

function showConditionsMaxQuantity() {
  var objConditionMaxQuantity = document.getElementById("objConditionMaxQuantity");
  objConditionMaxQuantity.style.display = "block";
}

function hideConditionsMaxQuantity() {
  var objConditionMaxQuantity = document.getElementById("objConditionMaxQuantity");
  objConditionMaxQuantity.style.display = "none";
}

function showConditionsMinQuantity() {
  var objConditionMinQuantity = document.getElementById("objConditionMinQuantity");
  objConditionMinQuantity.style.display = "block";
}

function hideConditionsMinQuantity() {
  var objConditionMinQuantity = document.getElementById("objConditionMinQuantity");
  objConditionMinQuantity.style.display = "none";
}

function showConditionsMinPrice() {
  var objConditionMinPrice = document.getElementById("objConditionMinPrice");
  objConditionMinPrice.style.display = "block";
}

function hideConditionsMinPrice() {
  var objConditionMinPrice = document.getElementById("objConditionMinPrice");
  objConditionMinPrice.style.display = "none";
}

function showConditionsReferencePrice() {
  var objConditionReferencePrice = document.getElementById("objConditionReferencePrice");
  objConditionReferencePrice.style.display = "block";
}

function hideConditionsReferencePrice() {
  var objConditionReferencePrice = document.getElementById("objConditionReferencePrice");
  objConditionReferencePrice.style.display = "none";
}

function showConditionsMaxPrice() {
  var objConditionMaxPrice = document.getElementById("objConditionMaxPrice");
  objConditionMaxPrice.style.display = "block";
}

function hideConditionsMaxPrice() {
  var objConditionMaxPrice = document.getElementById("objConditionMaxPrice");
  objConditionMaxPrice.style.display = "none";
}

function showConditionsRatio() {
  var objConditionRatio = document.getElementById("objConditionRatio");
  objConditionRatio.style.display = "block";
}

function hideConditionsRatio() {
  var objConditionRatio = document.getElementById("objConditionRatio");
  objConditionRatio.style.display = "none";
}

function showConditionsEntryPrice() {
  var objConditionEntryPrice = document.getElementById("objConditionEntryPrice");
  objConditionEntryPrice.style.display = "block";
}

function hideConditionsEntryPrice() {
  var objConditionEntryPrice = document.getElementById("objConditionEntryPrice");
  objConditionEntryPrice.style.display = "none";
}

function showConditionsActionsGeneric() {
  var objConditionActionGeneric = document.getElementById("objConditionActionGeneric");
  objConditionActionGeneric.style.display = "block";
}

function hideConditionsActionsGeneric() {
  var objConditionActionGeneric = document.getElementById("objConditionActionGeneric");
  objConditionActionGeneric.style.display = "none";
}

function showDutyExpressions() {
  var optDutyExpression = document.getElementById("optDutyExpression");
  var idDutyExpression = optDutyExpression.options[optDutyExpression.selectedIndex].value;

  var txtDutyExpression2 = document.getElementById("txtDutyExpression2");

  switch (idDutyExpression) {
    case "01":
    case "04":
    case "22":
    case "23":
      showDutyExpression2("Duty amount (%)");
      hideUnits();
      break;
    case "01b":
    case "04b":
    case "06":
    case "07":
    case "09":
    case "11":
    case "12":
    case "13":
    case "14":
    case "21":
    case "25":
    case "27":
    case "29":
    case "31":
    case "33":
      showDutyExpression2("Duty amount (€)");
      showUnits();
      break;
    case "40":
    case "41":
    case "42":
    case "43":
    case "44":
      showDutyExpression2("Refund amount (€)");
      showUnits();
      break;
    case "15":
      showDutyExpression2("Duty amount (at least €)");
      showUnits();
      break;
    case "17":
      showDutyExpression2("Duty amount (not more than €)");
      showUnits();
      break;
    case "02b":
      showDutyExpression2("Duty amount (-€)");
      showUnits();
      break;
    case "02":
    case "36":
      showDutyExpression2("Duty amount (-%)");
      hideUnits();
      break;
    case "23":
      showDutyExpression2("");
      hideUnits();
      break;
    default:
      a = 1;
  }
}

function showDutyExpression2(sLabel) {
  var lblDutyExpression2 = document.getElementById("lblDutyExpression2");
  var panelDutyExpression2 = document.getElementById("panelDutyExpression2");
  panelDutyExpression2.style.display = "block";
  lblDutyExpression2.innerText = sLabel;
}

function showUnits() {
  var panelPer = document.getElementById("panelPer");
  var panelMeasurementUnit = document.getElementById("panelMeasurementUnit");
  var panelMeasurementUnitQualifier = document.getElementById("panelMeasurementUnitQualifier");
  panelPer.style.display = "block";
  panelMeasurementUnit.style.display = "block";
  panelMeasurementUnitQualifier.style.display = "block";
}

function hideUnits() {
  //alert ("joijji");
  var panelPer = document.getElementById("panelPer");
  var panelMeasurementUnit = document.getElementById("panelMeasurementUnit");
  var panelMeasurementUnitQualifier = document.getElementById("panelMeasurementUnitQualifier");
  panelPer.style.display = "none";
  panelMeasurementUnit.style.display = "none";
  panelMeasurementUnitQualifier.style.display = "none";
}

function selectQuotaPeriodOptions() {
  var objQuotaPeriod = document.getElementById("quotaperiod");
  var idQuotaPeriod = objQuotaPeriod.options[objQuotaPeriod.selectedIndex].value;
  switch (idQuotaPeriod) {
    case "1":
      sShowQuotaPeriodAnnual();
      break;
    case "2":
      sShowQuotaPeriodBiannual();
      break;
    case "3":
      sShowQuotaPeriodQuarterly();
      break;
    case "4":
      sShowQuotaPeriodMonthly();
      break;
    default:
    sShowQuotaPeriodAnnual();
    break;
  }
}

function sShowQuotaPeriodAnnual() {
  document.getElementById("quotaBalanceAnnual").style.display = "block";
  document.getElementById("quotaBalanceBiannual").style.display = "none";
  document.getElementById("quotaBalanceQuarterly").style.display = "none";
  document.getElementById("quotaBalanceMonthly").style.display = "none";
  document.getElementById("quotaBalanceMeasurementUnits").style.display = "none";
}

function sShowQuotaPeriodBiannual() {
  document.getElementById("quotaBalanceAnnual").style.display = "none";
  document.getElementById("quotaBalanceBiannual").style.display = "block";
  document.getElementById("quotaBalanceQuarterly").style.display = "none";
  document.getElementById("quotaBalanceMonthly").style.display = "none";
  document.getElementById("quotaBalanceMeasurementUnits").style.display = "block";
}
function sShowQuotaPeriodQuarterly() {
  document.getElementById("quotaBalanceAnnual").style.display = "none";
  document.getElementById("quotaBalanceBiannual").style.display = "none";
  document.getElementById("quotaBalanceQuarterly").style.display = "block";
  document.getElementById("quotaBalanceMonthly").style.display = "none";
  document.getElementById("quotaBalanceMeasurementUnits").style.display = "block";
}
function sShowQuotaPeriodMonthly() {
  document.getElementById("quotaBalanceAnnual").style.display = "none";
  document.getElementById("quotaBalanceBiannual").style.display = "none";
  document.getElementById("quotaBalanceQuarterly").style.display = "none";
  document.getElementById("quotaBalanceMonthly").style.display = "block";
  document.getElementById("quotaBalanceMeasurementUnits").style.display = "block";
}
