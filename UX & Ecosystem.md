# UX

A typical user would:  
• Install the Android/iOS app on a phone (on theirs or someone else's device with NFC)

• Type EOSIO account name that you want to verify

• Scan the passport with a camera (that reads the data to establish a secure connection over NFC)

• Tap the passport on a phone

• Publish the transaction using your account permissions- either on the phone, or optionally, use share capability to send raw data to your desktop (over email, Telegram, WhatsApp, WeChat,...), and use the online portal to publish it from there (by using any [Universal Authenticator Library](https://github.com/EOSIO/universal-authenticator-library) providers)  
  
Your account is now PassID verified, and you can use it like any other EOS account.

# Example (D)apps that can leverage EOSIO PassID

PassID is the building block for countless of other ideas; we want to highlight we consider high impact.

  

### Crypto UBI, Airdrops/Airgrabs

Using verified accounts enables a rich set of fixed or on-going airdrops, based on allocation or inflation. Per country budgets to limit (unlikely but possible) government abuse (by issuing virtual passports).

  

To remove your government's ability to surveil, all air grabs can be run through long-running Chaumian coinjoins (or similar newer approaches). UBI Airgrabs are perfect for this because everybody gets the same amount, thus exiting the private transaction to an anonymous account won’t reveal anything. That allows anonymity set to be as big as the number of all Airgrabbers.  
  

### Key Registry

Key Registry helps dapps find a diverse group of Key Providers to secure their contract. Key Registry is a smart contract that helps with on-chain coordination. Dapps register and provide their parameters/requirements, Key providers register and opt-in (effectively promise) to help a dapp.  
  
The typical key provider would be Block Producer (candidate). This is all good, but it effectively means the key providers would be a static set of (standby) BPs. To increase the decentralization and provide the ability for a dapp provider to extend the trust globally, a new consensus could be used.

A representative democracy.

It ensures the Key Provider candidates are chosen locally. Then each country PassID Key Providers gets a ranking, and the most highly ranked Key Provider that opts into you dapp, gets to be in the multisig. That multisig automatically rotates if some Key Provider loses PassID votes, or some with a higher number of votes opt-in later. You can only vote for your representative, and can’t influence other countries votes. This reduces the ability to pay for votes and greatly mitigates the ability of abusing government issuing virtual passports to overpower their population vote.  
  

### KYC commit/reveal

PassID account can also be used as a “KYC commitment”. The exchanges/dapp can block/limit certain countries (unfortunate but it seems projects need it) without requesting “KYC reveal”. Assuming the regulator/police needs the data on a specific user (for instance in a case of stolen coins), the exchange or dapp provider can freeze the account and require the PassID user to reveal all the data from the passport- which is authenticated in his already committed PassID account. Affected user can present said data just by tapping on an NFC and send it to the exchange/dapp. The exchange/dapp then sends the data to authorities and releases the coins.

  

This might be very useful for security tokens and other financial (d)apps. Tokens with voting rights might need to reveal themselves before their vote is counted etc.

  
A good compromise between compliance and data protection, especially in an age of GDPR, [massive KYC data leaks](https://www.coindesk.com/binance-kyc-issue). Now even social networks [are starting to enforce](https://twitter.com/davidebbo/status/1178098665073737728) the same data collecting/exposing techniques that people in cryptocurrencies are being subject to, PassID can serve as an alternative.
