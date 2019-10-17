# EOSIO PassID

 *On-chain ePassport Active Authentication*  
  
## Biometric passport

It has an embedded electronic microprocessor chip that contains biometric information that can be used to authenticate the identity of the passport holder. It can also be used to sign arbitrary data. The standard called electronic machine-readable travel document or eMRTD, is standardized by the ICAO, Document 9303 (ISO/IEC 7501-1).

  

ePassport validation does not require any exchange of the personal data of passport holders.![](https://lh4.googleusercontent.com/eKFrbZYjCDuYA1vLi9fFMc2wYtEDEKN5lfsrbFv3A3DE4n7eVqm15Ku8fx5kL4usihqv4IOPwchwKX5sl-ehW5Bwplbt0qk8-gQ4TjWZhpKUP9BLc-HM8xTkoeDRM8Dt1U4-g9-q)

Look for the Biometric Passport chip sign

## ICAO PKD

ICAO Public Key Directory is a global initiative and deployment of Trust Chain used to issue passports.  
List of participant countries who [publish their Biometric Passport certificates public](https://www.icao.int/Security/FAL/PKD/Pages/ICAO-PKDParticipants.aspx);

![Biometric Passport](https://github.com/ZeroPass/PassID-documntation-and-tools/blob/master/images/biometric_passport.png?raw=true)

The yellow ones (non-participants) can usually be found in the Master List as well, but their revocation lists and DSC lists would have to be downloaded and uploaded from the location they provide.  
  
We need to further investigate what is happening with countries in white, but we have to assume they are not supported yet.

# Goals

This project aims to;

1.  Provide Android and iOS apps for the end-user to attest their eosio based accounts; Verify the signature in the eosio software (on-chain, in WASM);    
2.  Provide a fully verified path from: 
  1.  Master List Signer (uploads the self- signed lists of other CSCA certificates) 
  2.  CSCA (each country has one)    
  3.  DSC (each country issues multiple, renews them every 3 months or after signing 100k documents)    
  4.  Revocation lists    
  5.  Passport public key    
  6.  All passport data
 3.  Partial disclosure (pre-authenticated). Useful for actual KYC and/or for challenging people with multiple passports and as another factor used for recovery.
