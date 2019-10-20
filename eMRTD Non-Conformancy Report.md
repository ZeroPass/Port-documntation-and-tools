# eMRTD non-conformancy report

## Abstract
Although the ICAO 9303 allows general deviations from the standard conformance (see part 3 page 3) we found most is not being followed as defined by the standard. What's more, it was hard to find what the exact deviation was (for example serialization of master list’s signed attributes) because either there was deviation list but it didn’t specify particular deviation or in most cases, there was no documentation to be found. This document summers up our findings based on [ICAO PKD](https://pkddownloadsg.icao.int/download), [German PKI](https://www.bsi.bund.de/EN/Topics/ElectrIDDocuments/securPKI/securCSCA/Root_Certificate/cscaGermany_node.html#doc6650358bodyText4) and 1 Slovenian ePassport. For ICAO PKD, the examination was done on the collection of master lists version *127*, the collections of DSCs & CRLs version *3846* and the collections of non-conformant DSCs & CRLs version *53*. Examination of German PKI was done on master list: *20190925_DEMasterList.ml* and deviation list: *20181106_DEDeviationList.dvl*. For Slovenian passport the data is not publically available.

## CSCA Master List
Examined master lists were from countries: Botswana, Canada, France, Germany, Hungary, Moldova, Spain, Switzerland, Ukraine.

The inspection of master lists showed that signed attributes field stored in the master list is serialized differently than what was used to generate digital signature with. See the issue [#1](https://github.com/ZeroPass/PassID-Server/issues/1#issuecomment-536134037) in PassID server repo. This was true for every master list found in ICAO PKD and German PKI. Additionally, the signature verification of Hungarian master list failed and we could not find the reason why. There was also a problem with verifying integrity of the Portuguese CSCA (ser no.: *71c4aa41ac126d13*) because no issuing CSCA was found within any of the master lists.

 
## CSCA, DSC, CRL
The conformance test of eMRTD PKI found that most of issued certificates and CRLs don’t strictly follow the ICAO 9303 standard. The conformance verification was done according to the specification of part 12, section 7.1 (Certificate profiles) and section 7.2 (CRL profile). The most common issue was with missing required fields or fields having wrong values. Some of missing fields were: *Subject Key Identifier*, *Authority Key Identifier*, *Basic Constraints*, *Key Usage*. Most of wrongly set values were found if these fields: *Basic Constraints* (path length of CSCA was not set to 0) and *Key Usage* (for example: CACA missing Certificate signing field or having instead set field Digital signature). 
We also found that some certificates do not follow the recommended validity period (For CSCA 15 years, for DSC 10 years and for CRL 3 months). There was also a case where more CSCAs were issued with the same subject and public key but different validity period. Example of this are Slovenian LCSCA ser no.: *448831f3* and CSCA ser no.: *448831f1*.
What it is interesting with all this is that all non-conforming certificates and CRLs were not found in deviation list but in general issued collection list (ldif) or master list.

*Note: Due to many non-conformant eMRTD PKI elements the implementation of PassID will not verify the standard conformancy. Only verification of digital signature and validity period will be performed.* 
 
## Deviation list
The examination was done on deviation list publically available at ICAO PKD and on German deviation list version 20181106. The inspection of deviation list at the ICAO PKD showed that it doesn’t store lists according to the doc 9303 part 12 section 7 but only a list of CSCA, DSC and CRL in ldif format. This list doesn’t contain information on deviation of eMRTD IC & MRZ. List also contains header for each non-conforming certificate and CRL with explanation what the problem is. This information is not digitally signed. After further examination of German deviation list we found that ICAO’s deviation list is just a list of non-conforming PKI elements extracted from a deviation list file specified in doc 9303 part 12 section 7. One interesting find was that deviation list can include confusing information like describing problem for non-conforming CSCA of an actual DSC certificate. One such example of DSC specified in deviaton list as non-conforming CSCA is Chinese DSC ser no.: *5a*.


## Non-conformant eMRTD elements of IC
After extracting data (ef.COM, ef.SOD, ef.dg15) from 1 Slovenian passport no issue was found.


## [EU eMRTD Interoperability Test 2017](https://ec.europa.eu/jrc/en/publication/eu-emrtd-interoperability-test-2017-final-report)
There were 18.135 passports tested from the EU and outside the EU.

**Most relevant results for PassID;**
* Only 28% CSCA certificates follows the standard completly
* DSA for CSCA: 
  *	RSA 64%
  * ECDSA 36%
* DSA for DSC: 
  * RSA PKCS#1 v1.5 53% 
  * RSA SSA PSS 10%  
  * ECDSA 37% with sha256 70%

**Active Authentication (AA):**
* 63% of samples had AA enabled
  * 68% used RSA for DSA
  * 32% ECDSA for DSA
* with RSA  the used algoritm was
  *	71% SHA-1
  * ~18% SHA-256 
  *	11% unknown   
* with ECDSA the used algoritm was 
  * SHA-1 25% 
  * SHA-224 12.5% 
  * SHA-256 37% 
  * SHA-384 25%

#### Algoritms missing from EOSIO WASM intrinsics
SHA-224, SHA-384, RSA
