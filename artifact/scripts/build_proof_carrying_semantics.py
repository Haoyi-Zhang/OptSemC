#!/usr/bin/env python3
"""Build proof-carrying finite certificates for projection loss and repair."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
sys.path.insert(0, str(ART))
from optsemc.corpus import load_contract_maps
from optsemc.projections import false_equivalence_witnesses
from optsemc.certificates import CertificateHeader, CertificateBundle, ProjectionLossCertificate, FrontierCertificate, HittingSetCertificate
from optsemc.manifest import sha256_file
cm=load_contract_maps(ART)
inputs={
    'contract_maps': sha256_file(ART/'evaluation'/'grounded_contract_maps.jsonl'),
    'verified_rules': sha256_file(ART/'grounded'/'verified_rules.jsonl'),
    'generated_probes': sha256_file(ART/'benchmark'/'generated_probes.jsonl'),
}
label='OptSemC'
header=CertificateHeader('OptSemC-proof-carrying-semantics', label, inputs, 'build_proof_carrying_semantics.py')
certs=[]
all_w=[]
for method in ('keyword','yesno','operator_only'):
    w=false_equivalence_witnesses(cm.maps, cm.engines, cm.probes, method)
    all_w.extend(w)
    certs.append(ProjectionLossCertificate.build(header, method, w, cm.maps, sample_limit=25).as_dict())
core=('operator','layer','placement','decision_time','observability')
certs.append(FrontierCertificate.build(header,'all_headline',all_w,cm.maps,core).as_dict())
certs.append(HittingSetCertificate.build(header,'all_headline',all_w,cm.maps,core).as_dict())
CertificateBundle(tuple(certs)).write_json(ART/'evaluation'/'proof_carrying_semantics.json')
print(f"Proof-carrying semantics: {len(certs)} certificates")

