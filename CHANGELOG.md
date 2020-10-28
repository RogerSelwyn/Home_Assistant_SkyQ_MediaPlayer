# Changelog

## v2.4.5 (28/10/2020)
### Enhancements
- [Improve error reporting when no base URL set](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/edeb1918a13381b7d9b38d54f2cc4ed06407b58c) - @RogerSelwyn - [#35](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/issues/35)

## v2.4.4 (24/10/2020)
### Enhancements
- [Add German translations](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/affabcf771f06c8e4847a5bd84effa168c45d301) - @RogerSelwyn - Feature request - [#29](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/issues/29)
- [Add support for EPG Cache Length](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/b9a8daf6045188a603397d35bbaa73604a5b388f) - @RogerSelwyn - Feature request - [#31](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/issues/31)

### Maintenance
- [Update CHANGELOG.md](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/909eb31f55f86ae4d98078b273ab69c7e83c0f4f) - @RogerSelwyn
- [Update README.md](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/2bd99a2c3134c85303c1df5fbef0ef30b52cc5ee) - @RogerSelwyn
- [Auto update requirements.txt](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/633c572a18269e94a4101cfacbb2891d196462c4) - @actions-user

## v2.4.3 (30/09/2020)
### Fixes
- [Catch channel name that has been changed/removed](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/a7109459363143a24db9ec88d5ff7f97f189407e) - @RogerSelwyn

## v2.4.2 (28/09/2020)
### Fixes
- [Fix error in async_play_media](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/6646591a7ca6cba778ef19dfa7b17a3386792d83) - @RogerSelwyn

### Maintenance
- [Code improvement from Codefactor](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/d82bbc7933cddcfa1cf1bc15afb334f74badf028) - @RogerSelwyn
- [Break config out into class](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/81a6c21083036b54ddced8a6354fd85e56763f57) - @RogerSelwyn
- [Break volume entity out into class](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/95302a5965fdf694b2ec1165ecf4436c68d93bbd) - @RogerSelwyn
- [Break media browser out into a class](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/048c1378b8551bd9e38da4142a2c85308f8b52f9) - @RogerSelwyn

## v2.4.1 (25/09/2020)
### Fixes
- [Fix issue with error when no programme found](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/970cae1c3bcb54a98fda7e2a8f2ef2645b7d891f) - @RogerSelwyn

## v2.4.0 (24/09/2020)
### Enhancements
- [Add support for media browser](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/ad71bf30dbfbdf3c8c3805bbe0a2dbbaa2e0018b) - @RogerSelwyn
- [Change to use live info for browser](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/c9986860a65d986097b8e3fba4ad71371d9ac77e) - @RogerSelwyn
- [Rework retrieving data for browser](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/fdbcb51096309e759a661ec45b71cc23b8b847a6) - @RogerSelwyn

### Maintenance
- [Add Information log message on certificate error](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/251af863512e40fe5ad575620c31c33aa0ac68dc) - @RogerSelwyn
- [Update pyskyqremote to 0.2.30](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/ceb5599ca782759d98ff61c8f71aaed784c40bb5) - @RogerSelwyn
- [Auto update requirements.txt](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/818b92c672e09070639f9cc1f5a999cf2bf4c7ca) - @actions-user
- [Update CHANGELOG.md](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/34bc18e39035fc0cc426e1621782f529b47c25a5) - @RogerSelwyn
- [Added media browser screenshot](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/b2a44285c6885ec04046d09a1df0711e6d61501d) - @RogerSelwyn
- [Update README.md](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/c2355ae1060d8aac6d2c3cef8007942a8d9a6071) - @RogerSelwyn

### Fixes
- [Disable browser when no sources](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/68d5afa121bb11f8d3436e0ed9df68c80caca8f8) - @RogerSelwyn
- [Disable browser when switched off](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/2fe10a48582db9250de92dd50422ce3548a273ec) - @RogerSelwyn 

## v2.3.7 (24/08/2020)
### Enhancements
- [Add skynews logo](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/f04f09adfab6c87d59be494cf007237616d3eb88) - @RogerSelwyn

### Fixes
- [Fix certificate errors](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/3c813094b784553e961b800147462ba24c9277ee) - @RogerSelwyn

## v2.3.6 (15/08/2020)
### Fixes
- [Fix excessive errors in log on startup](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/a2be83406903e1e9e08489fd83bb7ac72e8a1a96) - @RogerSelwyn

## v2.3.5 (15/08/2020)
### Enhancements
- [Add playworks logo and title](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/9c6e943c6d61a79708dfd4b5396cd99beae7ce22) - @RogerSelwyn

### Fixes
- [Re-include check for power status](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/f5451151895378f8a555b6c115eb6681d4e0bc51) - @RogerSelwyn

## v2.3.4 (06/08/2020)
### Maintenance
- [Bump pyskyqremote to 0.2.27](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/6afc1e7ef1a5c003e4c011df5922145fc2701497) - @RogerSelwyn
- [Auto update requirements.txt](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/307db3154a58fe8ab03b9ad297beb664c91659d4) - @actions-user

## v2.3.3 (06/08/2020)
### Fixes
- [Fix showing volume properties incorrectly](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/5f51a381a715f48b84fed05995756a97515c8ad1) - @RogerSelwyn

### Maintenance
- [Unconstrain pygithub](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/e9c79706c3e0d93baaf331af78ac6f6cc0417cd6) - @RogerSelwyn

## v2.3.2 (03/08/2020)
### Enhancements
- [Use enhancements in pyskyqremote to remove powerstate calls](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/8a977f6d345c2ef45292a427ab0b61d0c693c56a) -  @RogerSelwyn

### Maintenance
- [Change minimum requirements for modules](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/b2a0d0fa3c2a2872828eb5b5b5dcce1dc53db44f) - @RogerSelwyn
- [Bump pyskyqremote to 0.2.26](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/781b3c2f5989e08c3e2257894cb9cbb10080b2d1) - @RogerSelwyn
- [Auto update requirements.txt](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/58b86465e49681bf6f6cda906571cf582a31684d) - @actions-user

### Fixes
- [Change device unavailable to error](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/236718b6795a9e420cc4615b4cdc6529f7bde9b7) - @RogerSelwyn

## v2.3.1 (29/07/2020)
### Fixes
- [Bump pyskyqremote to 0.2.25](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/8efc62701bfcc4800175231e56e8b61e91b001b7) - @RogerSelwyn
- [Auto update requirements.txt](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/1ff6a48257082108708a85209a9f7970f828fce6) - @actions-user

## v2.3.0 (22/07/2020)
### Enhancements
- [Add ability to control volume on specified entity](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/e12ddac34261eddec169d58b159638e12584a4ff) - @RogerSelwyn

### Fixes
- [Fix errors in switch generation](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/4e2a1fa5834ee58cc07deca731fceadddaa816dd) - @RogerSelwyn

## v2.2.4 (05/07/2020)
### Maintenance

- [Delete info.md](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/d626d5f58fc00096151fe846d503ffbdf232dd56) - @RogerSelwyn
- [Bump pycountry to 20.7.3](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/3b142529f1c4884fe9ad0c4e03eafe3c540af8bb) - @RogerSelwyn
- [Auto update requirements.txt](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/ef26a3ef2d83e642c3339b317cdb124124922b43) - @actions-user

## v2.2.3 (01/07/2020)

### Maintenance

- [Create dependabot.yml](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/e272e8daeb511fd8a11477ab4aadec705fb65a96) - @RogerSelwyn
- [Update README.md](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/a042182930753e93c43546a7771d748724211411) - @RogerSelwyn
- [Format with black and isort](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/994930dd05220e76303967b1f2a04a3253e7b568) - @RogerSelwyn
- [Change line length for Black](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/609102f0d7b4e6df2124ab2a826427a3bd1568cf) - @RogerSelwyn
- [Bump pyskyqremote to 0.2.23](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/5b52235b430b58f2038fdf61c4d717f1227cfd04) - @RogerSelwyn
- [Auto update requirements.txt](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/526a7a71d4182401528bdef44180fc845671754a) - @actions-user
- [Update generate_releasenotes.py](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/324b6038dea42569f8dd00f5956449f1fa3e9b99) - @RogerSelwyn

## v2.2.2 (10/06/2020)

### Fixes
- [Bump pyskyqremote to 0.2.21](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/e475439497b2764de06b67c973a55258e4d42c5d) - @RogerSelwyn
- [Fixed issue with Italian EPG](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/2146a7e1af08da84f3fd8814246c455daadeee2a) - @RogerSelwyn
- [Handle empty programme from pyskyqremote](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/90cd8d23ac7b3e0d53a7fad3465eb76950564772) - @RogerSelwyn

### Maintenance
- [Added automated updates](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/575023728b195ac456a950c64cf3acea945078bf) - @RogerSelwyn
- [Corrected Repository](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/52f6c991a19b40341889427ba91a5c90d12d48ee) - @RogerSelwyn
- [Remove commands](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/f5a99c7d07bf39a5a64527afdbae0bc3602696a1) - @RogerSelwyn
- [Auto update requirements.txt](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/edaaa225e9ed340ae06595ecbba98bd8f9bd3866) - @actions-user

## v2.2.1 (02/06/2020)

### Fixes
- [Fixed issue with channel list duplicates in config flow](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/36960b4961c6169fbc5d54d04dfc4aff009f767b) - @RogerSelwyn

## v2.2.0 (02/06/2020)

### Enhancements
- [Updated to add config flow](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/bef91ba6c56afbe232fd609067069ab30af05da8) - @RogerSelwyn
- [Added Italian](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/57eeb69a4a2e2e30de49cd6575c6a0d64a908718) - @RogerSelwyn
- [Validate custom commands on setup](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/33646a013716694159e954a684b4e98ede3598f0) - @RogerSelwyn
- [Generate switches for channel sources](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/bcc4478445a12e9cf121db3d1efdb290a4a42802) - @RogerSelwyn

### Fixes
- [Fixed source commands not working](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/ff77726ea984cbd98485ce055066ed771b742cdf) - @RogerSelwyn
- [Revert unique_id creation for YAML entities](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/38017f971d1918e904d2f44ea19c925e47786958) - @RogerSelwyn
- [Fixed source_list creation](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/a8757448baf0f874dd3d06305ffe86e052e8ce94) - @RogerSelwyn

### Maintenance 
- [Bump pyskyqremote to 0.2.19](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/4d99d851cd1357293ed92d9ff17c7ae684b15982) - @RogerSelwyn
- [Converted config to dataclass](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/ee0defa63fcee101950e70e4ec2c9c1c87ca260f) - @RogerSelwyn
- [Update hacs.json](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/f84854a8cd27345124ee19514db01127fd4ab953) - @RogerSelwyn
- [Moved schema to schema.py](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/976fba5825a44a709745150bb6bd1b2c01ca8488) - @RogerSelwyn
- [Update hacs.json](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/04510f138c685aed98abfa4748c4370717c016bd) - @RogerSelwyn
- [Change to zip file deploy](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/73a296bdda69f0c16670d8d6ebc9e93456f6c4bf) - @RogerSelwyn
- [Create skyqrelease.yaml](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/d18dfdb42874f7e6481fe60554366f5ba66702eb) - @RogerSelwyn
- [Added update of state after command](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/3714174327f1e5b6c0a409c872a91a8d30652a2b) - @RogerSelwyn
- [Code tidy up](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/b3847184a27cd31cd3854b180fd199349d619b9a) - @RogerSelwyn
- [Changed to keep channel/custom source order](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/e2634fe8c7e4e63b8f51cf84392bc498f638bdfb) - @RogerSelwyn
- [Changed to sort channel sources by number](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/0c8b1f7e9fbf5eaf81842eb058d755b3e2db6d9b) - @RogerSelwyn
- [Allow pass through of unknown sources](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/66dc7193db96db1ba202917c6eb69b53cd191bbe) - @RogerSelwyn
- [Put entity name in title of Options dialogue](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/057757c431f7e6c68c16d268c536e05e25d47719) - @RogerSelwyn
- [Display country code as country name](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/6ea5ae16b29c81550d7b473894f43247145a2dde) - @RogerSelwyn
- [Added valid countries to options drop down](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/402ed9ae82b0c37aef58c929873d305a5e9cd80a) - @RogerSelwyn
- [Tidied up startup code](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/89f2fbfa9cc36c11712b99975f5da23e7b2691fa) - @RogerSelwyn
- [Updated to display channel numbers in options](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/8664a7c5a82dac285d9bdacb7a614e2f8d7443bb) - @RogerSelwyn
- [Fixed issues with source storage](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/809add5888bff29dcde62ed163c9de2f04192826) - @RogerSelwyn
- [Added english translaton](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/13426594bbfcc5aee10c12b4643a8f2085b05754) - @RogerSelwyn
- [Corrected translations](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/4c0b41196a1022c66a4e02ea1190923819ec6232) - @RogerSelwyn
- [Added translation files](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/d54f751428ed64a854c71d5476f89aebb002da61) - @RogerSelwyn
- [Restructure in support of config flow](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/7f123164e7b10ecc0300387921135e82e3b4b21e) - @RogerSelwyn
- [Minor code improvement](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/f1fbbbc2f75147472cbf2a0e0d60e4aed71b7ef4) - @RogerSelwyn

## v2.1.8 (21/05/2020)

### Enhancements
- [Added link to issues in manifest](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/22ca72c4c9c6b8089e47dd9a7e2e8b1e51696f02) - @RogerSelwyn
- [Added Unique_ID property](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/c9dbaf98cd5c9d5996707637cd375dd79707c0f7) - @RogerSelwyn
- [Added 'available' property](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/d97919c0bd8c4cfd4d5b753d7cebcaecb5efbe53) - @RogerSelwyn
- [Added 10 second scan_interval](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/4e0891f7b73c880ba7183287ab1135452f4c9cfa) - @RogerSelwyn
- [Changed to update entity at startup](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/0ed9de33e90101d7edff01af406723da8a31e381) - @RogerSelwyn

### Maintenance
- [Bump pyskyqremote to 0.2.18](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/a9bb53edc32e660648d66915c2be73eab59778ea) - @RogerSelwyn
- [Fixed issue with app image check at startup](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/be9137b3d178068062a221ddf48f290f179bf831) - @RogerSelwyn
- [Updated to use getDeviceInformation](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/349e82cf9c8c71d419d926c5d0fc03edd22f97cb) - @RogerSelwyn
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
- [Update bug_report.md](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/commit/0658e36ae9e0a2290bc531076c6557aed2bd11a5) - @RogerSelwyn

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
- Added Emoji - @RogerSelwyn

---

## v1.5.3 (05/04/2020)
- Removed test - @RogerSelwyn
- Updated screenshots - @RogerSelwyn
