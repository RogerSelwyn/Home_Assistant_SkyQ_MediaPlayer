<div class="WordSection1">

<span style="font-size:13.5pt;
font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
color:#222222;mso-fareast-language:EN-GB">The </span><span class="SpellE"><span style="font-family:Consolas;mso-fareast-font-family:&quot;Times New Roman&quot;;
mso-bidi-font-family:&quot;Courier New&quot;;color:#1990B8;background:#FDFDFD;mso-fareast-language:
EN-GB">skyq</span></span><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;
mso-fareast-font-family:&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:
EN-GB"> platform allows you to control a <span class="SpellE">SkyQ</span> set top box.</span>

<span style="font-size:13.5pt;
font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
color:#222222;mso-fareast-language:EN-GB">There is currently support for the following device types within Home Assistant:</span>

*   <span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;
         mso-fareast-font-family:&quot;Times New Roman&quot;;mso-fareast-language:EN-GB">[<span style="color:#0378A9">Media Player</span>](https://www.home-assistant.io/components/webostv/#media-player)</span>

<a name="media-player"></a>**<span style="font-size:18.0pt;font-family:&quot;Helvetica&quot;,sans-serif;
mso-fareast-font-family:&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:
EN-GB">Media Player</span>**

<span style="font-size:13.5pt;
font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
color:#222222;mso-fareast-language:EN-GB">To begin with ensure your <span class="SpellE">SkyQ</span> set top box or boxes have static IP addresses.</span>

<span style="font-size:13.5pt;
font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
color:#222222;mso-fareast-language:EN-GB">Download the custom component into your <home assistant config folder>\<span class="SpellE">custom_components</span>\<span class="SpellE">skyq</span>\</span>

<a name="configuration"></a>**<span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;
mso-fareast-font-family:&quot;Times New Roman&quot;;color:#222222;text-transform:uppercase;
mso-fareast-language:EN-GB">CONFIGURATION</span>**

<span style="font-size:13.5pt;
font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
color:#222222;mso-fareast-language:EN-GB">To add a <span class="SpellE">SkyQ</span> to your installation, add the following to your </span><span class="SpellE"><span style="font-family:Consolas;mso-fareast-font-family:&quot;Times New Roman&quot;;
mso-bidi-font-family:&quot;Courier New&quot;;color:#1990B8;background:#FDFDFD;mso-fareast-language:
EN-GB">configuration.yaml</span></span><span style="font-size:13.5pt;
font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
color:#222222;mso-fareast-language:EN-GB"> file:</span>

<span style="font-size:10.0pt;font-family:Consolas;
mso-fareast-font-family:&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Courier New&quot;;
color:#7D8B99;mso-fareast-language:EN-GB"># Example <span class="SpellE">configuration.yaml</span> entry</span><span style="font-size:10.0pt;font-family:Consolas;mso-fareast-font-family:
&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Courier New&quot;;color:black;mso-fareast-language:
EN-GB"></span>

<span class="SpellE"><span style="font-size:10.0pt;
font-family:Consolas;mso-fareast-font-family:&quot;Times New Roman&quot;;mso-bidi-font-family:
&quot;Courier New&quot;;color:#1990B8;mso-fareast-language:EN-GB">media_player</span></span><span style="font-size:10.0pt;font-family:Consolas;mso-fareast-font-family:&quot;Times New Roman&quot;;
mso-bidi-font-family:&quot;Courier New&quot;;color:#5F6364;mso-fareast-language:EN-GB">:</span><span style="font-size:10.0pt;font-family:Consolas;mso-fareast-font-family:&quot;Times New Roman&quot;;
mso-bidi-font-family:&quot;Courier New&quot;;color:black;mso-fareast-language:EN-GB"></span>

<span style="font-size:10.0pt;font-family:Consolas;
mso-fareast-font-family:&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Courier New&quot;;
color:black;mso-fareast-language:EN-GB"><span style="mso-spacerun:yes"></span> </span><span style="font-size:10.0pt;font-family:Consolas;mso-fareast-font-family:
&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Courier New&quot;;color:#5F6364;mso-fareast-language:
EN-GB">-</span> <span style="font-size:10.0pt;font-family:Consolas;mso-fareast-font-family:
&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Courier New&quot;;color:black;mso-fareast-language:
EN-GB"></span> <span style="font-size:10.0pt;font-family:Consolas;mso-fareast-font-family:
&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Courier New&quot;;color:#1990B8;mso-fareast-language:
EN-GB">platform</span><span style="font-size:10.0pt;font-family:Consolas;
mso-fareast-font-family:&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Courier New&quot;;
color:#5F6364;mso-fareast-language:EN-GB">:</span> <span style="font-size:10.0pt;
font-family:Consolas;mso-fareast-font-family:&quot;Times New Roman&quot;;mso-bidi-font-family:
&quot;Courier New&quot;;color:black;mso-fareast-language:EN-GB"><span class="SpellE">skyq</span></span><span style="font-size:11.5pt;font-family:Consolas;mso-fareast-font-family:&quot;Times New Roman&quot;;
mso-bidi-font-family:&quot;Courier New&quot;;color:black;mso-fareast-language:EN-GB"></span>

**<span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;text-transform:uppercase;mso-fareast-language:
EN-GB">CONFIGURATION VARIABLES</span>**

<a name="host">**<span style="font-size:13.5pt;
font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
color:#222222;mso-fareast-language:EN-GB"><span style="mso-spacerun:yes"></span> host</span>**</a>

<span style="mso-bookmark:host">_<span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;
mso-fareast-font-family:&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:
EN-GB">(string)(Required)</span>_</span><span style="mso-bookmark:host"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB"></span></span>

<span style="mso-bookmark:host"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;
mso-fareast-font-family:&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:
EN-GB">The IP of the <span class="SpellE">SkyQ</span> set top box, e.g., </span></span><span style="mso-bookmark:host"><span style="font-family:Consolas;mso-fareast-font-family:
&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Courier New&quot;;color:#1990B8;background:
#FDFDFD;mso-fareast-language:EN-GB">192.168.0.10</span></span><span style="mso-bookmark:host"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;
mso-fareast-font-family:&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:
EN-GB">.</span></span>

<span style="mso-bookmark:host"><a name="name">**<span style="font-size:13.5pt;
font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
color:#222222;mso-fareast-language:EN-GB">name</span>**</a></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name">_<span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">(string)( Required)</span>_</span></span><span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB"></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">The name you would like to give to the <span class="SpellE">SkyQ</span> set top box.</span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><a name="filename"></a><a name="sources"></a><a name="turn_on_action"></a><span style="mso-bookmark:filename"><span style="mso-bookmark:sources">**<span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;
mso-fareast-font-family:&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:
EN-GB">sources</span>**</span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources">_<span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">(list)( Required)</span>_</span></span></span></span><span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB"></span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">List of channels or other commands that will appear in the source selection.</span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources">**<span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">room</span>**</span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources">_<span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">(string)( Required)</span>_</span></span></span></span><span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB"></span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">The room where the <span class="SpellE">SkyQ</span> set top box is located.</span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources">**<span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">name</span>**</span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources">_<span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">(string)( Required)</span>_</span></span></span></span><span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB"></span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">The name you would like to give to the <span class="SpellE">SkyQ</span> set top box.</span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span class="SpellE">**<span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;
mso-fareast-font-family:&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:
EN-GB">config_directory</span>**</span></span></span></span></span><span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources">**<span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB"></span>**</span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources">_<span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">(string)( Required)</span>_</span></span></span></span><span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB"></span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">The location of your default configuration folder.</span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span class="SpellE"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;
mso-fareast-font-family:&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:
EN-GB">Hassbian</span></span></span></span></span></span><span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"> <span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">default would be - <span class="SpellE">config_directory</span>: '/home/<span class="SpellE">homeassistant</span>/.<span class="SpellE">homeassistant</span>/'</span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span class="SpellE">**<span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;
mso-fareast-font-family:&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:
EN-GB">generate_switches_for_channels</span>**</span></span></span></span></span><span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources">**<span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB"></span>**</span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources">_<span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">(<span class="SpellE">boolean</span>)( Required)</span>_</span></span></span></span><span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB"></span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">Generate switches for each item listed in source, this helps when using an assistant <span class="SpellE">e.g</span> google home</span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">Usage based on google home: _“turn on <source name / channel name> in the <room>”_</span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">To integrate these, add the generated <span class="SpellE">yaml</span>, to your <span class="SpellE">configuration.yaml</span></span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">EXAMPLE</span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">switch:</span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB"><span style="mso-spacerun:yes"></span> - platform: template</span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB"><span style="mso-spacerun:yes"></span> <span style="mso-spacerun:yes">  </span>switches: !include <span class="SpellE">skyq</span><room*>.<span class="SpellE">yaml</span></span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources">_<span style="font-size:13.5pt;font-family:
&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:&quot;Times New Roman&quot;;color:#222222;
mso-fareast-language:EN-GB">*remove any spaces from the room</span>_</span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;
mso-fareast-font-family:&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:
EN-GB"></span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><a name="example"></a>**<span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;
mso-fareast-font-family:&quot;Times New Roman&quot;;color:#222222;text-transform:uppercase;
mso-fareast-language:EN-GB">EXAMPLE</span>**</span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;
mso-fareast-font-family:&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:
EN-GB">A full configuration example will look like the sample below:</span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:
name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:10.0pt;font-family:Consolas;mso-fareast-font-family:&quot;Times New Roman&quot;;
mso-bidi-font-family:&quot;Courier New&quot;;color:#7D8B99;mso-fareast-language:EN-GB"># Example <span class="SpellE">configuration.yaml</span> entry</span></span></span></span></span><span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:10.0pt;font-family:Consolas;mso-fareast-font-family:&quot;Times New Roman&quot;;
mso-bidi-font-family:&quot;Courier New&quot;;color:black;mso-fareast-language:EN-GB"></span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:
name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span class="SpellE"><span style="font-size:10.0pt;font-family:Consolas;mso-fareast-font-family:
&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Courier New&quot;;color:#1990B8;mso-fareast-language:
EN-GB">media_player</span></span></span></span></span></span><span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:10.0pt;font-family:Consolas;mso-fareast-font-family:&quot;Times New Roman&quot;;
mso-bidi-font-family:&quot;Courier New&quot;;color:#5F6364;mso-fareast-language:EN-GB">:</span></span></span></span></span><span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:10.0pt;font-family:Consolas;mso-fareast-font-family:&quot;Times New Roman&quot;;
mso-bidi-font-family:&quot;Courier New&quot;;color:black;mso-fareast-language:EN-GB"></span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span class="SpellE"><span style="font-size:10.0pt;
font-family:Consolas;mso-fareast-font-family:&quot;Times New Roman&quot;;mso-bidi-font-family:
&quot;Courier New&quot;;color:black;mso-fareast-language:EN-GB">media_player</span></span></span></span></span></span><span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:10.0pt;font-family:Consolas;mso-fareast-font-family:&quot;Times New Roman&quot;;
mso-bidi-font-family:&quot;Courier New&quot;;color:black;mso-fareast-language:EN-GB">:</span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:10.0pt;font-family:Consolas;
mso-fareast-font-family:&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Courier New&quot;;
color:black;mso-fareast-language:EN-GB"><span style="mso-spacerun:yes"></span> - platform: <span class="SpellE">skyq</span></span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:10.0pt;font-family:Consolas;
mso-fareast-font-family:&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Courier New&quot;;
color:black;mso-fareast-language:EN-GB"><span style="mso-spacerun:yes"></span> <span style="mso-spacerun:yes">  </span>name: <span class="SpellE">SkyQ</span> Living Room</span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:10.0pt;font-family:Consolas;
mso-fareast-font-family:&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Courier New&quot;;
color:black;mso-fareast-language:EN-GB"><span style="mso-spacerun:yes"></span> <span style="mso-spacerun:yes">  </span>host: 192.168.0.10</span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:10.0pt;font-family:Consolas;
mso-fareast-font-family:&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Courier New&quot;;
color:black;mso-fareast-language:EN-GB"><span style="mso-spacerun:yes"></span> <span style="mso-spacerun:yes">  </span>room: Living Room</span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:10.0pt;font-family:Consolas;
mso-fareast-font-family:&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Courier New&quot;;
color:black;mso-fareast-language:EN-GB"><span style="mso-spacerun:yes"></span> <span style="mso-spacerun:yes">  </span><span class="SpellE">config_directory</span>: '/home/<span class="SpellE">homeassistant</span>/.<span class="SpellE">homeassistant</span>/'</span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:10.0pt;font-family:Consolas;
mso-fareast-font-family:&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Courier New&quot;;
color:black;mso-fareast-language:EN-GB"><span style="mso-spacerun:yes"></span> <span style="mso-spacerun:yes">  </span><span class="SpellE">generate_switches_for_channels</span>: true</span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:10.0pt;font-family:Consolas;
mso-fareast-font-family:&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Courier New&quot;;
color:black;mso-fareast-language:EN-GB"><span style="mso-spacerun:yes"></span> <span style="mso-spacerun:yes">  </span>sources:</span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:10.0pt;font-family:Consolas;
mso-fareast-font-family:&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Courier New&quot;;
color:black;mso-fareast-language:EN-GB"><span style="mso-spacerun:yes"></span> <span style="mso-spacerun:yes">  </span><span class="SpellE">SkyOne</span>: '1,0,6'</span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:10.0pt;font-family:Consolas;
mso-fareast-font-family:&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Courier New&quot;;
color:black;mso-fareast-language:EN-GB"><span style="mso-spacerun:yes"></span> <span style="mso-spacerun:yes">  </span><span class="SpellE">SkyNews</span>: '5,0,1'</span></span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;
mso-fareast-font-family:&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:
EN-GB">Avoid using </span></span></span></span></span><span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-family:Consolas;mso-fareast-font-family:&quot;Times New Roman&quot;;
mso-bidi-font-family:&quot;Courier New&quot;;color:#1990B8;background:#FDFDFD;mso-fareast-language:
EN-GB">[ ]</span></span></span></span></span><span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;
mso-fareast-font-family:&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:
EN-GB"> in the </span></span></span></span></span><span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-family:Consolas;mso-fareast-font-family:&quot;Times New Roman&quot;;
mso-bidi-font-family:&quot;Courier New&quot;;color:#1990B8;background:#FDFDFD;mso-fareast-language:
EN-GB">name: or room:</span></span></span></span></span><span style="mso-bookmark:
host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="mso-bookmark:sources"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;
mso-fareast-font-family:&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:
EN-GB"> of your device.</span></span></span></span></span>

<span style="mso-bookmark:sources"></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><a name="turn-on-action"></a>**<span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;text-transform:uppercase;mso-fareast-language:
EN-GB">SOURCES</span>**</span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">To configure sources, set the name as <name>: ‘<button>,<button>,<button>’.</span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">Supported buttons:</span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">sky, power, <span class="SpellE">tvguide</span> or home, <span class="SpellE">boxoffice</span>, search, sidebar, up, down, left, right, select, <span class="SpellE">channelup</span>, <span class="SpellE">channeldown</span>, <span class="SpellE">i</span>, dismiss, text, help,</span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">play, pause, rewind, <span class="SpellE">fastforward</span>, stop, record</span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">red, green, yellow, blue</span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">0, 1, 2, 3, 4, 5, 6, 7, 8, 9</span></span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><a name="change-channel-through-play_media-servic"></a><a name="nextprevious-buttons"></a>**<span style="font-size:13.5pt;font-family:
&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:&quot;Times New Roman&quot;;color:#222222;
text-transform:uppercase;mso-fareast-language:EN-GB">NEXT/PREVIOUS BUTTONS</span>**</span></span></span>

<span style="mso-bookmark:host"><span style="mso-bookmark:name"><span style="mso-bookmark:filename"><span style="font-size:13.5pt;font-family:&quot;Helvetica&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#222222;mso-fareast-language:EN-GB">The behaviour of the next and previous buttons is <span class="SpellE">fastforward</span> and rewind (multiple presses to increase speed, play to resume)</span></span></span></span>

<span style="mso-bookmark:filename"></span><span style="mso-bookmark:name"></span><span style="mso-bookmark:host"></span>

<a name="notifications"></a>

</div>
