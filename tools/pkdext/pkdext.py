#!/usr/bin/python

import sys, os
from collections import OrderedDict
from pathlib import Path
from typing import Dict
from datetime import datetime

from ldif import LDIFParser

sys.path.append(str(Path(os.path.dirname(sys.argv[0])) / Path("../libs/PassID-Server/src")))
from pymrtd.pki.x509 import Certificate, CscaCertificate, MasterListSignerCertificate, DocumentSignerCertificate
from pymrtd.pki.crl import CertificateRevocationList
from pymrtd.pki.ml import CscaMasterList

from asn1crypto.crl import CertificateList
from asn1crypto.core import OctetBitString, Sequence, SetOf, PrintableString, Integer

class DocumentTypeList(SetOf):
    _child_spec = PrintableString

class DocumentTypeListSyntax(Sequence):
    _fields = [
        ('version', Integer),
        ('docTypeList', DocumentTypeList)
    ]

def parse_dn(dn: str):
    d = {}
    dnp = dn.split('+') # split cn from the rest of dn
    if len(dnp) == 1:
        dn = dnp[0]
    elif dnp[0].lower().startswith('cn'):
        d['cn'] = dnp[0][4:]
        dn = dnp[1]
    else:
        dn = dnp[0]
        d['cn'] = dnp[1][4:]

    dna = dn.split(',') # split other dn parts
    for e in dna:
        ea = e.split('=', 1)
        d[ea[0].strip('\\').lower()] = ea[1]
    return d

def fatal_error(msg: str):
    print(msg, file=sys.stderr)
    exit(1)

def print_warning(msg: str):
    print("Warning: {}".format(msg))

def format_cert_sn(cert: Certificate):
    return hex(cert.serial_number).rstrip("L").lstrip("0x")

def format_cert_fname(cert, baseName = ""):
    if baseName != "":
        baseName = "_" + baseName

    if isinstance(cert, CertificateList) or 'country_name' not in cert.subject.native:
        subject = cert.issuer
        fp = cert.sha256[0:5].hex()
    else:
        subject = cert.subject
        fp = cert.sha256_fingerprint[0:5]

    if 'country_name' in subject.native:
        name = subject.native['country_name'] + baseName
    else:
        name = 'unk_' + subject.human_friendly
        name = name.replace(' ', '_')
        name = name.replace(':', '_')
        name += baseName

    # se_no_op = getattr(cert, "serial_number", None)
    # if callable(se_no_op):
    #     name += "_" + hex(cert.serial_number)[2:]
    try:
        name += "_" + hex(cert.serial_number)[2:]
    except:
        if 'tbs_certificate' in cert.native:
            name += "_" + hex(int(cert.native['tbs_certificate']['serial_number']))[2:]
        else:
            name += "_fp_" + fp
    return "".join(name.lower().split())

def get_ml_out_dir_name(ml: CscaMasterList):
    cert = ml.signerCertificates[0]
    name = cert.subject.native['country_name'] + "_ml"
    return name.lower()

def get_ofile_for_cert(cert, baseName, ext, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    out_dir = out_dir.joinpath('{}.{}'.format(format_cert_fname(cert, baseName), ext))
    return out_dir.open('wb')

def get_ofile_for_csca(cert: Certificate, out_dir: Path):
    return get_ofile_for_cert(cert, 'csca', 'cer', out_dir)

def get_ofile_for_dsc(cert: Certificate, out_dir: Path):
    return get_ofile_for_cert(cert, 'dsc', 'cer', out_dir)

def get_ofile_for_crl(crl: CertificateList, out_dir: Path):
    return get_ofile_for_cert(crl, 'crl', 'crl', out_dir)

def get_issuer_cert(issued_cert: Certificate, root_certs: Dict[bytes, Certificate]):
    if issued_cert.self_signed == 'maybe':
        return issued_cert
    if issued_cert.authority_key_identifier is not None:
        if issued_cert.authority_key_identifier in root_certs:
            return root_certs[issued_cert.authority_key_identifier]
    else:
        issuer = issued_cert.issuer
        for skid, rc in root_certs.items():
            if rc.subject == issuer:
                return rc

    return None



def verify_and_write_csca(csca: CscaCertificate, issuing_cert: CscaCertificate, out_dir: Path):
    try:
        if not csca.isValidOn(datetime.utcnow()):
            out_dir /= 'expired'

        csca.verify(issuing_cert)
        f = get_ofile_for_csca(csca, out_dir)
        f.write(csca.dump())
    except Exception as e:
        if "Signature verification failed" == str(e):
            print_warning("Signature verification failed for CSCA: {}, sig_algo: {}"
                          .format(csca.subject.native['country_name'], csca.signature_algo))
            with get_ofile_for_csca(csca, out_dir.joinpath('failed_verification')) as f:
                f.write(csca.dump())
        else:
            country = 'unk_' + csca.subject.human_friendly
            if 'country_name' in csca.subject.native:
                country = csca.subject.native['country_name']
            print_warning("CSCA verification failed! [C={} SerNo={}]\n\treason: {}"
                          .format(country, format_cert_sn(csca), e))
            with get_ofile_for_csca(csca, out_dir.joinpath('failed_verification')) as f:
                f.write(csca.dump())

def verify_and_extract_masterlist(ml: CscaMasterList, out_dir: Path):
    # verify ml integrity
    try:
        ml.verify()
    except Exception as e:
        print_warning("Integrity verification failed for master list issued by {}."
                      .format(ml.signerCertificates[0].subject.native['country_name']))
        out_dir /= 'unverified_ml'

    # verify and extract CSCAs
    cscas = {}
    skipped_cscas = []
    for csca in ml.cscaList:
        try:
            # The the wrap in the try cache was done due to CSCAs from LT
            # don't encode subject key identifier correctly.
            # i.e.: KeyIdentifier is defined in RFC 5280 as OCTET STRING within OCTET STRING
            #      but the problematic certs can encode key id as single OCTET STRING.
            #       
            #
            # Problematic CSCAs:
            #   C=LT SerNo=275b
            #   C=LT SerNo=2761
            #   C=LT SerNo=2748

            if csca.key_identifier not in cscas:
                cscas[csca.key_identifier] = csca
        except Exception as e:
            print_warning("An exception was encountered while trying to get keyID of CSCA C={} SerNo={}"
                .format(csca.subject.native['country_name'], format_cert_sn(csca)))
            with get_ofile_for_csca(csca, out_dir.joinpath('parse_error')) as f:
                f.write(csca.dump())
            continue

        if csca.self_signed != 'maybe':
            if csca.authority_key_identifier not in cscas:
                skipped_cscas.append(csca)
                continue
            issuing_cert = cscas[csca.authority_key_identifier]
        else:
            issuing_cert = csca

        verify_and_write_csca(csca, issuing_cert, out_dir)

    for csca in skipped_cscas:
        issuer_cert = get_issuer_cert(csca, cscas)
        if issuer_cert is None:
            print_warning("Could not verify signature of CSCA C={} SerNo={}. Issuing CSCA not found!"
                          .format(csca.subject.native['country_name'], format_cert_sn(csca)))
            with get_ofile_for_csca(csca, out_dir.joinpath('unverified')) as f:
                f.write(csca.dump())
        else:
            verify_and_write_csca(csca, issuer_cert, out_dir)

    # verify master list signer certificates
    for mlsig_cert in ml.signerCertificates:
        issuer_cert = get_issuer_cert(mlsig_cert, cscas)
        if issuer_cert is None:
            print_warning("Could not verify signature of master list signer certificate. Issuing CSCA not found! [C={} Ml-Sig-SerNo={}]".format(mlsig_cert.subject.native['country_name'], format_cert_sn(mlsig_cert)))
        else:
            try:
                mlsig_cert.verify(issuer_cert)
            except Exception as e:
                print_warning("Failed to verify master list signer C={} Ml-Sig-SerNo={}\n\treason: {}".format(mlsig_cert.subject.native['country_name'],format_cert_sn(mlsig_cert), str(e)))








if __name__ == "__main__":
    valid_ext            = set([".ml", ".ldif"])
    default_out_dir_csca = Path("csca")
    default_out_dir_dsc  = Path("dsc")
    default_out_dir_crl  = Path("crl")

    if len(sys.argv[1:]) == 0:
        fatal_error("Usage:  <path_to_file|*.ml|*.ldif>")

    in_file_path = Path(sys.argv[1])
    in_file_ext = in_file_path.suffix
    if in_file_ext not in valid_ext:
        fatal_error("Error: Invalid input file!")

    if not in_file_path.exists() or in_file_path.is_dir():
        fatal_error("Error: Invalid input file path!")

    with in_file_path.open('rb') as f:
        if in_file_ext == '.ml':
            ml_bytes = f.read()
            ml = CscaMasterList.load(ml_bytes)
            verify_and_extract_masterlist(ml,
                default_out_dir_csca.joinpath(get_ml_out_dir_name(ml))
            )
        else:
            parser = LDIFParser(f)
            print("Note: DSC and CRL won't be verified against issuing CSCA!")
            for dn, entry in parser.parse():

                # ML
                if 'CscaMasterListData' in entry:
                    ml = entry['CscaMasterListData'][0]
                    ml = CscaMasterList.load(ml)
                    verify_and_extract_masterlist(ml,
                        default_out_dir_csca.joinpath(get_ml_out_dir_name(ml))
                    )

                # DSC
                elif 'userCertificate' in entry or 'userCertificate;binary' in entry:
                    dn = parse_dn(dn)
                    dsc = entry['userCertificate;binary'][0]
                    dsc = DocumentSignerCertificate.load(dsc)
                    for e in dsc.native['tbs_certificate']['extensions']:
                        if e['extn_id'] == '2.23.136.1.1.6.2':

                            dtl = DocumentTypeListSyntax.load(bytes(e['extn_value']))
                            #print(bytes(e['extn_value']).hex())
                            fdtl= open("dsc_doc_type_lists.txt","a")
                            fdtl.write("issuer: " + dsc.issuerCountry + "\n")
                            fdtl.write("ser: " + hex(int(dsc.native['tbs_certificate']['serial_number']))[2:] + "\n")
                            try:
                                fdtl.write("  " + str(dtl.native['docTypeList']) + "\n")
                            except Exception as aaaa:
                                fdtl.write("  " +  bytes(e['extn_value']).hex() + "\n")
                                fdtl.write("  " +  str(dtl) + "\n")
                            fdtl.flush()
                    f = get_ofile_for_dsc(dsc, default_out_dir_dsc / dn['c'].lower() / 'unverified')
                    f.write(dsc.dump())

                # CRL
                elif 'certificateRevocationList' in entry or 'certificateRevocationList;binary' in entry:
                    dn = parse_dn(dn)
                    crl = entry['certificateRevocationList;binary'][0]
                    crl = CertificateRevocationList.load(crl)
                    f = get_ofile_for_crl(crl, default_out_dir_crl / dn['c'].lower() / 'unverified')
                    f.write(crl.dump())