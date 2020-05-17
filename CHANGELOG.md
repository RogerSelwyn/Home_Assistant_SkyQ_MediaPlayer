# Changelog

## v2.1.8.beta (17/05/2020)

### Enhancements
- [Added link to issues in manifest](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/22ca72c4c9c6b8089e47dd9a7e2e8b1e51696f02) - @RogerSelwyn
- [Added Unique_ID property](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/c9dbaf98cd5c9d5996707637cd375dd79707c0f7) - @RogerSelwyn
- [Added 'available' property](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/d97919c0bd8c4cfd4d5b753d7cebcaecb5efbe53) - @RogerSelwyn
- [Added 10 second scan_interval](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/4e0891f7b73c880ba7183287ab1135452f4c9cfa) - @RogerSelwyn
- [Changed to update entity at startup](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/0ed9de33e90101d7edff01af406723da8a31e381) - @RogerSelwyn

### Maintenance
- [Bump pyskyqremote to 0.2.14](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/183c23790a0fe545f95346f1fd79195e178b9955) - @RogerSelwyn
- [Removed deprecated code](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/d20cbad11fa4226d1dacd3b21f157de1cf7d87fd) - @RogerSelwyn
- [Removed storing hass as self._hass - unnecessary](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/7d62304d89f756fd8f2f92e078f132ddfb849479) - @RogerSelwyn
- [Changed to use get_url instead of base_url](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/2658ccfa1b3c88fef66120a61fe0be7c7bcced13) - @RogerSelwyn
- [Changed to use Entity instead of Device](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/a4e25564d26baf96432df7e4212bcb897b3eb178) - @RogerSelwyn
- [Add requirements to manifest](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/5dbeaa1817e9b487bfbf615071b6cd7aa5eee7ff) - @RogerSelwyn
- [Update info.md](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/540f4f2de4544bb12636692fe3ecde67cd9ccfd0) - @RogerSelwyn
- [Update README.md](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/bd01d3a3d28f301c785483a051d52f8a9271ea26) - @RogerSelwyn
- [Create hacsvalidate.yaml](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/fb0a1c6a9c0a8b370c21c17757cedb5b66c1cc4c) - @RogerSelwyn
- [Bump aiohttp from 3.6.1 to 3.6.2](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/fa21acb6036e8e62987f8f75b8914900cf283921) - @dependabot-preview[bot]
- [Remove tracking of homeassistant version](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/6322855f7515588699b93bb958b369e442ef5c8d) - @RogerSelwyn
- [Added requirements.txt](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/5f54ced49f59ffd16c680f4778606c8711e58bca) - @RogerSelwyn

## v2.1.7 (10/05/2020)
### Enhancements
- [Enabled commands to be sent via play_media](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/73729a12babc8d421b3cab6ed449414e52698e8a) - @RogerSelwyn

## v2.1.6 (10/05/2020)
### Enhancements
- [Remove need for country parameter](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/465f2db6ebc20a1ed720d2cf59ee58745cc8b614) - @RogerSelwyn
- [Changed component to be async](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/d3d2ebdf1688a7e81a2955a033b7df6f383c3fd2) - @RogerSelwyn
- [Updated to access images direct from source where possible](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/161308bbc9d524a0e9e168b95803ff59e28cc83f) - @RogerSelwyn

### Fixed
- [Corrected init.py to setup integration correctly](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/e1d705c0082819197ae8140897fc744b79f1ca46) - @RogerSelwyn
- [Fixed device setup blocking I/O](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/6cc24050c41ac6fd924ba963245544add2501639) - @RogerSelwyn
- [Fixed issue with empty EPG](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/89ec0277f8dcd16e70bc1de9b0104d7b2fd40670) - @RogerSelwyn
- [Handle switched off/standby devices](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/bfec2f263776713b7c27352e50968c43b9756040) - @RogerSelwyn
- [Fixed non-return of recording data](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/3003805b989dda6a7ea020be2e929e0a82285550) - @RogerSelwyn
- [Corrected manifest.json](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/f3488d3faaedb7187b7b5af7b37d358432c226dd) - @RogerSelwyn


### Maintenance
- [Bump pyskyqremote to 0.2.13](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/42a3f23acd92cadd610d01840313526aa6483e67) - @RogerSelwyn
- [Updated to simplify use of pyskyqremote](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/9c94c2a08e1b57269c0ddcc56bd4e46fc67e22bd) - @RogerSelwyn
- [Moved constants to const.py](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/6281214d6393e100f6f237c7fe34f10afefacdc8) - @RogerSelwyn
- [Tidied up unnecessary method](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/5b438afb7b0a17e60db6670c899c43226f1cb132) - @RogerSelwyn
- [Moved all switch generation into the utility script](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/497c1b5f48f25b4c2e3a935e229da8787014c9a9) - @RogerSelwyn
- [Removed duplication in the config generator](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/42ce370a51e1b2a337874624714c6bf50d3fab02) - @RogerSelwyn
- [Tidied up code in line with Python best practice](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/a4f5847ccadeb5b55d876a5156cbca7bc26fc59e) - @RogerSelwyn
- [Update bug_report.md](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/45b0291cacee84b6d8e1d1c05a62104008415ec1) - @RogerSelwyn
- [Changed license to markdown](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/cc41fb45e67cc5674b593964ce0b9d957b25f4b1) - @RogerSelwyn

## v2.1.5 (23/04/2020)
- [Update in line with flake8](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/7fe2c9d828656766a0dd025cd50e3ccfa14a70f6) - @RogerSelwyn
- [Bump pyskyqremote to 0.2.6](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/f7ffa4668f9a65e87e0bd3bdc78beb58f54ea5ab) - @RogerSelwyn
- [Update to include link to documentation](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/a290202b05fca88d48d58e47ccf921aef9040d4e) - @RogerSelwyn
- [Added validation via hassfest](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/fba495f585f4b02d609906e87031b8383e93134d) - @RogerSelwyn
- [Added issue templates](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/24c5e1bdbd189a8ba8dc443f8a82a4ba4a0b15b2) - @RogerSelwyn


## v2.1.4 (21/04/2020)
- [Fixed unable to Power On](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/b1498bfc64de59f754bcf948ca0cd411ffc541e5) - @RogerSelwyn
- [Fixed app image not showing](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/1df7aae08a6992ab264baad3e24fd1b5708e6a29) - @RogerSelwyn


## v2.1.3 (17/04/2020)
- [Removed redundant get_live_tv](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/0ec065843dcd0b0cd75c1d1d0bb27f00b15ef3e1) - @RogerSelwyn
- [Bump pyskyqremote to 0.2.5](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/5dff1aecbc54f70ad24529ece52c13e5c61ddab0) - @RogerSelwyn
- [Tidy up unused code](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/44a33ce6138108526c145c0f3a82f40a89b367c4) - @RogerSelwyn

## v2.1.2 (17/04/2020)
- [Bump pyskyqremote to 0.2.4](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/8f5b2f5e42e7ae31e2fb9a2451a5b7e10c9901dc) - @RogerSelwyn
- [Updated to match pyskyqremote simplification](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/b624a02a22602b54cccbd8b56ecb7ae88e45568c) - @RogerSelwyn

## v2.1.1 (16/04/2020) *(Beta)*
- [Bump pyskyqremote to 0.2.2](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/2fa957a91b91d57b25ad5391b1060c58be2ce6c4) - @RogerSelwyn

## v2.1.0 (15/04/2020) *(Beta)*
- [Bump pyskyqremote to 0.2.1](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/5fefd8b02a0989805bba429bfa1323838418f508) - @RogerSelwyn
- [Pass Channel number back in support of countries](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/2c13d3940fb2ec18267ae6c2dace285d1831aef9) - @RogerSelwyn


## v2.0.0 (13/04/2020)
- Release to master - @RogerSelwyn

## v1.5.14 (12/04/2020)
- Fixed error with EPG image at startup - @RogerSelwyn

---

## v1.5.13 (12/04/2020)
- Moved sky_remote to PyPI - @RogerSelwyn
- Fix X0030 at end of EPG - @RogerSelwyn
- Deal with programmeuuid not being returned - @RogerSelwyn
- Add SID to error message - @RogerSelwyn

---

## v1.5.12 beta (11/04/2020)
- Prepare for breaking sky_remote out - @RogerSelwyn

---

## v1.5.11 (11/04/2020)
- Added host name to debug info - @RogerSelwyn

---

## v1.5.10 (09/04/2020)
- Add Roku - @RogerSelwyn
- Added icon for switched off and device class - @RogerSelwyn

---

## v1.5.9 (07/04/2020)
- Use entity icon as media type indicator - @RogerSelwyn
- Corrected screenshots - @RogerSelwyn
- Update screenshots - @RogerSelwyn

---

## v1.5.8 (07/04/2020)
- Always pass appimageurl if image is available - @RogerSelwyn
- Added state attribute to indicate what is playing - @RogerSelwyn

---

## v1.5.7 (06/04/2020)
- Set IoT Class - @RogerSelwyn
- Restructured getCurrentLiveTVProgramme - @RogerSelwyn
- Spelling correction - @RogerSelwyn
- Updated info files - @RogerSelwyn

---

## v1.5.6 (05/04/2020)
- Change live TV emoji - @RogerSelwyn

---

## v1.5.5 (05/04/2020)
- Added live TV emoji - @RogerSelwyn

---

## v1.5.4 (05/04/2020)
- Added Emoji] - @RogerSelwyn

---

## v1.5.3 (05/04/2020)
- Removed test - @RogerSelwyn
- Updated screenshots - @RogerSelwyn
