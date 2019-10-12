# Brief overview of  ICAO 9303
## Abstract 
International Civil Aviation Organization or ICAO is a specialized agency of the United Nations.
The ICAO Council adopts standards and recommended practices concerning air navigation, its infrastructure, flight inspection, prevention of unlawful interference, and facilitation of border-crossing procedures for international civil aviation. ICAO defines the protocols for air accident investigation that are followed by transport safety authorities in countries signatory to the Chicago Convention on International Civil Aviation.

This document briefly overviews ICAO standard for electronic passport, the doc 9303.
Document is divided in two sections. First section defines the standard terminology that is used in the second section. The second section briefly describes and summarizes the parts of the 9303 standard which are of interest for PassID.


## Terminology

| Keyword   | Definition  |
| ------------ | ------------ |
| AA  |  Active authentication. A procedure done by IC in order to prevent skimming and duplicating MRTD. |
| ASF/SLTD  | A database of stolen and lost TDs maintained by Interpol. <br>*Note: database is not publicly available.*  |
| CSCA  |  Country signing certification authority. Root certificate for eMRTD PKI. Usually its self issued and signed. |
| CRL  |  Certificate revocation list. List of revoked certificates (CSCA, DSC, MLSC etd..) signed by valid CSCA of issuing authority. CRL is defined in RFC-5280. |
| DL | Deviation list.<br/><br/> A list of countrys PKI certificates, MRTD’s LDS & MRZ data that deviates from the ICAO 9303 standard. The list is signed by DL signer of issuing authority.  |
| DLSC  | Deviation list signer certificate.  |
| DSC | Document signer certificate  |
| ECC  | Elliptic curve cryptography.  |
| eMRTD  | Electronic machine readable travel document (ePassport). |
| IC  |  Integrated Circuit. RFID chip stored on the MRTD.  |
| ICAO  | International Civil Aviation Organization.  |
| IFD  | Interface device. Device that communicates with IC.  |
| [ISO/IEC 9796-2](http://www.sarm.am/docs/ISO_IEC_9796-2_2002%28E%29-Character_PDF_document.pdf)   | Message recovery digital signature scheme.  |
| LCSCA   | Linked CSCA. CSCA issued by previous/current CSCA.  |
| LSRTD  |  Lost, stolen or revoked travel document.  |
| ML | Master list.<br/><br/>A list of CSCAs from states that the issuing authority of the master list has bilateral agreement with. List also includes CSCA from the issuing authority and is digitally signed by the ML signer of the issuing authority.
  |
| MLSC  | Master list signer certificate.  |
| MRP  | Machine readable passport (ePassport).  |
| MRTD  | Machine readable travel document.  |
| MRZ  |  Machine readable zone. Visual zone on physical page in passport which can be read by machine via imaging and OCR processing.  |
| PKC  | Public key cryptography (asymmetric cryptography).  |
| PKD  |  Public key directory.<br/><br/>PKD stores all important parts of eMRTD PKI including CSCAs, DSCs etc. The LDAP  is a protocol for handling the access and upload of files to PKD. Direct access to state’s PKD is usually subject to A bilateral agreement between states, but the ICAO 9303 standard encourages issuing authorities to provide public access to their eMRTD PKI. ICAO also maintains private PKD service for the state members and is acting as a central body for eMRTD PKI where PKI of other members can be accessed.  ICAO also provides public access to some parts of its PKD via http protocol:  https://pkddownloadsg.icao.int/download |
| SOD  | Document security object. <br/><br/> Data structure stored in IC of eMRTD which contains digest hashes of other data structures such as hash of AA public key, document no. and validity  etc. SOD is signed with document signer key and should be verified in the process of passive authentication against DSC.  |
| TD  | Travel document (passport).  |
| [TR-03111]( https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03111/BSI-TR-03111_V-2-1_pdf.pdf?__blob=publicationFile&v=2) | PKC specification for ECC signature used by IC to perform AA.  |

## Parts of ICAO doc 9303 interesting for PassID

**Part 1**: General overview of the eMRTD standard. 
Important sections: 4.1 Acronyms, 4.2 Term and definitions, 4.3 description of key words, 4.4 ISO Object Identifiers (OIDs)

**Part 2**: Specifies security of design, manufacturing and issuance of MRTD by TD issuing authority.
Important section:  
6: Provision of information on lost and stolen MRTDs. It defines general recommendations on how states should exchange information on lost, stolen or revoked TD (LSRTD) and procedure to be applied when LSRTS is detected.

In brief on the information exchange:  Specification recommends TD issuing authorities to establish and maintain a national database of LSRTD. In addition, the issuing authority is advised to share all information on LSRTD with the INTERPOL. INTERPOL facilitates a database of stolen and lost TD (ASF/SLTD). See section 6.2, 6.3 and appendix D. 

Note: At the time of writing this document no publicly available database of LSRTD was found!

**Part 3**: Common specification of (physical) MRTD.
Important sections: 
4: General specification of MRZ
5: ISO specification of 2 and 3 alpha letter country codes
6: Recommended transliteration between different characters of the Latin, Cyrillic and Arabic families of languages
7: Deviations
Deviations are defined as MRTDs that contain elements that do not precisely conform to the ICAO specifications and the governing ISO and RFC standards. Issuing authorities are solely responsible to inform other states of their eMRTD deviations from the standard. However this part defines standard data structure to be used to inform others of non-conforming elements of eMRTD. The structure is defined as Deviation List. It signed RFC-3852 data structure with custom fields.  

**Part 4,5,6**: Physical specifications of TD3, TD1, TD2.
Important sections in these parts are: 
3: General layout of MRZ on physical page in MRTD
4.2.2: Data structure of MRZ
4.2.3: Truncation of names in the MRZ
4.2.4: Check digits in the MRZ
4.3: Representation of the Issuing State or Organization and Nationality of Holder in the MRZ

**Part 10**: Defines technical specification of eMRTD contactless IC communication and logical data structure (LDS) of  eMRTD.
In brief: The proximity contactless IC of eMRTD should comply with ISO/IEC 14443 standard with type A or type B signal interface. The IC should have support for file structure, one or more application and appropriate commands as defined in ISO/IEC 7816-4 standard. The Application Family Identifier (AFI) should be 0xE1 (eMRTD) and CRC_B of Application Identifier (AID: 0xA0000002471001) should be 0xF35E. The file structure is specified in section 4. The data encoding of element files should follow ISO/IEC 7816-4 and ISO/IEC 7816-6 standard. In the nutshell data should be TLV (tag length value) encoded in DER (distinguished encoding rule) format with appropriate ASN.1 tag (Abstract syntax notation 1).
The definition of Elementary Files and Data Group files that can be stored on IC is specified in sections 5 and 6.

**Part 11**: Defines security mechanisms for eMRTD.
This includes technical specifications of cryptographic protocols to:
prevent skimming of data from the contactless IC
prevent eavesdropping on the communication between the IC and reader
provide passive authentication of the data stored on the IC (section 5, section 8.3, appendix E) based on the PKI described in Part 12. In this process, among others the SOD data structure should be verified against issuing DSC.
provide active authentication of the IC itself. 
In brief: Section 6.1 describes active authentication of eMRTD’s IC by signing 8 bytes challenge sent by the IFD with a private key known only to the IC. 
Asymmetric cryptography to sign challenge should be either RSA or ECDSA.
For worked example see appendix F.

RSA: Should compute signature according to the ISO/IEC 9796-2 digital signature scheme 1.
         For message digest usually Sha-1 is used in signature generation process.
         Other message digest functions that can be used are specified in
         ISO/IEC JTC ; ISO/IEC 10118. The hash function UID of the ISO/IEC 10118
         to be used can range from 0x00 to 0x7f.

ECDSA: For ECC, a plain signature format according to the TR-03111 shall be used.
              Only prime curve with uncompressed points shall be used.

**Part 12**: Defines technical specification of eMRTD PKI.
It specifies requirements and technical specifications for issuing and receiving authorities to be followed. This includes issuing and establishing trust anchor of CSCAs that issue other certificates (DSC, MLSC, DLSC) and CRL. All issued certificate should be in x.509 format specified by RFC-5280. 
This part also defines:
private key usage and public key validity associated with certificates.
handling of revoked certificates
cryptographic algorithms to be used (section 4.4): 
RSA - should follow RFC-4055 which defines two signature mechanisms: 
RSASSA-PKCS1_v1.5 and RSASSA-PSS. The standard recommends that issuing authorities 
                       use the former signature scheme.
ECDSA - should follow either ANSI x9.62 (old) or ISO/IEC 15946 standard. In general it is recommended to follow guidelines from TR-03111. In addition, the standard mandates that EC domain parameters to generate ECDSA key pair must be described explicitly in the parameters of public key, no named curves should be used and must include the optional co-factor. The EC points must be in uncompressed format.
DSA - should follow FIPS 186-4
Hashing algorithms
Only the following algorithms are permitted to be used: Sha-224, Sha-256, Sha-384 and Sha-512.

technical specification of CRL, CSCA, DSC
Technical specification of ML. In brief: ML is unencrypted and signed RFC-3652 CMS data structure, containing list of CSCA in the encapsulated content field. 
PKI distribution mechanisms to receiving states. It also describes the ICAO’s PKD service.



