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

This project aims to;

1.  Provide Android and iOS apps for the end-user to attest their accounts; Verify the signatures in the server-side software;    
2.  Provide a fully verified path from: 
    1.  Master List Signer (uploads the self- signed lists of other CSCA certificates) 
    2.  CSCA (each country has one)    
    3.  DSC (each country issues multiple, renews them every 3 months or after signing 100k documents)    
    4.  Revocation lists    
    5.  Passport public key    
    6.  All passport data
 3.  Partial disclosure (pre-authenticated). Useful for actual KYC and/or for challenging people with multiple passports and as another factor used for recovery.
    

  

# Deliverables

  
1. PassID Android app. 
2. PassID iOS app (after iOS13). 
3. PassID Web Portal- for parsing and uploading Master Lists, DSC lists and revocation lists and viewing partial disclosure data.
4. Trust Chain verification.
5. Verify Passport signatures.
6. Further research to cover more and more edge/future cases. 

  

## EOSIO PassID Mobile Apps

  
We developed a barebone android app for [Ethereum hackathon](https://github.com/ZeroPass/TokenRegistry).

Implemented [BAC](https://en.wikipedia.org/wiki/Basic_access_control) for talking with the passport- (people need to type those numbers in by hand);  
Then send over NFC(write) the hash of the ethereum pubkey (8 bytes only). And get the signed data back (fun fact: one of our passports got bricked while we were hacking it). ![](https://github.com/ZeroPass/PassID-documntation-and-tools/blob/master/images/passport_mr.png?raw=true)

The project was/is very experimental, open-source libraries are stubs with wrong information, docs are scarce and written in obfuscated ways for industry insiders. Trial and error is the modus operandi.  
For real applications, we need to up the game:

  

1.  BAC works, but it's very insecure and would be deprecated soon. We need to implement [SAC](https://en.wikipedia.org/wiki/Supplemental_access_control).  
      
    
2.  (optional- but needed) Typing numbers by hand is fine for a PoC, but end product needs to include a camera to read those numbers from user passports (ML Kit or something similar)  
      
    
3.  People would be able to input any account and sign its hash - this means you can use untrusted devices to sign. If the device app switches the account, you would be able to use your passport again on another device to revoke.  
      
    
4.  Four times RSA signatures for full verification, and one time RSA signature for proof of possession (less secure).First time verification or changing of the keys (for recovery?) would need four signatures. For proving the account is still in possession of the original owner (periodical renewals?), one signature would be enough. [Read more about the reasoning in verify section. ](https://docs.google.com/document/d/1agAKKX5GFBZ7ZrViHkYU5TSCphc3iCJexJ_OIoHxfNc/edit#bookmark=id.dvys2n7wo6st)
    
5.  The ICAO standard also specifies document authentication using ECC particularly curve p-256 (secp256r1), but a short search didn’t show us any country that is using it right now (we don’t know for sure). Nonetheless, we will implement both RSA based signature verification and ECC using P-256.  
      
    
6.  (optional) Partial disclosure function; this function would allow the user to write an account name they want to send the data too, which would, in turn, take out the public key and use ECIES to encrypt it. After that user can email the encrypted blob to the receiver, which can drop it to the EOSIO PassID Web Portal, which would decrypt and fully authenticate the data to the user account.  
Partial disclosure can be used to:
    1.  Challenge two IDs and check if the names match,
    2.  can be used for KYC; people can use ID-ed account and only reveal the data after the government is forcing the dapp to do so,
    3.  it can also be used as one factor in the recovery procedure. People opt-in anonymously, and only disclose the data if they lose their keys.
    

  

iOS just added NFC write api to their iOS 13, which means that from September it should be possible to implement.  
  
We prefer to use QT framework and C++ for apps (more experience) but are also ready to write Java + Swift apps if requirements or some unforeseen limitations are found.  
  

Mobile Apps would mimic the feel and simplicity of EOSIO reference authenticator.

  

## EOSIO PassID Web Portal

Static page (“downloadable”) for parsing and publishing Master Lists, DSC lists and Revocation lists to the chain. Also for decrypting and verifying against smart-contract and viewing partial disclosed data (encrypted files people can export in their mobile app).

  

Simple looking statically served webpage written in React, with ECIES decryption libraries, with parsing engine/rules for data [downloaded from ICAO](https://pkddownloadsg.icao.int/) and other sources. UAL integration so anybody can publish that data to the smart contracts as well.

  
  

## EOSIO Trust Chain smart contract

WASM C++ contract that provides [Trust Chain](https://www.icao.int/Security/FAL/PKD/Pages/ePassportBasics.aspx) from the master list to passports themselves

  

Provide a fully verified path from;

Master List Signer (uploads the self- signed lists of other CSCA certificates)

CSCA (each country has one)

DSC (each country issues multiple, renews them every 3 months)

Revocation lists

Passport public key

All passport data

  

Current Master Lists on published publicly on ICAO site are produced by Swiss, Germany, Canada, Botswana, French, Moldova, Ukraine, Spain.  
We can start by using those CSCA keys and define the threshold for adding new ones. For instance, if 4 out of all lists claim new CSCA is legit and the same, we add it to the contract. That way we can probably add all other countries CSCA in a permissionless way.  
  
Then we can use those keys to authenticate DSC and RCL (revocation) lists for each country.  
The beautiful part is that anybody can publish new data as long as it authenticates. This reduces the liability of the system maintainers/developers by not allowing to pinpoint who is actively refreshing the certs.  
  

To optimize performance, we don’t need to verify the data itself until the passport signature presented request the specific path to be authenticated. Once all the signatures are verified, the whole path gets approved, so if the same person comes the second time (and revocation lists didn’t nullify its path), the contract can just use the state instead of verifying the whole path again. Relying on a state instead of verifying minimizes the CPU resources needed and makes the whole process scalable. It also allows new data to be constantly uploaded but doesn’t waste resources on verifying every signature in it.

**EOS WASM intrinsics for decrypting RSA signatures would go a long way to further improve the performance.**

  

## EOSIO Verify PassID smart contract

WASM C++ contract that verifies the passport signature.

Algorithms and data schemes to be implemented:

-   Asn1 DER parser    
-   X509 parser
-   RSA decryption
-   ISO/IEC 9796-2 signature scheme
    

The constraints of eMRTD’s active authentication (AA) is that it can only sign 8 bytes at a time. To mitigate this, all important attestation would have to split SHA-256 digest of data being attested into 4, 8 bytes chunks and sign each chunk (4 signatures) with an eMRTD chip.
  
**The fact there are 4 signatures to verify also means RSA should be implemented as WASM intrinsic  for performance (and resource cost) reasons.**

To sign, the EOSIO Mobile App would take user-provided account name, add some verifiable data (timestamp, TaPos, name of the action?...), hash it, then split the hash into chunks.  
Then send every chunk one after another via NFC to be digitally signed by the passport. When all chunks are signed, their signatures, public key used to make those signatures and attested data (or its hash) is sent to the Verify PassID smart contract via transaction.  
  
The contract first verifies the public key is genuine by looking in the chain database (CSCA & DSC master list/revocation list). If the verification fails the whole transaction fails. After the public key verification, it generates a hash, if not provided, from the received attested data. Then it’s split hash into chunks and depending on which DSA was used based on the signature type it verifies the signature of each hash chunk. If for any chunk the verification fails, the whole transaction fails.

In the case of ECC based DSA and ECDSA P-256, no additional implementation is needed since it should already be possible to verify the signature in the contract. Other ECC DSA specified in the BSI TR-03111 (ECGDSA, ECSDSA) are not taken into account here since we were not able to determine if any is used at the time of writing this document.
  
In the case of RSA DSA, we would need to implement ISO/IEC 9796-2 signature verification scheme along with RSA decryption. RSA decryption could be and probably should be implemented as WASM intrinsic for faster decryption. Also, it can be used for a wide variety of government connected use-cases. Many institutions trust long RSA keys more than elliptic curve cryptography. The ISO/IEC 9796-2 shall be implemented in the contract.

## Algoritms missing from EOSIO WASM intrinsics
SHA-224, SHA-384, RSA
