## MRTD document types
The cocument type identifies the type of MRTD document e.g. type beginning with capital letter 'P' marks a machine readable passport (MRP), capital letter 'I' ussualy marks electronic identification card etc... The document type is found in machine readable zone (MRZ), visual inspection zone (VIZ) and in document signer certificate (DSC) issued after 2015 in the certificate extension section indentified by OID=2.23.136.1.1.6.2.

**Doc types:**
  - 'P' - passport
    'Px' - passport document with sub type 'x' where x can be any uppercase letter
  - 'AR' - probably Residence Permit Document. It's probably not a passport.
  - 'AC' - Crew  Member  Certificate – CMC, specified in doc ICAO 9303-p5 Appendix C to Part 5
  - 'CR' - Residence Card Document. It's probably not a passport.
  - 'I', 'ID' - National ID Card Document. It's probably not a passport.
    'IR' - probably also ID Card. French DSC certificates contains this.
    'Ix' - probably national identity card where x is sub type
    'IX' - found in Spanish DSC certificate.
           Also found found in Bulgarian DSC, ser. no.: 78f0bfccfdd923c8 ;  OU = Electronic PassportsCN = DocSigner-R 044
           not verified if valid passport signed or only identity card signer.
  - 'KR' - Found in South Korean DSC certificates issued in august 2020. Example DSC cert ser. no.: 0147.
           From wikipedia South Korea is issuing new version of biometric passport starting in June 2020. First issued passports are
           for diplomatic and official passports holders and in December 2020 for those holding an ordinary passport.
           It's possible that this type indicates Machine Readable Official Travel Documents MROTDs and not machine readable passport MRP.
           Wiki ref.: https://en.wikipedia.org/wiki/Republic_of_Korea_passport#New_passport_issued_from_2020
  - 'MA' - unknown, found in chinese DSC certificate from issuer CN = China Passport Country Signing Certificate (Macao) DSC ser. no: 69, 6b, 6d, 6f, 71, 73, 75
           Could be special passport like or identity document issued by Macao special administrative region to residents of Macao.
           Note: Citizens of Macao can hold Macao passport and other national passports such as Chinese or Portuguese (info was briefly verified)
  - 'V','Vx' - Probably machine readable visa. Where x it's optional additional 1 capital letter