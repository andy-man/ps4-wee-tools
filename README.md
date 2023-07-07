![PS4 Wee Tools](assets/splash.png)

# PS4 Wee Tools

PS4 wee tools help to work with PS4 nor and syscon dumps.

It is free open source alternative for BwE's PS4-NOR-Validator & Syscon-Patcher written in Python to keep it simple.

Currently it provides base functional and can not fully replace those tools.

![Main tool](assets/main.png)

Was tested with Python 3.8

## Features

Common
* Multy files compare

NOR tool
* PS4 Nor dump info
* Toggle UART
* Toggle Memory test, RNG/Keystorage test
* System flags cleaning
* Memory clock editing (GDDR5)
* SAMU boot flag edit
* Downgrade by slot switch
* Entropy stats

Syscon tool
* Syscon check
* Patchable check
* Show active SNVS slot
* Manual SNVS patch
* Auto SNVS patch (upcoming)

Don't use if you don't understant what is it for

## Credits

This wouldn't be possible without work of these folks: 
* fail0verflow
* BwE
* Darknesmonk
* pearlxcore

And of course [PSDevWiki](https://www.psdevwiki.com/ps4/)

## Donate

* **[Patreon](https://patreon.com/andy_man)**
* **[Boosty](https://boosty.to/andy_man/donate)**
* **[YandexMoney](https://yoomoney.ru/to/410011555252085)**
* **Bitcoin**: 39VaMnFqCQo751mvDc3M7ADVty71q2tWDm 

## Links

* [Twitter](https://twitter.com/AndyManDev)

## Changelog

### v0.4
* Syscon patchable check
* Manual patch bug fix
* Minor errors fix

### v0.3
* NOR Entropy stats
* Syscon manual patch
* Minor errors fix

### v0.2
* Syscon DEBUG toggle
* Syscon NVStorage class
* Syscon show active slot

### v0.1
* Files compare
* UART, Memtest toggle
* Sys flags clean
* Edit mem clock and SAMU
* Downgrade switch patterns
* Syscon base check
