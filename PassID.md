# PassID

 *ePassport Active Authentication*  
  
## Biometric passport

It has an embedded electronic microprocessor chip that contains biometric information that can be used to authenticate the identity of the passport holder. It can also be used to sign arbitrary data. The standard called electronic machine-readable travel document or eMRTD, is standardized by the ICAO, Document 9303 (ISO/IEC 7501-1).

  

ePassport validation does not require any exchange of the personal data of passport holders.![Biometric Passport](https://github.com/ZeroPass/PassID-documntation-and-tools/blob/master/images/biometric_passport.png?raw=true)

Look for the Biometric Passport chip sign

## ICAO PKD

ICAO Public Key Directory is a global initiative and deployment of Trust Chain used to issue passports.  
List of participant countries who [publish their Biometric Passport certificates public](https://www.icao.int/Security/FAL/PKD/Pages/ICAO-PKDParticipants.aspx);

![Biometric Passport Countries](https://github.com/ZeroPass/PassID-documntation-and-tools/blob/master/images/Biometric_passports_countries.png?raw=true)

The yellow ones (non-participants) can usually be found in the Master List as well, but their revocation lists and DSC lists would have to be downloaded and uploaded from the location they provide.  
  
We need to further investigate what is happening with countries in white, but we have to assume they are not supported yet.

# Goals


1.  Provide Android and iOS apps for the end-user to attest their accounts; Verify the signatures in the server-side software;    
2.  Provide a fully verified path from: 
    1.  Master List Signer (uploads the self- signed lists of other CSCA certificates) 
    2.  CSCA (each country has one)    
    3.  DSC (each country issues multiple, renews them every 3 months or after signing 100k documents)    
    4.  Revocation lists    
    5.  Passport public key    
    6.  All passport data
 3.  Partial disclosure (pre-authenticated). Useful for actual KYC and/or for challenging people with multiple passports and as another factor used for recovery.
    

  

# Delivered
  
1. PassID Android app. 
2. PassID iOS app (after iOS13). 
3. PassID Web Portal- for parsing and uploading Master Lists, DSC lists and revocation lists and viewing partial disclosure data.
4. Trust Chain verification.
5. Verify Passport signatures.
6. Further research to cover more and more edge/future cases. 

  

## EOSIO PassID Mobile Apps
  
 

1.  BAC works, but it's very insecure and would be deprecated soon. We need to implement [SAC](https://en.wikipedia.org/wiki/Supplemental_access_control).  
           
    
2.  People are able to input any account and sign its hash - this means you can use untrusted devices to sign. If the device app switches the account, you would be able to use your passport again on another device to revoke.  
      
    
3.  Four times RSA signatures for full verification. 

4. Implemented  
  1. RSA-SSA PKCS v1.5 and RSA ISO 9796-2-DSS
  2. RSASSA-PSS signatures  
  3. ECDSA signatures for other ECC curves
   i.e.: 
    1. BrainpoolP256r1,
    2. BrainpoolP384r1, 
    3. BrainpoolP512r1, 
    4. P-384 
    5. etc...
      
    
5. Send personal data (reveal)
Can be used to:
    1.  Challenge two IDs and check if the names match,
    2.  Can be used for KYC; people can use ID-ed account and only reveal the data after the government is forcing the dapp to do so,
    3.  It can also be used as one factor in the recovery procedure. People opt-in anonymously, and only disclose the data if they lose their keys.

  

## PassID Web Portal

Static page (“downloadable”) for parsing and publishing Master Lists, DSC lists and Revocation lists to the chain. Also for decrypting and verifying against smart-contract and viewing partial disclosed data (encrypted files people can export in their mobile app).

  

Simple looking statically served webpage written in React, with ECIES decryption libraries, with parsing engine/rules for data [downloaded from ICAO](https://pkddownloadsg.icao.int/) and other sources. UAL integration so anybody can publish that data to the smart contracts as well.

  
  

## Server verified Trust Chain

Server would verify data through [Trust Chain](https://www.icao.int/Security/FAL/PKD/Pages/ePassportBasics.aspx), from the master list to passports themselves.

  

Server Provide a fully verified path from;

Master List Signer (uploads the self- signed lists of other CSCA certificates)

CSCA (each country has one)

DSC (each country issues multiple, renews them every 3 months)

Revocation lists

Passport public key

All passport data

  

Current Master Lists on published publicly on ICAO site are produced by Swiss, Germany, Canada, Botswana, French, Moldova, Ukraine, Spain.  
  
Anybody can publish new data as long as it authenticates. This reduces the liability of the system maintainers/developers by not allowing to pinpoint who is actively refreshing the certs.  
  

  

## Server PassID signature verification


Algorithms and data schemes to be implemented:

-   Asn1 DER parser    
-   X509 parser
-   RSA decryption
-   ISO/IEC 9796-2 signature scheme
    

The constraints of eMRTD’s active authentication (AA) is that it can only sign 8 bytes at a time. To mitigate this, all important attestation would have to split SHA-256 digest of data being attested into 4, 8 bytes chunks and sign each chunk (4 signatures) with an eMRTD chip.


