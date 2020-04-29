# Changelog

## v2.1.6 (29/04/2020) *(Beta4)*
### Enhancements
- [Remove need for country parameter](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/465f2db6ebc20a1ed720d2cf59ee58745cc8b614) - @RogerSelwyn

### Fixed
- [Fixed issue with empty EPG](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/89ec0277f8dcd16e70bc1de9b0104d7b2fd40670) - @RogerSelwyn
- [Handle switched off/standby devices](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/bfec2f263776713b7c27352e50968c43b9756040) - @RogerSelwyn

### Maintenance
- [Bump pyskyqremote to 0.2.10](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/655dc04e0cc7962a82699cc3c2d95a1b179bc44f) - @RogerSelwyn
- [Updated to simplify use of pyskyqremote](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/9c94c2a08e1b57269c0ddcc56bd4e46fc67e22bd) - @RogerSelwyn
- [Moved constants to const.py](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/6281214d6393e100f6f237c7fe34f10afefacdc8) - @RogerSelwyn
- [Tidied up unnecessary method](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/5b438afb7b0a17e60db6670c899c43226f1cb132) - @RogerSelwyn
- [Moved all switch generation into the utility script](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/497c1b5f48f25b4c2e3a935e229da8787014c9a9) - @RogerSelwyn
- [Removed duplication in the config generator](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/42ce370a51e1b2a337874624714c6bf50d3fab02) - @RogerSelwyn
- [Tidied up code in line with Python best practice](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/a4f5847ccadeb5b55d876a5156cbca7bc26fc59e) - @RogerSelwyn



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
