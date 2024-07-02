<!--next-version-placeholder-->

## v0.7.0 (2024-07-02)

### Feature

* SA-429 Add options support ([`087b1ac`](https://github.com/SIGTechnologies/sigtech-python/commit/087b1acb795dd70c931a3850c5c682ab724d9dcf))
* Remove tests for end-of-life python3.6 & python3.7 ([`db2d809`](https://github.com/SIGTechnologies/sigtech-python/commit/db2d8093d63a508b608575a266d994316ed827e4))

### Fix

* Install libomp on macos ([`1da1c15`](https://github.com/SIGTechnologies/sigtech-python/commit/1da1c1577441ba2698e4f5fe4430d494361d5c9e))
* Pin numpy in older tests ([`d43b1d8`](https://github.com/SIGTechnologies/sigtech-python/commit/d43b1d85a3843b2d23b80e646c6c1d9792cd1bcc))

## v0.6.1 (2024-05-28)

### Fix

* Pin matplotlib in colab test case ([`94b785e`](https://github.com/SIGTechnologies/sigtech-python/commit/94b785eb42c08a07df79aa0695c2f7c1f9448a1b))

## v0.6.0 (2024-05-28)

### Feature

* SA-421 Add SDK support for RollingBondStrategy & SingleBondStrategy ([`94d5260`](https://github.com/SIGTechnologies/sigtech-python/commit/94d52601e7ff1ca469c908b33c1350c2cdfb04fc))

### Fix

* Remove signup reference from readme ([`74f88f8`](https://github.com/SIGTechnologies/sigtech-python/commit/74f88f8f3d4a902efbc3957cd929f91ebba213bb))
* SA-438 Bugfix for Jobs API output formats ([`1005ab3`](https://github.com/SIGTechnologies/sigtech-python/commit/1005ab3b4e39af4a7ea20de758d58994d09c99c6))

### Documentation

* SA-434 Documentation updates ([`afd4ed7`](https://github.com/SIGTechnologies/sigtech-python/commit/afd4ed7f0b5145d134980be69acbbcd8f2ebec6b))

## v0.5.1 (2024-03-25)

### Fix

* Datasets & Jobs API wrappers ([`5f58e34`](https://github.com/SIGTechnologies/sigtech-python/commit/5f58e343dc2911305c927857bd63650b5ef39c7d))

## v0.5.0 (2024-03-01)

### Feature

* Remove data validation support from SDK ([`00b7b8e`](https://github.com/SIGTechnologies/sigtech-python/commit/00b7b8ed10ae0a5ec5a626082b377a31ff803190))

### Fix

* Fix broken link in README.md ([`472209e`](https://github.com/SIGTechnologies/sigtech-python/commit/472209e867be2fbcec2aa20865a14015451af363))
* Add support for Rolling Swap strategy ([`fd732f9`](https://github.com/SIGTechnologies/sigtech-python/commit/fd732f96ed86bd3cd75d54480d4e2716b1865ea6))
* Remove scikit-learn explicit dependency for train_test_split ([`e5faee2`](https://github.com/SIGTechnologies/sigtech-python/commit/e5faee2cdee5392fd95c0ac2f7cff34ec949bbe4))
* Add support for FX Forwards ([`2f93026`](https://github.com/SIGTechnologies/sigtech-python/commit/2f930260e4c3cd7ac47235bebae5d96bdfa4bea8))
* Add support for Interest-Rate Swaps ([`f899cbd`](https://github.com/SIGTechnologies/sigtech-python/commit/f899cbdcac8fd3a14889fad7fcb98ac6746f7aea))
* Use new comma syntax change for front_offset & monthly_roll_days ([`e1b3786`](https://github.com/SIGTechnologies/sigtech-python/commit/e1b37862904efe52f4e9f710fbda6dec0b4da80b))
* Remove empyrical dependency ([`9f7fda7`](https://github.com/SIGTechnologies/sigtech-python/commit/9f7fda766a90583b877d76c15dcc4753e7f73ab2))
* Remove ta import ([`f7c2686`](https://github.com/SIGTechnologies/sigtech-python/commit/f7c268645ea280d8604a4c01bd8af44a1de36578))
* Bump tools lockfile ([`ab59d19`](https://github.com/SIGTechnologies/sigtech-python/commit/ab59d19cab0eba6f32dce4d9b8ae48bb87647289))
* Bump tests to use python3.12 ([`8152698`](https://github.com/SIGTechnologies/sigtech-python/commit/81526986a61e610cbc4dd8eef683dd3030bbe77c))
* Bump versions of standard github actions ([`afcf155`](https://github.com/SIGTechnologies/sigtech-python/commit/afcf1559a8944653048cb35fb6faedec83b815d0))

### Documentation

* Fix typo in OIS example ([`e911659`](https://github.com/SIGTechnologies/sigtech-python/commit/e911659f38d83ddbead9a4e38430977fa3e1b93e))

## v0.4.2 (2024-01-19)

### Fix

* SA-224 Add SDK support for OISSwap ([`f9b64df`](https://github.com/SIGTechnologies/sigtech-python/commit/f9b64df4e876d4fa6ca4b0d101aa890aeefe74b1))
* SA-353 Add SDK support for TradableTSIndex ([`ecf0273`](https://github.com/SIGTechnologies/sigtech-python/commit/ecf027393ee9c9a742107707867e333b6f3df178))
* Add SDK-Python/<version> to the User-Agent header ([`89d5a6a`](https://github.com/SIGTechnologies/sigtech-python/commit/89d5a6a74f1394d88f91b5a463114e15d84eb47f))

### Documentation

* Update License ([`1c02b5d`](https://github.com/SIGTechnologies/sigtech-python/commit/1c02b5d12e2ccb54ceab5aa472c5820501bee2eb))

## v0.4.1 (2024-01-02)

### Fix

* Add support for reference data on API objects ([`704785f`](https://github.com/SIGTechnologies/sigtech-python/commit/704785f64b7a7aa10d55ef1b7a5ae4e89dd929ef))

## v0.4.0 (2023-12-18)

### Feature

* Add ETF and single stock support with example script ([`b25fcfa`](https://github.com/SIGTechnologies/sigtech-python/commit/b25fcfaf453ec9f70c699d8b7b5786214f43a1df))
* Add ticker input for named basket and signal strategies ([`89b3397`](https://github.com/SIGTechnologies/sigtech-python/commit/89b33978278333b4ac14db8e748d94a5b82f24c9))

### Fix

* Fix checks for pypi package release ([`664f692`](https://github.com/SIGTechnologies/sigtech-python/commit/664f6921e817b98b2fda0af6d4dc74d175662d7e))
* Assert SIGTECH_API_KEY environment variable exists in scripts ([`5e4c83e`](https://github.com/SIGTechnologies/sigtech-python/commit/5e4c83eded44a15d0cf592ec1954947b67f08b2d))
* Remove scripts from wheel and source-distribution ([`2119b9d`](https://github.com/SIGTechnologies/sigtech-python/commit/2119b9d9e58724cfcba0ce755dd82a7ed32d7031))

### Documentation

* Add FX spot trade example ([`aeb9332`](https://github.com/SIGTechnologies/sigtech-python/commit/aeb9332b5e39e0b6b5de817a01feaa61803b1521))

## v0.3.0 (2023-11-16)

### Feature

* SA-274 Add support for portfolio table ([`94a3e4e`](https://github.com/SIGTechnologies/sigtech-python/commit/94a3e4e24f854cc8e8acbcd8cbc6dc617a483521))

### Fix

* Bugfix for rolling futures contract code with trailing space (e.g. `Z `) ([`f9251ea`](https://github.com/SIGTechnologies/sigtech-python/commit/f9251eaf6ce17b73a3a5894874b3c91e1cb1fb7c))

### Documentation

* Replace hubspot img url with cms url [TW-380] ([`9d06327`](https://github.com/SIGTechnologies/sigtech-python/commit/9d0632748ee6c3531bb571d2d37deea5db9f177b))
* Reorganise examples directory ([`68e69b0`](https://github.com/SIGTechnologies/sigtech-python/commit/68e69b0fd9b2b7f1b5eeb4669dbeb5323a679a99))

## v0.2.1 (2023-10-12)

### Fix

* Add support for environment flags & total_return for rolling-futures strategy ([`9552ae9`](https://github.com/SIGTechnologies/sigtech-python/commit/9552ae9739611d22857d2a7e69ec2f1dcd28b2a2))
* Fix sed command to catch python files in new sub dirs ([`4228a36`](https://github.com/SIGTechnologies/sigtech-python/commit/4228a36d21ea42cc4c95ee550c5341f7a76e3670))

### Documentation

* Fix broken colab links ([`446d34e`](https://github.com/SIGTechnologies/sigtech-python/commit/446d34eea337844a6d3ee6768cf19131ffa1d8aa))

## v0.2.0 (2023-10-10)

### Feature

* Sdk client to send Sig-Version header in requests ([`9776845`](https://github.com/SIGTechnologies/sigtech-python/commit/977684524cb063e695e5c41e2cec9693eb7948a8))
* Add dave support ([`bb814af`](https://github.com/SIGTechnologies/sigtech-python/commit/bb814af451e10597b650b33eb61b3efe82ab2504))

### Fix

* Pin semantic release version ([`f04ffa7`](https://github.com/SIGTechnologies/sigtech-python/commit/f04ffa70ae53349f2b6d00a44ea70c721829d27e))
* Make isort and black compatible ([`1f8715e`](https://github.com/SIGTechnologies/sigtech-python/commit/1f8715e8c7c61e48eadf05edadecd4580bfafb36))
* Migrate to new /performance/history endpoint ([`644451c`](https://github.com/SIGTechnologies/sigtech-python/commit/644451c2cb478f59234eed57147d4cdceda46dc9))

### Documentation

* Link fixes ([`1a91c07`](https://github.com/SIGTechnologies/sigtech-python/commit/1a91c07752dac5d1ef0370e97caa06ef3c50efc6))
* SDK examples 8 and 9 ([`514763c`](https://github.com/SIGTechnologies/sigtech-python/commit/514763c167b1c56d6225524c553d41c50dfd508e))
* Adding new example 7 ([`5d3dcd2`](https://github.com/SIGTechnologies/sigtech-python/commit/5d3dcd2d2eb0b19b5dab67293f8d3754459c6888))
* Typo fix ([`42f16f2`](https://github.com/SIGTechnologies/sigtech-python/commit/42f16f21ce4a1a97b480f0d5d024fd09cccdb9d8))
* Updating examples 2 ([`460b9b9`](https://github.com/SIGTechnologies/sigtech-python/commit/460b9b9ddc128f7ccb18a014eb6a1247b7eeee1b))
* Update to existing examples ([`8b66c66`](https://github.com/SIGTechnologies/sigtech-python/commit/8b66c661014ddf5bbf3b6e339d7e9770bb86f389))
* Markdown formatting ([`0796bc9`](https://github.com/SIGTechnologies/sigtech-python/commit/0796bc9098f2320dfe54db5d1ba02d065686c3e6))
* Url fixes ([`845d15b`](https://github.com/SIGTechnologies/sigtech-python/commit/845d15bb035d979884d8abeba51fd8a2026ddd2b))
* Readme and examples update ([`c2ee738`](https://github.com/SIGTechnologies/sigtech-python/commit/c2ee7384cba4643d70d07afe3e6b268d29a4d4f8))
* Improving example pre-req sections ([`b5c4942`](https://github.com/SIGTechnologies/sigtech-python/commit/b5c4942aa9191b1bd12b4019b133075ea8c5353e))
* Re-wording existing examples and adding 3 new ones ([`9ac89d2`](https://github.com/SIGTechnologies/sigtech-python/commit/9ac89d2131d051817ab12cbd6b645a3efe0569f6))

## v0.1.1 (2023-07-27)

### Fix

* Increase timeout for macOS tests ([`c626d7b`](https://github.com/SIGTechnologies/sigtech-python/commit/c626d7b0f0360c4632d4c899682c1c5a5a077384))

### Documentation

* Readme dashboard link update ([`0e797e2`](https://github.com/SIGTechnologies/sigtech-python/commit/0e797e26d4848988818b91d97ba68a519fe1470e))
* Adding security policy ([`adb406f`](https://github.com/SIGTechnologies/sigtech-python/commit/adb406fb5af2d537e4e8364ef1740c6194089082))
* Adding examples minus grain basket ([`189b0f0`](https://github.com/SIGTechnologies/sigtech-python/commit/189b0f06923bb819455aff7261ea72f96a23496f))
* Answering comments ([`f7ee823`](https://github.com/SIGTechnologies/sigtech-python/commit/f7ee8234aa70bfd59eaee7909a8ba8c9b17f1990))
* Readme and code of conduct updates ([`dc5265e`](https://github.com/SIGTechnologies/sigtech-python/commit/dc5265e0bc1c49a23c1967f489463cfe37b58ea2))

## v0.1.0 (2023-07-19)

### Feature

* SA-60 PyPI package ([#13](https://github.com/SIGTechnologies/sigtech-python/issues/13)) ([`fe9f99d`](https://github.com/SIGTechnologies/sigtech-python/commit/fe9f99db02af8bc4810e00804eb3b847f5164bfa))
* Update timeout to 5 mins ([`a1a94a1`](https://github.com/SIGTechnologies/sigtech-python/commit/a1a94a1453a4425c275ed533b0d9ba981d265766))
* Remove settings singleton ([`ca787bc`](https://github.com/SIGTechnologies/sigtech-python/commit/ca787bc5ab3b14d288d090aae4604df10c5c1de4))
* Add SignalStrategy and Instruments ([`a5cf9f7`](https://github.com/SIGTechnologies/sigtech-python/commit/a5cf9f7b9f4405f007f55786930fd0d579fea284))

### Fix

* URL change ([#7](https://github.com/SIGTechnologies/sigtech-python/issues/7)) ([`0a4ab87`](https://github.com/SIGTechnologies/sigtech-python/commit/0a4ab87ee95eae03875e83559670fbafec2640e3))
* Remove progress bar and add name error ([`bcc0328`](https://github.com/SIGTechnologies/sigtech-python/commit/bcc0328f2116f769a8e831990f092a3f27ac9050))
* Make sigtech a pkgutil-style namespace package ([#5](https://github.com/SIGTechnologies/sigtech-python/issues/5)) ([`2394105`](https://github.com/SIGTechnologies/sigtech-python/commit/239410585028d1d454c222e96d67a738daf328b6))
* Add initialization error and docs ([`c76c63c`](https://github.com/SIGTechnologies/sigtech-python/commit/c76c63c70b9f3d0ed4fd2a9a364c154754b80abe))
* Add typings ([`7dc915e`](https://github.com/SIGTechnologies/sigtech-python/commit/7dc915e756ed31996cdd65a979f097d6a253abfb))

### Documentation

* Use full company entity name in licence ([#15](https://github.com/SIGTechnologies/sigtech-python/issues/15)) ([`a5193e0`](https://github.com/SIGTechnologies/sigtech-python/commit/a5193e0a20043bc87509aa078ffb58e3905374ed))
* Docs update pre-beta ([#14](https://github.com/SIGTechnologies/sigtech-python/issues/14)) ([`b6cced3`](https://github.com/SIGTechnologies/sigtech-python/commit/b6cced35f55dcc3ae726221dd08a265970c41f61))
* Fix typos ([`893a295`](https://github.com/SIGTechnologies/sigtech-python/commit/893a29537f3286f5004e4326c1d04621bff3a681))
