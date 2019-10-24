
# Documenting risks/limits of PassID

## Sybil risks
There is a risk of a corrupt country issuing unlimited virtual passports (by using DSC issued certificates). To limit that risk the dapp providers need to impose limits per country.

Mitigation; For airdrops/air grabs; limit max % each country can claim. When/if the limit is reached, start diluting the claim within that country. This makes sure that abuse is contained and only “steals” from a citizen of the abusing country.

If there is voting (one PassID one vote), it's better to have a representative democracy. Potential abuse is then limited only to one representative from the specific abusing country.

## Skimming
Skimming is not that easy, because [SAC](https://en.wikipedia.org/wiki/Supplemental_access_control) is used to secure the access to passport over NFC. To get enough data for a handshake, the attacker needs to see the first page of the passport. This does allow corrupt gate attendant or police officer to start onboarding ton of unsuspecting passenger to PassID system, which could be abused to drain airdrops and Sybil votes.

Mitigation; we propose 2 weeks verification maturity, where first-time verifiers can have the PassID account to claim airdrops, but they can’t transfer them until they attest their PassID account again (after 2 weeks or more).

## Lost/stolen
Public Certificate revocation lists (CRLs) are only issued to revoke CSCA and DSC issued certificates. Currently, they don’t publish revocation lists containing specific passports. The data about stolen passports they send to the Interpol also can’t be used to revoke the passports trustlessly. We would need to convince countries to issue DSC signed revocation lists of revoked passports to solve it, or employ mitigations (which isn’t realistic).  
 
Mitigation; all DSC certificates are only used for 3 months (according to standard) an have an expiration date (10 years), which can be used to remove the lost/stolen passports sooner or later.

We propose each PassID needs to be attested yearly, to show the participant can still exercise authority over account private key and physical passport. As a bonus, this would also help expire the stolen accounts (where the passport was not stolen!), where the passport owner doesn’t come back to revoke the account.

## Privacy risk
PassID system is very private as far as ID systems go. It only reveals your country of origin and your passport public key on-chain. The remaining risk is that country that issued your passport can match your account with your name; using their passport issuing records. Other countries can not.  
 
Mitigation;  to remove your government's ability to surveil, all air grabs can be run through long-running Chaumian coninjoins (or similar newer approaches). UBI Airgrabs are perfect for this because everybody gets the same amount, thus exiting the private transaction to an anonymous account won’t reveal anything. That allows anonymity set to be as big as the number of all Airgrabers.
