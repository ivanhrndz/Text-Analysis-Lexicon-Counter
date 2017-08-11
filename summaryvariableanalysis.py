from __future__ import division
import wx
import numpy
import glob 
import os
import re
import string
import wx.grid


APP_SIZE_X = 550
APP_SIZE_Y = 265


we_re=re.compile("\\blet's\\b|lets\b|\bour\b|\bours\b|\bourselves\b|\bus\b|\bwe\b|\bwe'd\b|\bwe'll\b|\bwe're\b|\bwe've\b|\bweve\\b",re.IGNORECASE)
you_re=re.compile("\\bily*\\b|\\bthee\\b|\\bthine\\b|\\bthou\\b|\\bthoust\\b|\\bthy\\b|\\bthyself\\b|\\bu\\b|\\bur\\b|\\by'al\\b|\\by'all's\\b|\\bya\\b|\\bya'll*\\b|\\byall\\b|\\byalls\\b|\\bye\\b|\\byinz*\\b|\\byou\\b|\\byou'd\\b|\\byou'l\\b|\\byou're\\b|\\byou've\\b|\\byoud\\b|\\byoul\\b|\\byour\\b|\\byoure\\b|\\byours\\b|\\byourself\\b|\\byourselves\\b|\\byouve\\b",re.IGNORECASE)
i_re=re.compile("\\bi\\b|\\bi'd\\b|\\bi'd've\\b|\\bi'll\\b|\\bi'm\\b|\\bi've\\b|\\bid\\b|\\bidc\\b|\\bidgaf\\b|\\bidk\\b|\\bidontknow\\b|\\bidve\\b|\\bikr\\b|\\bily*\\b|\\bim\\b|\\bima\\b|\\bimean\\b|\\bimma\\b|\\bive\\b|\\bme\\b|\\bmethinks\\b|\\bmine\\b|\\bmy\\b|\\bmyself\\b",re.IGNORECASE)
shehe_re=re.compile("\\bhe\\b|\\bhe'd\\b|\\bhe's\\b|\\bher\\b|\\bhers\\b|\\bherself\\b|\\bhes\\b|\\bhim\\b|\\bhimself\\b|\\bhis\\b|\\bhissel*\\b|\\boneself\\b|\\bshe\\b|\\bshe'd\\b|\\bshe'll\\b|\\bshe's\\b|\\bshes\\b",re.IGNORECASE)

social_re=re.compile("\\baccomplice*\\b|\\bdivorc*\\b|\\bhelping\\b|\\bmotherhood\\b|\\bsororit*\\b|\\bacquainta*\\b|\\bduchess*\\b|\\bhelps\\b|\\bmothering\\b|\\bsoulmate*\\b|\\badmit\\b|\\bdude*\\b|\\bher\\b|\\bmotherl*\\b|\\bspeak\\b|\\badmits\\b|\\bduke*\\b|\\bheroine*\\b|\\bmothers\\b|\\bspeaking\\b|\\badmitted\\b|\\be-mai\\b|\\bhers\\b|\\bmr\\b|\\bspeaks\\b|\\badmitting\\b|\\be-mailed\\b|\\bherself\\b|\\bmrs\\b|\\bspoke*\\b|\\badult\\b|\\be-mailing\\b|\\bhes\\b|\\bms\\b|\\bspous*\\b|\\badults\\b|\\be-mails\\b|\\bhey\\b|\\bmum\\b|\\bsquad*\\b|\\badvice\\b|\\bemai\\b|\\bhi\\b|\\bmum's\\b|\\bstep-child*\\b|\\badvis*\\b|\\bemailed\\b|\\bhim\\b|\\bmummy*\\b|\\bstep-dad*\\b|\\baffair*\\b|\\bemailing\\b|\\bhimself\\b|\\bmums\\b|\\bstep-dau*\\b|\\bally\\b|\\bemails\\b|\\bhipster\\b|\\bname\\b|\\bstep-fath*\\b|\\bamigo*\\b|\\bembarrass*\\b|\\bhis\\b|\\bnames\\b|\\bstep-kid*\\b|\\banonymous*\\b|\\bencourag*\\b|\\bhissel*\\b|\\bnana\\b|\\bstep-moth*\\b|\\banybod*\\b|\\benemie*\\b|\\bhomie\\b|\\bnana's\\b|\\bstep-son*\\b|\\banyone*\\b|\\benemy*\\b|\\bhoney\\b|\\bnanas\\b|\\bstepchild*\\b|\\bapolog*\\b|\\bengag*\\b|\\bhoneymoon\\b|\\bnann*\\b|\\bstepdad*\\b|\\bapproachable\\b|\\beverybod\\b|\\bhostil*\\b|\\bnegotiat*\\b|\\bstepdau*\\b|\\bargu*\\b|\\beveryone\\b|\\bhottie\\b|\\bneighbor*\\b|\\bstepfath*\\b|\\barmies\\b|\\beverything\\b|\\bhousehusband*\\b|\\bneighbour*\\b|\\bstepkid*\\b|\\barmy\\b|\\bex\\b|\\bhousewi*\\b|\\bnephew*\\b|\\bstepmoth*\\b|\\bask\\b|\\bex-bf*\\b|\\bhubby\\b|\\bnewborn*\\b|\\bstepson\\b|\\basked\\b|\\bex-boyfriend\\b|\\bhug\\b|\\bniece*\\b|\\bstories\\b|\\basking\\b|\\bex-gf*\\b|\\bhuman*\\b|\\boffer*\\b|\\bstory\\b|\\basks\\b|\\bex-girlfriend*\\b|\\bhusband*\\b|\\boomf\\b|\\bsugardadd*\\b|\\bassembl*\\b|\\bexbf*\\b|\\bimpersona\\b|\\bour\\b|\\bsugarmam*\\b|\\baunt*\\b|\\bexboy*\\b|\\bimpolite*\\b|\\bours\\b|\\bsugarmom*\\b|\\bawkward\\b|\\bexcus*\\b|\\bimpress*\\b|\\bourselves\\b|\\bsuggest*\\b|\\bawkwardness\\b|\\bexes\\b|\\bin-law*\\b|\\boutsider*\\b|\\bsweetheart*\\b|\\bbabe*\\b|\\bexgf*\\b|\\bindividual*\\b|\\boverhear\\b|\\bsweetie*\\b|\\bbabies\\b|\\bexgirl*\\b|\\binfant\\b|\\bowner*\\b|\\bsympath*\\b|\\bbaby\\b|\\bexhusb*\\b|\\binfant's\\b|\\bpa\\b|\\btalk\\b|\\bbachelor\\b|\\bexplain\\b|\\binfants*\\b|\\bpa's\\b|\\btalkative\\b|\\bbachelor'*\\b|\\bexplained\\b|\\binform\\b|\\bpal\\b|\\btalked\\b|\\bbachelorette\\b|\\bexplaining\\b|\\binformed\\b|\\bpal's\\b|\\btalker*\\b|\\bbachelors\\b|\\bexplains\\b|\\binforming\\b|\\bpals\\b|\\btalking\\b|\\bbae\\b|\\bexpress*\\b|\\binforms\\b|\\bpapa\\b|\\btalks\\b|\\bband\\b|\\bexwife*\\b|\\binlaw*\\b|\\bpapa's\\b|\\bteam*\\b|\\bbands\\b|\\bexwive\\b|\\binquir*\\b|\\bpapas\\b|\\bteas*\\b|\\bbanter*\\b|\\bfacebook\\b|\\binstagram\\b|\\bpappy\\b|\\bteen\\b|\\bbb\\b|\\bfam\\b|\\binsult*\\b|\\bpappy's\\b|\\bteenage*\\b|\\bbby\\b|\\bfamilies\\b|\\binteract*\\b|\\bparent*\\b|\\btelephon*\\b|\\bbcc\\b|\\bfamily\\b|\\binterpersonal\\b|\\bparticipant*\\b|\\btell\\b|\\bbeau\\b|\\bfarewel\\b|\\binterrup*\\b|\\bparticipat*\\b|\\btelling\\b|\\bbeloved\\b|\\bfather*\\b|\\binterview*\\b|\\bpartie*\\b|\\btells\\b|\\bbestfriend*\\b|\\bfb\\b|\\binvolv*\\b|\\bpartner*\\b|\\btexted\\b|\\bbestie\\b|\\bfella\\b|\\bkegger*\\b|\\bparty*\\b|\\btexting\\b|\\bbesties\\b|\\bfellow\\b|\\bkid\\b|\\bpaterna\\b|\\bthee\\b|\\bbf\\b|\\bfellow's\\b|\\bkid'*\\b|\\bpaternity\\b|\\btheir*\\b|\\bbf's\\b|\\bfellows\\b|\\bkidding\\b|\\bpatriarch*\\b|\\bthem\\b|\\bbff*\\b|\\bfellowship*\\b|\\bkids*\\b|\\bpeeps\\b|\\bthemselves\\b|\\bbfs\\b|\\bfemale\\b|\\bkik\\b|\\bpeople*\\b|\\bthey\\b|\\bblam*\\b|\\bfemales\\b|\\bkin\\b|\\bperson\\b|\\bthey'd\\b|\\bboi\\b|\\bfeminine\\b|\\bking\\b|\\bperson's\\b|\\bthey'l\\b|\\bboy\\b|\\bfemininity\\b|\\bking's\\b|\\bpersona\\b|\\bthey're\\b|\\bboy's\\b|\\bfemme*\\b|\\bkingl*\\b|\\bpersons\\b|\\bthey've\\b|\\bboyfriend*\\b|\\bfeud*\\b|\\bkings\\b|\\bpersua*\\b|\\btheyd\\b|\\bboyhood\\b|\\bfiance\\b|\\bknight*\\b|\\bphone*\\b|\\btheyl\\b|\\bboyish\\b|\\bfiance's\\b|\\blad\\b|\\bphoning\\b|\\btheyre\\b|\\bboys\\b|\\bfiancee*\\b|\\bladies\\b|\\bplaymate\\b|\\btheyve\\b|\\bbreakup\\b|\\bfiances\\b|\\blady\\b|\\bpolite\\b|\\bthine\\b|\\bbride*\\b|\\bfight*\\b|\\blady's\\b|\\bpolitely\\b|\\bthou\\b|\\bbro\\b|\\bflatter*\\b|\\blanguage*\\b|\\bpopular\\b|\\bthoust\\b|\\bbro'*\\b|\\bflirt\\b|\\blass\\b|\\bposse\\b|\\bthy\\b|\\bbros\\b|\\bflirtatious\\b|\\blassie\\b|\\bppl*\\b|\\btogether\\b|\\bbrother*\\b|\\bflirted\\b|\\bleader*\\b|\\bprais*\\b|\\btold\\b|\\bbruh\\b|\\bflirting\\b|\\blesbian*\\b|\\bpregnan*\\b|\\btomboy*\\b|\\bbud\\b|\\bflirts\\b|\\blet's\\b|\\bprince\\b|\\btrust\\b|\\bbuddies\\b|\\bflirty\\b|\\blets\\b|\\bprince'*\\b|\\btrusted\\b|\\bbuddy*\\b|\\bfoe*\\b|\\bletter\\b|\\bprinces\\b|\\btrusting\\b|\\bbye\\b|\\bfolks\\b|\\bliar*\\b|\\bprincess*\\b|\\btrusts\\b|\\bcall\\b|\\bfollower*\\b|\\blikeab*\\b|\\bprivate\\b|\\btweet*\\b|\\bcalled\\b|\\bfool\\b|\\blisten\\b|\\bprom\\b|\\btwitter\\b|\\bcaller*\\b|\\bfooled\\b|\\blistened\\b|\\bprovide\\b|\\buncle\\b|\\bcalling\\b|\\bfooling\\b|\\blistener*\\b|\\bprovides\\b|\\buncle's\\b|\\bcalls\\b|\\bfools\\b|\\blistening\\b|\\bproviding\\b|\\buncles\\b|\\bcc\\b|\\bforgave\\b|\\blistens\\b|\\bpublic\\b|\\bur\\b|\\bcced\\b|\\bforgiv*\\b|\\blocals\\b|\\bqueen\\b|\\bus\\b|\\bcelebrat*\\b|\\bformal\\b|\\blove\\b|\\bqueen's\\b|\\bvalentin*\\b|\\bchap\\b|\\bforwarded\\b|\\bloved\\b|\\bqueens\\b|\\bvisit\\b|\\bchat*\\b|\\bfought\\b|\\blover*\\b|\\bquestion\\b|\\bvisited\\b|\\bchick\\b|\\bfrenem*\\b|\\bloves\\b|\\breassur*\\b|\\bvisiting\\b|\\bchick'*\\b|\\bfriend\\b|\\bloving*\\b|\\breceiv*\\b|\\bvisits\\b|\\bchicks\\b|\\bfriendlier\\b|\\bluv\\b|\\brecommend*\\b|\\bwe\\b|\\bchild\\b|\\bfriendliest\\b|\\blying\\b|\\brefus*\\b|\\bwe'd\\b|\\bchild'*\\b|\\bfriendly\\b|\\bma\\b|\\brelate*\\b|\\bwe'll\\b|\\bchildren*\\b|\\bfriends\\b|\\bma'am\\b|\\brelationship*\\b|\\bwe're\\b|\\bchit-chat*\\b|\\bfwb\\b|\\bma's\\b|\\brelatives\\b|\\bwe've\\b|\\bchitchat*\\b|\\bgal\\b|\\bmaam\\b|\\breplie*\\b|\\bwed\\b|\\bchum\\b|\\bgals\\b|\\bmadam\\b|\\breply*\\b|\\bwedding*\\b|\\bchums\\b|\\bgame*\\b|\\bmadame*\\b|\\brequest*\\b|\\bweds\\b|\\bcitizen\\b|\\bgang\\b|\\bmademoiselle\\b|\\brespond*\\b|\\bwelcom*\\b|\\bcitizen'*\\b|\\bgangs\\b|\\bmaid\\b|\\brole*\\b|\\bwench*\\b|\\bcitizens\\b|\\bgather*\\b|\\bmaid's\\b|\\broomate*\\b|\\bweve\\b|\\bclassmate\\b|\\bgave\\b|\\bmaiden\\b|\\broomed\\b|\\bwho\\b|\\bclassmates\\b|\\bgenero*\\b|\\bmaids\\b|\\broomie*\\b|\\bwho'd\\b|\\bclique*\\b|\\bgent\\b|\\bmail\\b|\\brooming\\b|\\bwho'll\\b|\\bco-work*\\b|\\bgentlem*\\b|\\bmailed\\b|\\broommate*\\b|\\bwho's\\b|\\bcolleague*\\b|\\bgentlewom*\\b|\\bmailing\\b|\\brt\\b|\\bwhod\\b|\\bcoma*\\b|\\bgents\\b|\\bmails\\b|\\brumor*\\b|\\bwhoeve\\b|\\bcomment*\\b|\\bgf*\\b|\\bmale\\b|\\brumour*\\b|\\bwholl\\b|\\bcommun*\\b|\\bgirl\\b|\\bmale's\\b|\\bsaid\\b|\\bwhom\\b|\\bcompadre*\\b|\\bgirl's\\b|\\bmales\\b|\\bsay\\b|\\bwhomeve\\b|\\bcompanion*\\b|\\bgirlfriend*\\b|\\bmam\\b|\\bsaying\\b|\\bwhos\\b|\\bcompany\\b|\\bgirlh*\\b|\\bmama\\b|\\bsays\\b|\\bwhose\\b|\\bcompassion*\\b|\\bgirli*\\b|\\bman\\b|\\bschoolboy*\\b|\\bwidow*\\b|\\bcomplain*\\b|\\bgirls*\\b|\\bman's\\b|\\bschoolgirl*\\b|\\bwife*\\b|\\bcompliment*\\b|\\bgirly\\b|\\bmanly\\b|\\bschoolmate\\b|\\bwitch*\\b|\\bcomrad*\\b|\\bgive\\b|\\bmanners\\b|\\bsecret\\b|\\bwive*\\b|\\bconfess*\\b|\\bgiver*\\b|\\bmarriag*\\b|\\bsecretive\\b|\\bwoman\\b|\\bconfidant*\\b|\\bgives\\b|\\bmarrie*\\b|\\bsecretively\\b|\\bwoman's\\b|\\bconfide\\b|\\bgiving\\b|\\bmarry\\b|\\bsecretly\\b|\\bwomanhood\\b|\\bconfided\\b|\\bgoddess*\\b|\\bmasculine\\b|\\bsecrets\\b|\\bwomanly\\b|\\bconfides\\b|\\bgodfather*\\b|\\bmasculinity\\b|\\bself\\b|\\bwomans\\b|\\bconfiding\\b|\\bgodmothe\\b|\\bmate\\b|\\bsend\\b|\\bwomen*\\b|\\bcongregat*\\b|\\bgodparen\\b|\\bmate's\\b|\\bsender\\b|\\by'al\\b|\\bconsult*\\b|\\bgoodbye\\b|\\bmaternal*\\b|\\bsending\\b|\\by'all's\\b|\\bcontact\\b|\\bgossip*\\b|\\bmaternity\\b|\\bsends\\b|\\bya\\b|\\bcontacted\\b|\\bgramp*\\b|\\bmates\\b|\\bsenor\\b|\\bya'll*\\b|\\bcontacts\\b|\\bgrandchil*\\b|\\bmating\\b|\\bsenora\\b|\\byall\\b|\\bcontradic*\\b|\\bgranddad*\\b|\\bmatriarch*\\b|\\bsenorita\\b|\\byalls\\b|\\bconvers*\\b|\\bgranddau*\\b|\\bmeet\\b|\\bsent\\b|\\bye\\b|\\bcounc*\\b|\\bgrandfath*\\b|\\bmeeting*\\b|\\bshare\\b|\\byou\\b|\\bcouns*\\b|\\bgrandkid*\\b|\\bmeets\\b|\\bshared\\b|\\byou'd\\b|\\bcourtship\\b|\\bgrandm*\\b|\\bmember*\\b|\\bshares\\b|\\byou'l\\b|\\bcousin*\\b|\\bgrandpa*\\b|\\bmen\\b|\\bsharing\\b|\\byou're\\b|\\bcowboy*\\b|\\bgrandson*\\b|\\bmen'*\\b|\\bshe\\b|\\byou've\\b|\\bcowgirl*\\b|\\bgranny\\b|\\bmens\\b|\\bshe'd\\b|\\byoud\\b|\\bcowork*\\b|\\bgreet*\\b|\\bmention*\\b|\\bshe'll\\b|\\byoul\\b|\\bcrew\\b|\\bgrl*\\b|\\bmessage\\b|\\bshe's\\b|\\byoungster*\\b|\\bcrowd*\\b|\\bgroom'*\\b|\\bmessaged\\b|\\bshe-*\\b|\\byour\\b|\\bcultur*\\b|\\bgroup*\\b|\\bmessages\\b|\\bshes\\b|\\byoure\\b|\\bcutie*\\b|\\bgrown-up*\\b|\\bmessaging\\b|\\bshy\\b|\\byours\\b|\\bdad\\b|\\bgrownup*\\b|\\bmet\\b|\\bshyly\\b|\\byourself\\b|\\bdad's\\b|\\bgrudg*\\b|\\bmilf*\\b|\\bshyness\\b|\\byourselves\\b|\\bdaddies\\b|\\bguest*\\b|\\bmimi\\b|\\bsibling*\\b|\\byouve\\b|\\bdaddy\\b|\\bgurl*\\b|\\bmimi'*\\b|\\bsidekick*\\b|\\bdaddy's\\b|\\bguy*\\b|\\bmimis\\b|\\bsir\\b|\\bdads\\b|\\bhandshake\\b|\\bmissus\\b|\\bsis\\b|\\bdame*\\b|\\bhangout*\\b|\\bmister\\b|\\bsister*\\b|\\bdamsel*\\b|\\bhe\\b|\\bmistres*\\b|\\bsms\\b|\\bdance\\b|\\bhe'd\\b|\\bmock\\b|\\bsmsed\\b|\\bdanced\\b|\\bhe'll\\b|\\bmocked\\b|\\bsnapchat*\\b|\\bdances\\b|\\bhe's\\b|\\bmocking\\b|\\bsnob*\\b|\\bdancing\\b|\\bhe-*\\b|\\bmocks\\b|\\bsociability\\b|\\bdarlin*\\b|\\bhear\\b|\\bmom\\b|\\bsociable\\b|\\bdate\\b|\\bheard\\b|\\bmom's\\b|\\bsocial\\b|\\bdating\\b|\\bhearing\\b|\\bmomma*\\b|\\bsocially\\b|\\bdaughter*\\b|\\bhears\\b|\\bmommy*\\b|\\bsociet*\\b|\\bdawg*\\b|\\bhello*\\b|\\bmoms\\b|\\bsomebod*\\b|\\bdear\\b|\\bhelp\\b|\\bmonsieur\\b|\\bsomeone*\\b|\\bdebate\\b|\\bhelper*\\b|\\bmooch*\\b|\\bson\\b|\\bdilf*\\b|\\bhelpful\\b|\\bmother\\b|\\bson's\\b|\\bdisclo*\\b|\\bhelpfully\\b|\\bmother's\\b|\\bson-in-law*\\b|\\bdiscuss*\\b|\\bhelpfulness\\b|\\bmothered\\b|\\bsons\\b",re.IGNORECASE)
swear_re=re.compile("\\baf\\b|\\barse\\b|\\barsehole*\\b|\\barses\\b|\\basf\\b|\\bass\\b|\\basses\\b|\\basshole*\\b|\\basswipe\\b|\\bbadass*\\b|\\bbamf\\b|\\bbastard*\\b|\\bbiatch*\\b|\\bbiotch*\\b|\\bbitch*\\b|\\bbloody\\b|\\bbollock*\\b|\\bboob*\\b|\\bbs\\b|\\bbullshit\\b|\\bbumfuck\\b|\\bbutt\\b|\\bbuttfuck*\\b|\\bbutts\\b|\\bcock\\b|\\bcocks*\\b|\\bcrap\\b|\\bcrappy\\b|\\bcunt*\\b|\\bdammit\\b|\\bdamn*\\b|\\bdang\\b|\\bdarn\\b|\\bdick\\b|\\bdickhead*\\b|\\bdickhole*\\b|\\bdickish*\\b|\\bdicks\\b|\\bdickwad\\b|\\bdilf*\\b|\\bdipshit*\\b|\\bdoofus\\b|\\bdork*\\b|\\bdouche*\\b|\\bdtf\\b|\\bdufus\\b|\\bdumb\\b|\\bdumbass*\\b|\\bdumber\\b|\\bdumbest\\b|\\bdumbfuck*\\b|\\bdummy\\b|\\beffin\\b|\\beffin'\\b|\\beffing\\b|\\bfag\\b|\\bfaggot*\\b|\\bfaggy\\b|\\bfatties\\b|\\bfml\\b|\\bfreak*\\b|\\bfriggin\\b|\\bfriggin'\\b|\\bfrigging\\b|\\bfu\\b|\\bfuck\\b|\\bfuckboy*\\b|\\bfucked*\\b|\\bfucker*\\b|\\bfuckface*\\b|\\bfuckh*\\b|\\bfuckin*\\b|\\bfucks\\b|\\bfucktard\\b|\\bfucktwat*\\b|\\bfuckwad*\\b|\\bgeek*\\b|\\bgoddam*\\b|\\bhalf-ass*\\b|\\bhalfass*\\b|\\bheck\\b|\\bhell\\b|\\bhella\\b|\\bhoe\\b|\\bhoebag\\b|\\bhoes\\b|\\bhomo\\b|\\bhomos\\b|\\bhorseshit*\\b|\\bidgaf\\b|\\bidiot*\\b|\\bignoramus\\b|\\bjackass\\b|\\bjeez\\b|\\blmao*\\b|\\blmfao*\\b|\\bmf\\b|\\bmf'*\\b|\\bmfs\\b|\\bmilf*\\b|\\bmofo*\\b|\\bmoron*\\b|\\bmotherfucke*\\b|\\bmotherfuckin*\\b|\\bnigga*\\b|\\bnigger*\\b|\\bomfg\\b|\\bpiss*\\b|\\bprick*\\b|\\bpussies\\b|\\bpussy*\\b|\\bretard*\\b|\\bscrew*\\b|\\bshit*\\b|\\bskank*\\b|\\bslut*\\b|\\bsonofa*\\b|\\bstfu\\b|\\bsuck\\b|\\bsucked\\b|\\bsucks\\b|\\btit\\b|\\btits\\b|\\btitties\\b|\\btitty\\b|\\btwat*\\b|\\bwank*\\b|\\bwhore*\\b|\\bwtf\\b|\\bwuss\\b|\\bwussy\\b",re.IGNORECASE)
negate_re=re.compile("\\bain't\\b|\\baint\\b|\\baren't\\b|\\barent\\b|\\bcan't\\b|\\bcannot\\b|\\bcant\\b|\\bcouldn't\\b|\\bcouldnt\\b|\\bdidn't\\b|\\bdidnt\\b|\\bdoesn't\\b|\\bdoesnt\\b|\\bdon't\\b|\\bdont\\b|\\bhadn't\\b|\\bhadnt\\b|\\bhasn't\\b|\\bhasnt\\b|\\bhaven'\\b|\\bhaven\\b|\\bidk\\b|\\bisn't\\b|\\bisnt\\b|\\bmust'nt\\b|\\bmustn't\\b|\\bmustnt\\b|\\bnah*\\b|\\bneed'nt\\b|\\bneedn't\\b|\\bneednt\\b|\\bnegat*\\b|\\bneither\\b|\\bnever\\b|\\bno\\b|\\bnobod*\\b|\\bnoes\\b|\\bnone\\b|\\bnope\\b|\\bnor\\b|\\bnot\\b|\\bnothing\\b|\\bnowhere\\b|\\bnp\\b|\\bought'nt\\b|\\boughtn't\\b|\\boughtnt\\b|\\bshan't\\b|\\bshant\\b|\\bshould'nt\\b|\\bshouldn't\\b|\\bshouldnt\\b|\\buh-uh\\b|\\bwasn't\\b|\\bwasnt\\b|\\bweren't\\b|\\bwerent\\b|\\bwithout\\b|\\bwon't\\b|\\bwont\\b|\\bwouldn't\\b|\\bwouldnt\\b",re.IGNORECASE)
differ_re=re.compile("\\bactually\\b|\\badjust*\\b|\\bagainst\\b|\\bain't\\b|\\baint\\b|\\balternativ\\b|\\balthough\\b|\\bapart\\b|\\baren't\\b|\\barent\\b|\\bbut\\b|\\bcan't\\b|\\bcannot\\b|\\bcant\\b|\\bdespite\\b|\\bdidn't\\b|\\bdidnt\\b|\\bdiffer\\b|\\bdiffered\\b|\\bdifference*\\b|\\bdifferent\\b|\\bdifferentia\\b|\\bdifferentiat*\\b|\\bdifferently\\b|\\bdiffering\\b|\\bdiffers\\b|\\bdissimil*\\b|\\bdistinct*\\b|\\bdistinguish*\\b|\\beither\\b|\\belse\\b|\\bexcept\\b|\\bexception\\b|\\bexceptions\\b|\\bexclude\\b|\\bexcluded\\b|\\bexcludes\\b|\\bexcluding\\b|\\bexclusion*\\b|\\bexclusively\\b|\\bhasn't\\b|\\bhasnt\\b|\\bhaven'\\b|\\bhaven\\b|\\bhoweve\\b|\\bif\\b|\\binequal*\\b|\\binstead\\b|\\bisn't\\b|\\bisnt\\b|\\bjus\\b|\\bkinds\\b|\\bneither\\b|\\bnevertheless\\b|\\bnor\\b|\\bnot\\b|\\bnotwithstanding\\b|\\bopposite*\\b|\\bor\\b|\\bother\\b|\\bothers\\b|\\botherwise\\b|\\brather\\b|\\breally\\b|\\brespective\\b|\\bseparat*\\b|\\bsplit*\\b|\\bthan\\b|\\bthough\\b|\\bunless\\b|\\bunlike\\b|\\bversion\\b|\\bversus\\b|\\bvs\\b|\\bwasn't\\b|\\bwasnt\\b|\\bweren't\\b|\\bwerent\\b|\\bwhereas\\b|\\bwhether\\b|\\bwithout\\b",re.IGNORECASE)

article_re=re.compile("\\ba\\b|\\ban\\b|\\bthe\\b",re.IGNORECASE)
prep_re=re.compile("\\babout\\b|\\babove\\b|\\babt\\b|\\bacross\\b|\\bafter\\b|\\bagainst\\b|\\bahead\\b|\\balong\\b|\\bamid\\b|\\bamidst\\b|\\bamong*\\b|\\baround\\b|\\bas\\b|\\bat\\b|\\batop\\b|\\baway\\b|\\bbefore\\b|\\bbehind\\b|\\bbelow\\b|\\bbeneath\\b|\\bbeside\\b|\\bbesides\\b|\\bbetween\\b|\\bbeyond\\b|\\bby\\b|\\bdespite\\b|\\bdown\\b|\\bduring\\b|\\bexcept\\b|\\bexcluding\\b|\\bfor\\b|\\bfrom\\b|\\bhereafter\\b|\\bin\\b|\\bincluding\\b|\\binside\\b|\\binsides\\b|\\binto\\b|\\blike\\b|\\bminus\\b|\\bnear\\b|\\bof\\b|\\boff\\b|\\bon\\b|\\bonto\\b|\\bout\\b|\\boutside\\b|\\bover\\b|\\bplus\\b|\\bregarding\\b|\\brespecting\\b|\\bsans\\b|\\bsince\\b|\\bthan\\b|\\bthrough*\\b|\\bthru\\b|\\btil\\b|\\btill\\b|\\bto\\b|\\btoward*\\b|\\bunder\\b|\\bunderneath\\b|\\bunless\\b|\\bunlike\\b|\\buntil\\b|\\bunto\\b|\\bup\\b|\\bupon\\b|\\bversus\\b|\\bvia\\b|\\bvs\\b|\\bwith\\b|\\bwithin\\b|\\bwithout\\b",re.IGNORECASE)
pronoun_re=re.compile("\\banother\\b|\\banybod*\\b|\\banymore\\b|\\banyone*\\b|\\banything\\b|\\bdeez\\b|\\beverybod\\b|\\beveryda\\b|\\beveryone\\b|\\beverything\\b|\\bhe\\b|\\bhe'd\\b|\\bhe's\\b|\\bher\\b|\\bhers\\b|\\bherself\\b|\\bhes\\b|\\bhim\\b|\\bhimself\\b|\\bhis\\b|\\bhissel*\\b|\\bi\\b|\\bi'd\\b|\\bi'd've\\b|\\bi'll\\b|\\bi'm\\b|\\bi've\\b|\\bid\\b|\\bidc\\b|\\bidgaf\\b|\\bidk\\b|\\bidontknow\\b|\\bidve\\b|\\bikr\\b|\\bily*\\b|\\bim\\b|\\bima\\b|\\bimean\\b|\\bimma\\b|\\bit\\b|\\bit'd\\b|\\bit'll\\b|\\bit's\\b|\\bitd\\b|\\bitll\\b|\\bits\\b|\\bitself\\b|\\bive\\b|\\blet's\\b|\\blets\\b|\\bme\\b|\\bmethinks\\b|\\bmine\\b|\\bmy\\b|\\bmyself\\b|\\bnobod*\\b|\\boneself\\b|\\bother\\b|\\bothers\\b|\\bour\\b|\\bours\\b|\\bourselves\\b|\\bshe\\b|\\bshe'd\\b|\\bshe'll\\b|\\bshe's\\b|\\bshes\\b|\\bsomebod*\\b|\\bsomeone*\\b|\\bsomething*\\b|\\bsomewhere\\b|\\bstuff\\b|\\bthat\\b|\\bthat'd\\b|\\bthat'll\\b|\\bthat's\\b|\\bthatd\\b|\\bthatll\\b|\\bthats\\b|\\bthee\\b|\\btheir*\\b|\\bthem\\b|\\bthemself\\b|\\bthemselves\\b|\\bthese\\b|\\bthey\\b|\\bthey'd\\b|\\bthey'l\\b|\\bthey've\\b|\\btheyd\\b|\\btheyl\\b|\\btheyve\\b|\\bthine\\b|\\bthing*\\b|\\bthis\\b|\\bthose\\b|\\bthou\\b|\\bthoust\\b|\\bthy\\b|\\bthyself\\b|\\bu\\b|\\bur\\b|\\bus\\b|\\bwe\\b|\\bwe'd\\b|\\bwe'll\\b|\\bwe're\\b|\\bwe've\\b|\\bweve\\b|\\bwhat\\b|\\bwhat'd\\b|\\bwhat'll\\b|\\bwhat's\\b|\\bwhatd\\b|\\bwhateve\\b|\\bwhatll\\b|\\bwhats\\b|\\bwhich\\b|\\bwhicheve\\b|\\bwho\\b|\\bwho'd\\b|\\bwho'll\\b|\\bwho's\\b|\\bwhod\\b|\\bwhoeve\\b|\\bwholl\\b|\\bwhom\\b|\\bwhomeve\\b|\\bwhos\\b|\\bwhose\\b|\\bwhoseve\\b|\\bwhoso*\\b|\\by'al\\b|\\by'all's\\b|\\bya\\b|\\bya'll*\\b|\\byall\\b|\\byalls\\b|\\bye\\b|\\byinz*\\b|\\byou\\b|\\byou'd\\b|\\byou'l\\b|\\byou're\\b|\\byou've\\b|\\byoud\\b|\\byoul\\b|\\byour\\b|\\byoure\\b|\\byours\\b|\\byourself\\b|\\byourselves\\b|\\byouve\\b",re.IGNORECASE)
auxverb_re=re.compile("\\bain't\\b|\\baint\\b|\\bam\\b|\\bare\\b|\\baren't\\b|\\barent\\b|\\bbe\\b|\\bbecome\\b|\\bbecomes\\b|\\bbecoming\\b|\\bbeen\\b|\\bbeing\\b|\\bcan\\b|\\bcannot\\b|\\bcould\\b|\\bcould've\\b|\\bcouldn't\\b|\\bcouldnt\\b|\\bcouldve\\b|\\bdid\\b|\\bdidn't\\b|\\bdidnt\\b|\\bdo\\b|\\bdoes\\b|\\bdoesn't\\b|\\bdoesnt\\b|\\bdoing\\b|\\bdon't\\b|\\bdone\\b|\\bdont\\b|\\bgunna\\b|\\bhad\\b|\\bhadn't\\b|\\bhadnt\\b|\\bhas\\b|\\bhasn't\\b|\\bhasnt\\b|\\bhave\\b|\\bhaven'\\b|\\bhaven\\b|\\bhaving\\b|\\bhe'd\\b|\\bhe's\\b|\\bhes\\b|\\bi'd\\b|\\bi'll\\b|\\bi'm\\b|\\bi've\\b|\\bid\\b|\\bim\\b|\\bis\\b|\\bisn't\\b|\\bisnt\\b|\\bit'd\\b|\\bit'll\\b|\\bit's\\b|\\bitd\\b|\\bitll\\b|\\bive\\b|\\blet\\b|\\bmay\\b|\\bmight\\b|\\bmight've\\b|\\bmightve\\b|\\bmust\\b|\\bmust'nt\\b|\\bmust've\\b|\\bmustn't\\b|\\bmustnt\\b|\\bmustve\\b|\\bought\\b|\\bought'nt\\b|\\bought've\\b|\\boughta\\b|\\boughtn't\\b|\\boughtnt\\b|\\boughtve\\b|\\bshall\\b|\\bshan't\\b|\\bshant\\b|\\bshe'd\\b|\\bshe'll\\b|\\bshe's\\b|\\bshes\\b|\\bshould\\b|\\bshould'nt\\b|\\bshould've\\b|\\bshouldn't\\b|\\bshouldnt\\b|\\bshouldve\\b|\\bthat'd\\b|\\bthat'll\\b|\\bthat's\\b|\\bthatd\\b|\\bthatll\\b|\\bthats\\b|\\bthere's\\b|\\btheres\\b|\\bthey'd\\b|\\bthey'l\\b|\\bthey're\\b|\\bthey've\\b|\\btheyd\\b|\\btheyl\\b|\\btheyre\\b|\\btheyve\\b|\\btryna\\b|\\bunable\\b|\\bwanna\\b|\\bwas\\b|\\bwasn't\\b|\\bwasnt\\b|\\bwe'd\\b|\\bwe'll\\b|\\bwe've\\b|\\bwere\\b|\\bweren't\\b|\\bwerent\\b|\\bweve\\b|\\bwhat's\\b|\\bwhats\\b|\\bwho'd\\b|\\bwho'll\\b|\\bwhod\\b|\\bwholl\\b|\\bwill\\b|\\bwon't\\b|\\bwont\\b|\\bwould\\b|\\bwould've\\b|\\bwouldn't\\b|\\bwouldnt\\b|\\bwouldve\\b|\\byou'd\\b|\\byou'l\\b|\\byou're\\b|\\byou've\\b|\\byoud\\b|\\byoul\\b|\\byoure\\b|\\byouve\\b",re.IGNORECASE)
conj_re=re.compile("\\balso\\b|\\baltho\\b|\\balthough\\b|\\band\\b|\\bas\\b|\\bbc\\b|\\bbecause\\b|\\bbut\\b|\\bcos\\b|\\bcoz\\b|\\bcuz\\b|\\bhow\\b|\\bhow'd\\b|\\bhow're\\b|\\bhow's\\b|\\bhowd\\b|\\bhoweve\\b|\\bhowre\\b|\\bhows\\b|\\bif\\b|\\bnevertheless\\b|\\bnor\\b|\\bor\\b|\\botherwise\\b|\\bplus\\b|\\bso\\b|\\bthen\\b|\\btho\\b|\\btho'\\b|\\bthough\\b|\\btil\\b|\\btill\\b|\\bunless\\b|\\buntil\\b|\\bwhen\\b|\\bwhen'*\\b|\\bwheneve\\b|\\bwhereas\\b|\\bwherefore\\b|\\bwhereve\\b|\\bwhether\\b|\\bwhile\\b|\\bwhilst\\b",re.IGNORECASE)
adverb_re=re.compile("\\babout\\b|\\babsolutely\\b|\\bactually\\b|\\bagain\\b|\\balmost\\b|\\balready\\b|\\balso\\b|\\banyway\\b|\\banywhere\\b|\\bapparently\\b|\\baround\\b|\\bawhile\\b|\\bback\\b|\\bbarely\\b|\\bbasically\\b|\\bbeyond\\b|\\bbriefly\\b|\\bclearly\\b|\\bcommonly\\b|\\bcompletely\\b|\\bconstantly\\b|\\bcontinually\\b|\\bdefinitely\\b|\\bespecially\\b|\\bessentially\\b|\\beven\\b|\\beventuall\\b|\\bever\\b|\\beverywhere\\b|\\bexclusively\\b|\\bextremely\\b|\\bfinally\\b|\\bfortunately\\b|\\bfrequently\\b|\\bfully\\b|\\bgenerally\\b|\\bhardly\\b|\\bhence\\b|\\bhenceforth\\b|\\bhere\\b|\\bhere's\\b|\\bherein\\b|\\bheres\\b|\\bhereto*\\b|\\bhopefully\\b|\\bhow\\b|\\bhow'd\\b|\\bhow're\\b|\\bhow's\\b|\\bhowd\\b|\\bhoweve\\b|\\bhowre\\b|\\bhows\\b|\\bimmediately\\b|\\bindeed\\b|\\binstead\\b|\\bjus\\b|\\bjust\\b|\\bjuz\\b|\\blately\\b|\\bmaybe\\b|\\bmeanwhile\\b|\\bmostly\\b|\\bnamely\\b|\\bnearly\\b|\\bnever\\b|\\bnevertheless\\b|\\bnonetheless\\b|\\bnotwithstanding\\b|\\bnow\\b|\\boften\\b|\\bonly\\b|\\boriginally\\b|\\bparticularly\\b|\\bperhaps\\b|\\bpractically\\b|\\bpresently\\b|\\bprimarily\\b|\\bprincipally\\b|\\bprobab*\\b|\\bprolly\\b|\\brarely\\b|\\brather\\b|\\breally\\b|\\bregularly\\b|\\brelatively\\b|\\brespectively\\b|\\bseldomly\\b|\\bseriously\\b|\\bshortly\\b|\\bsimply\\b|\\bso\\b|\\bsomehow\\b|\\bsomewha\\b|\\bsomewhere\\b|\\bsoon\\b|\\bsooo*\\b|\\bspecifically\\b|\\bstill\\b|\\bsubsequently\\b|\\bsuch\\b|\\bsuddenly\\b|\\bsupposedly\\b|\\bthere\\b|\\bthere's\\b|\\bthereafter\\b|\\btherefor*\\b|\\btheres\\b|\\btho\\b|\\btho'\\b|\\bthough\\b|\\bthus*\\b|\\btoo\\b|\\btotally\\b|\\btruly\\b|\\btypically\\b|\\bultimately\\b|\\buncommonly\\b|\\busually\\b|\\bvastly\\b|\\bvery\\b|\\bvirtually\\b|\\bwell\\b|\\bwhen\\b|\\bwhen'*\\b|\\bwhence\\b|\\bwheneve\\b|\\bwhere\\b|\\bwhere'd\\b|\\bwhereby\\b|\\bwherefore\\b|\\bwherein\\b|\\bwhereof\\b|\\bwhereve\\b|\\bwhither\\b|\\bwholly\\b|\\bwhy\\b|\\bwhy'*\\b|\\bwhyeve\\b|\\byet\\b",re.IGNORECASE)

insight_re=re.compile("\\baccept\\b|\\bmotiv*\\b|\\baccepta*\\b|\\bnotice\\b|\\baccepted\\b|\\bnoticed\\b|\\baccepting\\b|\\bnotices\\b|\\baccepts\\b|\\bnoticing\\b|\\backnowledg*\\b|\\bperceiv*\\b|\\badmit\\b|\\bpercept*\\b|\\badmits\\b|\\bperspective\\b|\\badmitted\\b|\\bpersua*\\b|\\badmitting\\b|\\bponder*\\b|\\bafterthought*\\b|\\bprefer*\\b|\\banaly*\\b|\\bpresum*\\b|\\banswer*\\b|\\bpretend*\\b|\\bappreciat*\\b|\\bprove*\\b|\\bassum*\\b|\\bproving\\b|\\battent*\\b|\\bquer*\\b|\\baware*\\b|\\bquestion\\b|\\bbecame\\b|\\bquestioned\\b|\\bbecome\\b|\\bquestioning\\b|\\bbecomes\\b|\\bquestions\\b|\\bbecoming\\b|\\brational*\\b|\\bbelief*\\b|\\brealization\\b|\\bbelieve\\b|\\brealize\\b|\\bbelieved\\b|\\brealized\\b|\\bbelieves\\b|\\brealizes\\b|\\bbelieving\\b|\\brealizing\\b|\\bcategor*\\b|\\brearrang*\\b|\\bchoice*\\b|\\breason*\\b|\\bchoos*\\b|\\brebel*\\b|\\bclarif*\\b|\\brecall*\\b|\\bclosure\\b|\\brecogni*\\b|\\bclue\\b|\\brecollect*\\b|\\bcohere*\\b|\\breconcil*\\b|\\bcomplex\\b|\\breconsider*\\b|\\bcomplexity\\b|\\breconstruct*\\b|\\bcomplicate\\b|\\breevaluat\\b|\\bcomplicated\\b|\\brefer*\\b|\\bcomplicates\\b|\\breflect*\\b|\\bcomplicating\\b|\\brelate*\\b|\\bcomplication*\\b|\\brelating\\b|\\bcompreh*\\b|\\brelation\\b|\\bconcentrat*\\b|\\brelations\\b|\\bconclud*\\b|\\bremember\\b|\\bconclus*\\b|\\bremembered\\b|\\bconfess*\\b|\\bremembering\\b|\\bconscious*\\b|\\bremembers\\b|\\bconsider\\b|\\breorgani*\\b|\\bconsideration\\b|\\bresolu*\\b|\\bconsidered\\b|\\bresolv*\\b|\\bconsidering\\b|\\brestructur*\\b|\\bconsiders\\b|\\brethink*\\b|\\bcontemplat*\\b|\\breveal*\\b|\\bconvinc*\\b|\\brevelat*\\b|\\bcorrelat*\\b|\\bsecret\\b|\\bcurio*\\b|\\bsecretive\\b|\\bdecide\\b|\\bsecretively\\b|\\bdecided\\b|\\bsecrets\\b|\\bdecides\\b|\\bseem\\b|\\bdeciding\\b|\\bseemed\\b|\\bdecis*\\b|\\bseeming*\\b|\\bdeduc*\\b|\\bseems\\b|\\bdefine\\b|\\bsense\\b|\\bdefines\\b|\\bsensed\\b|\\bdefining\\b|\\bsenses\\b|\\bdefinition\\b|\\bsensing\\b|\\bdetermina*\\b|\\bskeptic*\\b|\\bdetermine\\b|\\bsolution*\\b|\\bdetermined\\b|\\bsolve\\b|\\bdetermines\\b|\\bsolved\\b|\\bdetermining\\b|\\bsolves\\b|\\bdiagnos*\\b|\\bsolving\\b|\\bdiscern*\\b|\\bsought\\b|\\bdisclo*\\b|\\bstatement*\\b|\\bdiscover*\\b|\\bsuspect*\\b|\\bdisillusion*\\b|\\bsuspicio*\\b|\\bdistract*\\b|\\bthink\\b|\\beffect*\\b|\\bthinker*\\b|\\benlighten*\\b|\\bthinking\\b|\\bevaluat*\\b|\\bthinks\\b|\\bevidence\\b|\\bthought\\b|\\bexamin*\\b|\\bthoughts\\b|\\bexplain\\b|\\btrick\\b|\\bexplained\\b|\\btricked\\b|\\bexplaining\\b|\\btrickier\\b|\\bexplains\\b|\\btrickiest\\b|\\bexplanat\\b|\\btricks\\b|\\bexplor*\\b|\\btricky\\b|\\bfeel\\b|\\bunaccept*\\b|\\bfeeling\\b|\\bunaware*\\b|\\bfeelings\\b|\\bunderstand\\b|\\bfeels\\b|\\bunderstandab*\\b|\\bfelt\\b|\\bunderstanding*\\b|\\bfigur*\\b|\\bunderstands\\b|\\bfind\\b|\\bunderstood\\b|\\bfinding\\b|\\bunrelat*\\b|\\bfindings\\b|\\bwisdom\\b|\\bfinds\\b|\\bwise\\b|\\bforgave\\b|\\bwisely\\b|\\bforgiv*\\b|\\bwiser\\b|\\bfound\\b|\\bwisest\\b|\\bgenuine\\b|\\bwonder\\b|\\bgenuinely\\b|\\bwondered\\b|\\bgrasp*\\b|\\bwondering\\b|\\bheed\\b|\\bwonders\\b|\\bheeded\\b|\\bidea\\b|\\bideas\\b|\\bidentif*\\b|\\bimagin*\\b|\\binduc*\\b|\\binfer\\b|\\binferen*\\b|\\binferr*\\b|\\binfers\\b|\\binfo\\b|\\binform\\b|\\binformation\\b|\\binformative*\\b|\\binformed\\b|\\binforming\\b|\\binforms\\b|\\binquir*\\b|\\binsight*\\b|\\binspir*\\b|\\binterpret*\\b|\\bjustif*\\b|\\bknew\\b|\\bknow\\b|\\bknowab*\\b|\\bknowing\\b|\\bknowledg*\\b|\\bknown\\b|\\bknows\\b|\\blearn\\b|\\blearned\\b|\\blearner\\b|\\blearners\\b|\\blearning\\b|\\blearns\\b|\\blearnt\\b|\\blesson*\\b|\\blink*\\b|\\blogic*\\b|\\bmean\\b|\\bmeaning*\\b|\\bmeans\\b|\\bmeant\\b|\\bmemorabl*\\b|\\bmemories\\b|\\bmemoris*\\b|\\bmemoriz*\\b|\\bmemory\\b|\\bmethinks\\b|\\bmindful*\\b|\\bmisunder*\\b",re.IGNORECASE)
relativ_re=re.compile("\\babove\\b|\\bcounties\\b|\\bformer\\b|\\blowering\\b|\\breceiv*\\b|\\bstopped\\b|\\bwed\\b|\\babrupt*\\b|\\bcountr*\\b|\\bformerly\\b|\\blowers\\b|\\brecency\\b|\\bstopping\\b|\\bwednesday\\b|\\bacross\\b|\\bcounty\\b|\\bforward\\b|\\blowest\\b|\\brecent*\\b|\\bstops\\b|\\bweek\\b|\\baction*\\b|\\bcoverage\\b|\\bforwarded\\b|\\blowli*\\b|\\brecur*\\b|\\bstraight\\b|\\bweek'*\\b|\\badvanc*\\b|\\bcrawl*\\b|\\bforwarding\\b|\\blowly\\b|\\bregion*\\b|\\bstraighter\\b|\\bweekend*\\b|\\bafter\\b|\\bcruis*\\b|\\bforwards\\b|\\blunge*\\b|\\bregularly\\b|\\bstraightest\\b|\\bweekl*\\b|\\baftermath*\\b|\\bcurrent*\\b|\\bfoundation*\\b|\\blunging\\b|\\brelative\\b|\\bstreet*\\b|\\bweeks\\b|\\bafternoon*\\b|\\bcycle*\\b|\\bfrequent\\b|\\bmap\\b|\\bremote*\\b|\\bstretch*\\b|\\bwent\\b|\\bafterthought*\\b|\\bdaily\\b|\\bfrequented\\b|\\bmapped\\b|\\bremov*\\b|\\bstuck\\b|\\bwest*\\b|\\bafterward*\\b|\\bdance\\b|\\bfrequenting\\b|\\bmapping\\b|\\brepeat*\\b|\\bstumble\\b|\\bwhen\\b|\\bagain\\b|\\bdanced\\b|\\bfrequently\\b|\\bmaps\\b|\\brepetit*\\b|\\bstumbled\\b|\\bwhen'*\\b|\\bage\\b|\\bdances\\b|\\bfrequents\\b|\\bmarch*\\b|\\breplace*\\b|\\bstumbles\\b|\\bwhence\\b|\\baged\\b|\\bdancing\\b|\\bfri\\b|\\bmass\\b|\\breplacing\\b|\\bstumbling\\b|\\bwheneve\\b|\\bages\\b|\\bdate\\b|\\bfriday*\\b|\\bmassive\\b|\\brespectively\\b|\\bsubsequent\\b|\\bwhere\\b|\\baging\\b|\\bdated\\b|\\bfront\\b|\\bmeantime\\b|\\breturn*\\b|\\bsubsequently\\b|\\bwhere'd\\b|\\bago\\b|\\bdates\\b|\\bfull\\b|\\bmeanwhile\\b|\\brevolve\\b|\\bsuccessive\\b|\\bwhere's\\b|\\bahead\\b|\\bdating\\b|\\bfuller\\b|\\bmedial*\\b|\\brevolved\\b|\\bsudden\\b|\\bwheres\\b|\\bair\\b|\\bday*\\b|\\bfullest\\b|\\bmeter*\\b|\\brevolves\\b|\\bsuddenly\\b|\\bwhereve\\b|\\balready\\b|\\bdecade*\\b|\\bfullness\\b|\\bmetre*\\b|\\brevolving\\b|\\bsummer*\\b|\\bwhile\\b|\\balways\\b|\\bdecay*\\b|\\bfully\\b|\\bmid\\b|\\brhythm*\\b|\\bsun\\b|\\bwhilst\\b|\\bamong*\\b|\\bdecember\\b|\\bfurther\\b|\\bmiddle\\b|\\bridden\\b|\\bsunday*\\b|\\bwide\\b|\\bancient\\b|\\bdeep\\b|\\bfurthering\\b|\\bmile*\\b|\\bride\\b|\\bsunk\\b|\\bwidely\\b|\\banciently\\b|\\bdeeper\\b|\\bfutur*\\b|\\bmin\\b|\\brides\\b|\\bsunrise*\\b|\\bwider\\b|\\banniversar*\\b|\\bdeepest\\b|\\bgallop\\b|\\bminute*\\b|\\briding\\b|\\bsunset*\\b|\\bwidest\\b|\\bannual*\\b|\\bdeeply\\b|\\bgap\\b|\\bmixed\\b|\\bright\\b|\\bsuperior\\b|\\bwidth*\\b|\\banterior\\b|\\bdelay*\\b|\\bgate*\\b|\\bmobility\\b|\\brise*\\b|\\bsurf\\b|\\bwinter*\\b|\\banymore\\b|\\bdeliver*\\b|\\bgeneration\\b|\\bmodern\\b|\\brising\\b|\\bsurfac*\\b|\\bwithin\\b|\\banytime\\b|\\bdense\\b|\\bgesture*\\b|\\bmodernity\\b|\\broad*\\b|\\bsurfed\\b|\\bwobble\\b|\\banywhere\\b|\\bdensit*\\b|\\bgiant\\b|\\bmodernly\\b|\\brode\\b|\\bsurfing\\b|\\bwobbled\\b|\\bapart\\b|\\bdepart\\b|\\bgigantic\\b|\\bmoment*\\b|\\broll\\b|\\bsurfs\\b|\\bwobbles\\b|\\bapproach\\b|\\bdeparted\\b|\\bginormous\\b|\\bmon\\b|\\brolling\\b|\\bsurround*\\b|\\bwobbling\\b|\\bapproached\\b|\\bdeparting\\b|\\bglide\\b|\\bmonday*\\b|\\broom\\b|\\bswam\\b|\\bwobbly\\b|\\bapproaches\\b|\\bdeparts\\b|\\bgliding\\b|\\bmonth*\\b|\\broomate*\\b|\\bsway\\b|\\bworld\\b|\\bapproaching\\b|\\bdeparture*\\b|\\bglobal*\\b|\\bmorning*\\b|\\broomed\\b|\\bswerve\\b|\\byear\\b|\\bapril\\b|\\bdepth*\\b|\\bgo\\b|\\bmotion*\\b|\\broomie*\\b|\\bswerved\\b|\\byearly\\b|\\barea*\\b|\\bdescend\\b|\\bgoes\\b|\\bmove\\b|\\brooming\\b|\\bswerves\\b|\\byears\\b|\\baround\\b|\\bdescended\\b|\\bgoing\\b|\\bmoved\\b|\\broommate*\\b|\\bswerving\\b|\\byester*\\b|\\barrival*\\b|\\bdescending\\b|\\bgon\\b|\\bmovement\\b|\\brooms\\b|\\bswim*\\b|\\byet\\b|\\barrive\\b|\\bdescends\\b|\\bgone\\b|\\bmover*\\b|\\brotate\\b|\\bswing\\b|\\byoung\\b|\\barrived\\b|\\bdiagonal*\\b|\\bgonna\\b|\\bmoves\\b|\\brotated\\b|\\bswinging\\b|\\byounger\\b|\\barrives\\b|\\bdimension*\\b|\\bgravitate*\\b|\\bmoving\\b|\\brotates\\b|\\bswings\\b|\\byounges\\b|\\barriving\\b|\\bdirect\\b|\\bgrew\\b|\\bnarrow\\b|\\brotating\\b|\\bswivel*\\b|\\byoungster*\\b|\\bat\\b|\\bdirection*\\b|\\bground*\\b|\\bnarrowed\\b|\\brotation*\\b|\\bswung\\b|\\byouth*\\b|\\batop\\b|\\bdirectly\\b|\\bgrow\\b|\\bnarrower\\b|\\broute*\\b|\\bsynch*\\b|\\bzoom\\b|\\battend\\b|\\bdistal\\b|\\bgrowing\\b|\\bnarrowes\\b|\\brun\\b|\\btall\\b|\\battended\\b|\\bdistan*\\b|\\bgrown\\b|\\bnarrowing\\b|\\brunner*\\b|\\btaller\\b|\\battending\\b|\\bdistrict\\b|\\bgrowth\\b|\\bnarrowly\\b|\\brunning\\b|\\btallest\\b|\\battends\\b|\\bdoor*\\b|\\bhall\\b|\\bnarrowness\\b|\\bruns\\b|\\btempora*\\b|\\baugust\\b|\\bdown\\b|\\bhang\\b|\\bnarrows\\b|\\brush*\\b|\\bterm\\b|\\bautumn\\b|\\bdownhil\\b|\\bhappening\\b|\\bnation\\b|\\bsank\\b|\\bterminat*\\b|\\bavenue*\\b|\\bdownstairs\\b|\\bheaded\\b|\\bnationa\\b|\\bsat\\b|\\bterritor*\\b|\\baway\\b|\\bdowntown\\b|\\bheadin*\\b|\\bnationality\\b|\\bsaturday*\\b|\\bthen\\b|\\bawhile\\b|\\bdownward*\\b|\\bheight*\\b|\\bnationally\\b|\\bschedul*\\b|\\bthick*\\b|\\bback\\b|\\bdrift*\\b|\\bhigh\\b|\\bnationals\\b|\\bscoot\\b|\\bthin\\b|\\bbackward*\\b|\\bdrive\\b|\\bhigher\\b|\\bnations\\b|\\bseason*\\b|\\bthinly\\b|\\bbedtime\\b|\\bdriven\\b|\\bhighest\\b|\\bnear\\b|\\bseconds\\b|\\bthinned\\b|\\bbefore\\b|\\bdrives\\b|\\bhik*\\b|\\bneared\\b|\\bsection\\b|\\bthinner\\b|\\bbegan\\b|\\bdriving\\b|\\bhistor*\\b|\\bnearer\\b|\\bsector*\\b|\\bthinnest\\b|\\bbegin\\b|\\bdrop\\b|\\bhole*\\b|\\bnearest\\b|\\bsegment*\\b|\\bthrew\\b|\\bbeginner\\b|\\bdrove\\b|\\bhop\\b|\\bnearing\\b|\\bseldom\\b|\\bthrow\\b|\\bbeginning*\\b|\\bdue\\b|\\bhorizontal*\\b|\\bnears\\b|\\bseldomly\\b|\\bthrown\\b|\\bbegins\\b|\\bdump*\\b|\\bhour*\\b|\\bneighbor*\\b|\\bsemester*\\b|\\bthrows\\b|\\bbegun\\b|\\bduring\\b|\\bhuge\\b|\\bneighbour*\\b|\\bsend\\b|\\bthurs\\b|\\bbehavio*\\b|\\bearlier\\b|\\bhugely\\b|\\bnever\\b|\\bsender\\b|\\bthursday*\\b|\\bbehind\\b|\\bearliest\\b|\\bhuger\\b|\\bnew\\b|\\bsending\\b|\\btil\\b|\\bbelow\\b|\\bearly\\b|\\bhugest\\b|\\bnewer\\b|\\bsends\\b|\\btill\\b|\\bbend\\b|\\bearth\\b|\\bhurrie*\\b|\\bnewest\\b|\\bsenior*\\b|\\btime*\\b|\\bbending\\b|\\beast*\\b|\\bhurry*\\b|\\bnewly\\b|\\bsent\\b|\\btiming\\b|\\bbends\\b|\\bedge*\\b|\\bimmediate\\b|\\bnext\\b|\\bseparat*\\b|\\btiniest\\b|\\bbeneath\\b|\\belapse*\\b|\\bimmediately\\b|\\bnight\\b|\\bseptember*\\b|\\btiny\\b|\\bbent\\b|\\belsewhere\\b|\\bimmediateness\\b|\\bnightly\\b|\\bsequen*\\b|\\btiptoe*\\b|\\bbeside\\b|\\bemptier\\b|\\bimmortal*\\b|\\bnights\\b|\\bshake*\\b|\\btoday*\\b|\\bbeyond\\b|\\bemptiest\\b|\\bin\\b|\\bnoon*\\b|\\bshape*\\b|\\btogether\\b|\\bbiannu*\\b|\\bemptiness\\b|\\binch*\\b|\\bnorth*\\b|\\bshaping*\\b|\\btomorrow*\\b|\\bbig\\b|\\bempty\\b|\\binciden*\\b|\\bnovembe\\b|\\bshook\\b|\\btonight*\\b|\\bbigger\\b|\\bemtpie*\\b|\\bincreas*\\b|\\bnow\\b|\\bshort\\b|\\btop\\b|\\bbiggest\\b|\\benclos*\\b|\\bindirect*\\b|\\bnowhere\\b|\\bshorter\\b|\\btoward*\\b|\\bbimonth*\\b|\\bencompass*\\b|\\binferior\\b|\\bo'clock*\\b|\\bshortest\\b|\\btown\\b|\\bbirth*\\b|\\bend\\b|\\binfinit*\\b|\\boccasion\\b|\\bshortly\\b|\\btransfer*\\b|\\bbiweek*\\b|\\bended\\b|\\binfrequent\\b|\\boccasional*\\b|\\bshove\\b|\\btransport*\\b|\\bborder*\\b|\\bending\\b|\\binitial*\\b|\\boccasions\\b|\\bshoved\\b|\\btrave\\b|\\bborn\\b|\\bends\\b|\\binitiat*\\b|\\boclock*\\b|\\bshoves\\b|\\btraveled\\b|\\bboth\\b|\\benorm*\\b|\\binner*\\b|\\boctober\\b|\\bshoving\\b|\\btraveler*\\b|\\bbottom\\b|\\benter\\b|\\binside\\b|\\boff\\b|\\bshrug*\\b|\\btraveling\\b|\\bbottomless\\b|\\bentered\\b|\\binsides\\b|\\boften\\b|\\bshut\\b|\\btravels\\b|\\bbounce\\b|\\bentering\\b|\\binstan*\\b|\\bold\\b|\\bside\\b|\\btrembl*\\b|\\bbounces\\b|\\benters\\b|\\binterior*\\b|\\bolden\\b|\\bsides\\b|\\btrip\\b|\\bbouncing\\b|\\bentrance*\\b|\\binterna\\b|\\bolder\\b|\\bsiding\\b|\\btripped\\b|\\bbreadth\\b|\\benvironment\\b|\\binternally\\b|\\boldest\\b|\\bsimultaneous*\\b|\\btripping\\b|\\bbreak\\b|\\bera\\b|\\binternation*\\b|\\bon\\b|\\bsince\\b|\\btrips\\b|\\bbrief\\b|\\beras\\b|\\bintersect*\\b|\\bonce\\b|\\bsinking\\b|\\btrot\\b|\\bbriefly\\b|\\bescap*\\b|\\bintertwine\\b|\\bonto\\b|\\bsit\\b|\\btrots\\b|\\bbring\\b|\\betern*\\b|\\bintertwined\\b|\\bopen\\b|\\bsite\\b|\\btrotted\\b|\\bbringing\\b|\\bevad*\\b|\\binterval*\\b|\\bopened\\b|\\bsites\\b|\\btrotting\\b|\\bbrings\\b|\\beve\\b|\\binto\\b|\\bopening*\\b|\\bsits\\b|\\btues\\b|\\bbrink\\b|\\bevening*\\b|\\birregularly\\b|\\bopens\\b|\\bsitting\\b|\\btuesday*\\b|\\bbroad\\b|\\beven\\b|\\bjanuary\\b|\\borbit\\b|\\bsky*\\b|\\btumble\\b|\\bbroader\\b|\\beventuall\\b|\\bjog*\\b|\\border\\b|\\bslid\\b|\\btumbled\\b|\\bbroadest\\b|\\bever\\b|\\bjourney*\\b|\\borigin\\b|\\bslide\\b|\\btumbles\\b|\\bbrought\\b|\\beveryda\\b|\\bjuly\\b|\\boriginally\\b|\\bslides\\b|\\btumbling\\b|\\bbumfuck\\b|\\beverytime\\b|\\bjump\\b|\\bout\\b|\\bsliding\\b|\\bturn\\b|\\bbusy\\b|\\beverywhere\\b|\\bjumped\\b|\\bouter*\\b|\\bslip\\b|\\bturned\\b|\\bbye\\b|\\bexit*\\b|\\bjumping\\b|\\boutside\\b|\\bslipping\\b|\\bturns\\b|\\bcame\\b|\\bexpand*\\b|\\bjumps\\b|\\boutsides\\b|\\bslow\\b|\\btwirl*\\b|\\bcapacit*\\b|\\bexplor*\\b|\\bjune\\b|\\boutward*\\b|\\bslowed\\b|\\btwist*\\b|\\bcar\\b|\\bexterior*\\b|\\bkilometer*\\b|\\bover\\b|\\bslower\\b|\\btwitch\\b|\\bcarried\\b|\\bfade*\\b|\\bkm*\\b|\\boverflow*\\b|\\bslowest\\b|\\btwitched\\b|\\bcarrier*\\b|\\bfading*\\b|\\bland\\b|\\boverlap*\\b|\\bslowing\\b|\\btwitches\\b|\\bcarries\\b|\\bfall\\b|\\blarge\\b|\\bpass\\b|\\bslowly\\b|\\btwitching\\b|\\bcarry\\b|\\bfallen\\b|\\blargely\\b|\\bpassed\\b|\\bslows\\b|\\btwitchy\\b|\\bcarrying\\b|\\bfalling\\b|\\blarger\\b|\\bpasses\\b|\\bsmall\\b|\\bunder\\b|\\bcatch\\b|\\bfalls\\b|\\blargest\\b|\\bpassing\\b|\\bsmaller\\b|\\bunderneath\\b|\\bcaught\\b|\\bfar\\b|\\blast*\\b|\\bpast\\b|\\bsmallest\\b|\\bundersid*\\b|\\bcease*\\b|\\bfarther\\b|\\blate\\b|\\bperiod*\\b|\\bsometime\\b|\\buniverse*\\b|\\bceasing\\b|\\bfarthest\\b|\\blately\\b|\\bpermanen\\b|\\bsometimes\\b|\\buntil\\b|\\bceiling*\\b|\\bfast\\b|\\blater\\b|\\bperpetual*\\b|\\bsomewhere\\b|\\buntwist*\\b|\\bcenter*\\b|\\bfaster\\b|\\blatera\\b|\\bpivot\\b|\\bsoon\\b|\\bup\\b|\\bcentral*\\b|\\bfastest\\b|\\blatest\\b|\\bplace\\b|\\bsooner\\b|\\bupdat*\\b|\\bcentre*\\b|\\bfebruary\\b|\\blaunch*\\b|\\bplaced\\b|\\bsoonest\\b|\\bupon\\b|\\bcentur*\\b|\\bfell\\b|\\blead\\b|\\bplacement*\\b|\\bsouth*\\b|\\bupper\\b|\\bchange\\b|\\bfill*\\b|\\bleading\\b|\\bplaces\\b|\\bspace\\b|\\buppermost\\b|\\bchanged\\b|\\bfinal\\b|\\bleads\\b|\\bplacing*\\b|\\bspaced\\b|\\bupright\\b|\\bchanges\\b|\\bfinale\\b|\\bleave\\b|\\bplatform*\\b|\\bspaces\\b|\\bupstairs\\b|\\bchanging\\b|\\bfinally\\b|\\bleaves\\b|\\bpoint\\b|\\bspaci*\\b|\\busual\\b|\\bchildhood\\b|\\bfinish\\b|\\bleaving\\b|\\bposition*\\b|\\bspan\\b|\\busually\\b|\\bchristmas*\\b|\\bfinishes\\b|\\bled\\b|\\bpost\\b|\\bspann*\\b|\\bvast\\b|\\bchronic*\\b|\\bfinishing\\b|\\bledge*\\b|\\bposterior\\b|\\bsped\\b|\\bvastly\\b|\\bcirculat*\\b|\\bfirst\\b|\\bleft\\b|\\bpranc*\\b|\\bspeed*\\b|\\bvastness\\b|\\bcity\\b|\\bfirstly\\b|\\blength\\b|\\bpreced*\\b|\\bspin\\b|\\bverg*\\b|\\bclimb*\\b|\\bfirsts\\b|\\bleve\\b|\\bpremier*\\b|\\bspiral\\b|\\bvertical*\\b|\\bclock*\\b|\\bfit\\b|\\blevels\\b|\\bpresent\\b|\\bsplit*\\b|\\bvia\\b|\\bclose\\b|\\bflapping\\b|\\blifetime*\\b|\\bpresently\\b|\\bsprawl*\\b|\\bvibrate\\b|\\bclosed\\b|\\bflat\\b|\\blil\\b|\\bprevious*\\b|\\bspring\\b|\\bvisit\\b|\\bclosely\\b|\\bfled\\b|\\blil'\\b|\\bprior\\b|\\bsprint*\\b|\\bvisited\\b|\\bcloser\\b|\\bflee\\b|\\blinear\\b|\\bproceed*\\b|\\bspun\\b|\\bvisiting\\b|\\bcloses\\b|\\bfleeing\\b|\\blink*\\b|\\bprocrastin*\\b|\\bstair*\\b|\\bvisits\\b|\\bclosest\\b|\\bflees\\b|\\blittle\\b|\\bprovinc*\\b|\\bstart\\b|\\bwaddl*\\b|\\bclosing\\b|\\bflew\\b|\\blittler\\b|\\bproxima\\b|\\bstarted\\b|\\bwaft*\\b|\\bcolumn*\\b|\\bflies\\b|\\blittlest\\b|\\bproximity\\b|\\bstarter*\\b|\\bwag\\b|\\bcome\\b|\\bflight*\\b|\\blocal\\b|\\bpull*\\b|\\bstarting\\b|\\bwagged\\b|\\bcomes\\b|\\bfloor*\\b|\\blocale*\\b|\\bpush\\b|\\bstarts\\b|\\bwagging\\b|\\bcoming\\b|\\bflow\\b|\\blocalis*\\b|\\bpushe*\\b|\\bstartup*\\b|\\bwags\\b|\\bcommon\\b|\\bflowed\\b|\\blocalit*\\b|\\bpushing\\b|\\bstay\\b|\\bwait\\b|\\bcommute*\\b|\\bflowing\\b|\\blocaliz*\\b|\\bpushup*\\b|\\bstayed\\b|\\bwaited\\b|\\bcommuting\\b|\\bflown\\b|\\blocally\\b|\\bput\\b|\\bstaying\\b|\\bwaiting\\b|\\bconnection*\\b|\\bflows\\b|\\blocals\\b|\\bputs\\b|\\bstays\\b|\\bwaits\\b|\\bconstant\\b|\\bflutter\\b|\\blocat*\\b|\\bputting\\b|\\bstep\\b|\\bwalk\\b|\\bconstantly\\b|\\bfly\\b|\\blong\\b|\\bquick\\b|\\bstepp*\\b|\\bwalked\\b|\\bcontain*\\b|\\bflying\\b|\\blonger\\b|\\bquicken*\\b|\\bsteps\\b|\\bwalking\\b|\\bcontinually\\b|\\bfollow\\b|\\blongest\\b|\\bquicker\\b|\\bstill\\b|\\bwalks\\b|\\bcontinue\\b|\\bfollowed\\b|\\blongevity\\b|\\bquickest\\b|\\bstir\\b|\\bwall\\b|\\bcontinued\\b|\\bfollowing\\b|\\blongitud*\\b|\\bquickly\\b|\\bstirred\\b|\\bwalls\\b|\\bcontinues\\b|\\bfollows\\b|\\blow\\b|\\bran\\b|\\bstirring\\b|\\bwarehous*\\b|\\bcorner\\b|\\bfollowup*\\b|\\blower\\b|\\brapid\\b|\\bstirs\\b|\\bwave\\b|\\bcorners\\b|\\bforever\\b|\\blowered\\b|\\brarely\\b|\\bstop\\b|\\bway\\b",re.IGNORECASE)
discrep_re=re.compile("\\babnormal*\\b|\\bbesides\\b|\\bcould\\b|\\bcould've\\b|\\bcouldn't\\b|\\bcouldnt\\b|\\bcouldve\\b|\\bdesir*\\b|\\bexpect*\\b|\\bhope\\b|\\bhoped\\b|\\bhopeful\\b|\\bhopefully\\b|\\bhopes\\b|\\bhoping\\b|\\bideal*\\b|\\bif\\b|\\bimpossible\\b|\\binadequa*\\b|\\black\\b|\\blacked\\b|\\blacking\\b|\\blacks\\b|\\bliabilit*\\b|\\bmistak*\\b|\\bmust\\b|\\bmust'nt\\b|\\bmustn't\\b|\\bmustnt\\b|\\bneed\\b|\\bneed'nt\\b|\\bneeded\\b|\\bneeding\\b|\\bneedn't\\b|\\bneednt\\b|\\bneeds\\b|\\bnormally\\b|\\bodd\\b|\\bodder\\b|\\boddest\\b|\\bought\\b|\\bought'nt\\b|\\bought've\\b|\\boughta\\b|\\boughtn't\\b|\\boughtnt\\b|\\boughtve\\b|\\boutstanding\\b|\\bprefer*\\b|\\bproblem*\\b|\\brather\\b|\\bregardless\\b|\\bregret*\\b|\\bshould\\b|\\bshould'nt\\b|\\bshould've\\b|\\bshouldn't\\b|\\bshouldnt\\b|\\bshouldve\\b|\\bundesir*\\b|\\bundid\\b|\\bundo\\b|\\bundoes\\b|\\bundoing\\b|\\bundone\\b|\\bunneccess*\\b|\\bunusual\\b|\\bunwanted\\b|\\bwanna\\b|\\bwant\\b|\\bwanted\\b|\\bwanting\\b|\\bwants\\b|\\bwish\\b|\\bwished\\b|\\bwishes\\b|\\bwishing\\b|\\bwould\\b|\\bwould've\\b|\\bwouldn't\\b|\\bwouldnt\\b|\\bwouldve\\b|\\byearn*\\b",re.IGNORECASE)

posemo_re=re.compile("\:\)|\\bentertain*\\b|\\bhugs\\b|\\bpromising\\b|\\bwealthy\\b|\(\:|\\benthus*\\b|\\bhumor*\\b|\\bproud\\b|\\bwelcom*\\b|\\baccept\\b|\\bexce\\b|\\bhumour*\\b|\\bprouder\\b|\\bwell\\b|\\baccepta*\\b|\\bexcelled\\b|\\bhurra*\\b|\\bproudest\\b|\\bwellbeing\\b|\\baccepted\\b|\\bexcellence\\b|\\bideal*\\b|\\bproudly\\b|\\bwellness\\b|\\baccepting\\b|\\bexcellen\\b|\\bily*\\b|\\bradian*\\b|\\bwin\\b|\\baccepts\\b|\\bexcellently\\b|\\bimportance\\b|\\breadiness\\b|\\bwinn*\\b|\\bactive\\b|\\bexcelling\\b|\\bimportant\\b|\\bready\\b|\\bwins\\b|\\bactively\\b|\\bexcels\\b|\\bimportantly\\b|\\breassur*\\b|\\bwisdom\\b|\\badmir*\\b|\\bexcite\\b|\\bimpress*\\b|\\breinvigor*\\b|\\bwise\\b|\\bador*\\b|\\bexcited\\b|\\bimprove*\\b|\\brejoice*\\b|\\bwisely\\b|\\badvantag\\b|\\bexcitedly\\b|\\bimproving\\b|\\brelax*\\b|\\bwiser\\b|\\badventur*\\b|\\bexcitemen\\b|\\bincentive*\\b|\\brelief\\b|\\bwisest\\b|\\baffection*\\b|\\bexciting\\b|\\binnocen*\\b|\\breliev*\\b|\\bwon\\b|\\bagree\\b|\\bfab\\b|\\binspir*\\b|\\bresolv*\\b|\\bwonderfu\\b|\\bagreeable\\b|\\bfabulous\\b|\\bintellect*\\b|\\brespect\\b|\\bwonderfully\\b|\\bagreeablenes\\b|\\bfabulously\\b|\\bintelligence\\b|\\brespected\\b|\\bworship*\\b|\\bagreeably\\b|\\bfabulousness\\b|\\bintelligen\\b|\\brespectful\\b|\\bworthwhile\\b|\\bagreed\\b|\\bfair\\b|\\binterest\\b|\\brespectfully\\b|\\bwow*\\b|\\bagreeing\\b|\\bfairer\\b|\\binterested\\b|\\brespecting\\b|\\byay*\\b|\\bagreement\\b|\\bfairest\\b|\\binteresting\\b|\\breward*\\b|\\byum\\b|\\bagrees\\b|\\bfaith*\\b|\\binterests\\b|\\brich\\b|\\byummy\\b|\\balright*\\b|\\bfantasi*\\b|\\binvigor*\\b|\\bricher\\b|\\bamaze*\\b|\\bfantastic\\b|\\bjoke*\\b|\\briches\\b|\\bamazing\\b|\\bfantastical\\b|\\bjoking\\b|\\brichest\\b|\\bamazingly\\b|\\bfantastically\\b|\\bjolly\\b|\\brofl*\\b|\\bamor*\\b|\\bfantasy\\b|\\bjoy*\\b|\\bromanc*\\b|\\bamus*\\b|\\bfav\\b|\\bkeen*\\b|\\bromantic*\\b|\\baok\\b|\\bfave\\b|\\bkidding\\b|\\bsafe\\b|\\bappreciat*\\b|\\bfavor\\b|\\bkind\\b|\\bsafely\\b|\\bapprov*\\b|\\bfavoring\\b|\\bkindly\\b|\\bsafer\\b|\\bassur*\\b|\\bfavorite\\b|\\bkindn*\\b|\\bsafest\\b|\\battract\\b|\\bfavors\\b|\\bkiss*\\b|\\bsafety\\b|\\battracted\\b|\\bfavour*\\b|\\blaidback\\b|\\bsatisf*\\b|\\battracting\\b|\\bfearless*\\b|\\blaugh*\\b|\\bsave\\b|\\battraction\\b|\\bfestiv*\\b|\\blegit\\b|\\bscrumptious*\\b|\\battracts\\b|\\bfiesta*\\b|\\blibert*\\b|\\bsecur*\\b|\\baward*\\b|\\bfine\\b|\\bto like\\b|\\bsentimental*\\b|\\bawesome\\b|\\bfiner\\b|\\bi like*\\b|\\bsexy\\b|\\bbeautifu\\b|\\bfinest\\b|\\byou like*\\b|\\bshare\\b|\\bbeautify\\b|\\bflatter*\\b|\\bwe like*\\b|\\bshared\\b|\\bbeauty\\b|\\bflawless*\\b|\\bthey like*\\b|\\bshares\\b|\\bbeloved\\b|\\bflexib*\\b|\\bdo like\\b|\\bsharing\\b|\\bbenefic*\\b|\\bflirt\\b|\\bdon't like\\b|\\bsillier\\b|\\bbenefit\\b|\\bflirtatious\\b|\\bdid like\\b|\\bsilliest\\b|\\bbenefits\\b|\\bflirting\\b|\\bdidn't like\\b|\\bsilly\\b|\\bbenefitt*\\b|\\bflirts\\b|\\bwill like\\b|\\bsincer*\\b|\\bbenevolen\\b|\\bflirty\\b|\\bwon't like\\b|\\bsmart\\b|\\bbest\\b|\\bfond\\b|\\bdoes like\\b|\\bsmarter\\b|\\bbestest\\b|\\bfondly\\b|\\bdoesn't like\\b|\\bsmartest\\b|\\bbestie\\b|\\bfondness\\b|\\bdid not like\\b|\\bsmartly\\b|\\bbesties\\b|\\bforgave\\b|\\bwill not like\\b|\\bsmil*\\b|\\bbetter\\b|\\bforgiv*\\b|\\bdo not like\\b|\\bsociability\\b|\\bbless*\\b|\\bfortunately\\b|\\bdoes not like\\b|\\bsociable\\b|\\bbliss*\\b|\\bfree\\b|\\bwould not like\\b|\\bsoulmate*\\b|\\bbold\\b|\\bfree-think*\\b|\\bshould not like\\b|\\bspecial\\b|\\bbolder\\b|\\bfreed*\\b|\\bcould not like\\b|\\bsplendid\\b|\\bboldest\\b|\\bfreeing\\b|\\bdiscrep like*\\b|\\bsplendidly\\b|\\bboldly\\b|\\bfreely\\b|\\blikeab*\\b|\\bsplendor\\b|\\bbonus*\\b|\\bfrees*\\b|\\bliked\\b|\\bstrength*\\b|\\bbrave\\b|\\bfreethink*\\b|\\blikes\\b|\\bstrong\\b|\\bbraved\\b|\\bfun\\b|\\bliking\\b|\\bstronger\\b|\\bbraver\\b|\\bfunner\\b|\\blivel*\\b|\\bstrongest\\b|\\bbravery\\b|\\bfunnest\\b|\\blmao*\\b|\\bstrongly\\b|\\bbraves\\b|\\bfunnier\\b|\\blmfao*\\b|\\bsucceed*\\b|\\bbravest\\b|\\bfunnies\\b|\\blol\\b|\\bsuccess\\b|\\bbright\\b|\\bfunniest\\b|\\blove\\b|\\bsuccesses\\b|\\bbrilliance*\\b|\\bfunnily\\b|\\bloved\\b|\\bsuccessful\\b|\\bbrilliant\\b|\\bfunniness\\b|\\blovelie\\b|\\bsuccessfully\\b|\\bbrilliantly\\b|\\bfunny\\b|\\blovelies\\b|\\bsunnier\\b|\\bcalm\\b|\\bgenero*\\b|\\blovely\\b|\\bsunniest\\b|\\bcalmer\\b|\\bgentle\\b|\\blover*\\b|\\bsunny\\b|\\bcalmest\\b|\\bgentler\\b|\\bloves\\b|\\bsunshin*\\b|\\bcalming\\b|\\bgentlest\\b|\\bloving*\\b|\\bsuper\\b|\\bcare\\b|\\bgently\\b|\\bloya\\b|\\bsuperb*\\b|\\bcared\\b|\\bgiggl*\\b|\\bloyalt*\\b|\\bsuperior\\b|\\bcarefree\\b|\\bgiver*\\b|\\bluck\\b|\\bsupport\\b|\\bcares\\b|\\bgiving\\b|\\blucked\\b|\\bsupported\\b|\\bcaring\\b|\\bglad\\b|\\bluckier\\b|\\bsupporter*\\b|\\bcertain*\\b|\\bgladly\\b|\\bluckiest\\b|\\bsupporting\\b|\\bchalleng*\\b|\\bglamor*\\b|\\bluckily\\b|\\bsupportive\\b|\\bchamp*\\b|\\bglamour*\\b|\\blucky\\b|\\bsupports\\b|\\bcharit*\\b|\\bglori*\\b|\\bluv\\b|\\bsuprem*\\b|\\bcharm*\\b|\\bglory\\b|\\bmagnific*\\b|\\bsure*\\b|\\bcheer\\b|\\bgood\\b|\\bmerit*\\b|\\bsurprise\\b|\\bcheerful\\b|\\bgoodness\\b|\\bmerr*\\b|\\bsurprised*\\b|\\bcheers\\b|\\bgorgeous\\b|\\bneat\\b|\\bsurprising*\\b|\\bcheery\\b|\\bgorgeously\\b|\\bneater\\b|\\bsweet\\b|\\bcherish*\\b|\\bgorgeousness\\b|\\bneatest\\b|\\bsweeter\\b|\\bchuckl*\\b|\\bgrace\\b|\\bneatness\\b|\\bsweetest\\b|\\bclever\\b|\\bgraced\\b|\\bnice\\b|\\bsweetheart*\\b|\\bcomed*\\b|\\bgraceful*\\b|\\bnicely\\b|\\bsweetie*\\b|\\bcomfort\\b|\\bgraces\\b|\\bniceness*\\b|\\bsweetly\\b|\\bcomfortable\\b|\\bgraci*\\b|\\bnicer\\b|\\bsweetness*\\b|\\bcomfortably\\b|\\bgrand\\b|\\bnicest\\b|\\bsweets\\b|\\bcomforting\\b|\\bgrande*\\b|\\bniceties\\b|\\btalent*\\b|\\bcomforts\\b|\\bgratef*\\b|\\bnurtur*\\b|\\bteehe*\\b|\\bcompassion*\\b|\\bgrati*\\b|\\bok\\b|\\btender\\b|\\bcompliment*\\b|\\bgreat\\b|\\bokay\\b|\\btenderly\\b|\\bconfidence\\b|\\bgreater\\b|\\bokayed\\b|\\bterrific\\b|\\bconfident\\b|\\bgreatest\\b|\\bokays\\b|\\bterrifically\\b|\\bconfidently\\b|\\bgreatness\\b|\\bokey*\\b|\\bthank\\b|\\bconsiderate\\b|\\bgrin\\b|\\boks\\b|\\bthanked\\b|\\bcontented*\\b|\\bgrinn*\\b|\\bopen-minded\\b|\\bthankful\\b|\\bcontentmen\\b|\\bgrins\\b|\\bopenminded\\b|\\bthankfully\\b|\\bcool\\b|\\bha\\b|\\bopenness\\b|\\bthanking\\b|\\bcourag*\\b|\\bhah\\b|\\bopportun*\\b|\\bthanks\\b|\\bcreate\\b|\\bhaha*\\b|\\boptimal*\\b|\\bthanx\\b|\\bcreated\\b|\\bhandsome\\b|\\boptimism\\b|\\bthnx\\b|\\bcreates\\b|\\bhandsomely\\b|\\boptimistic\\b|\\bthoughtful*\\b|\\bcreating\\b|\\bhandsomes\\b|\\borigina\\b|\\bthrill*\\b|\\bcreation\\b|\\bhappier\\b|\\boutgoing\\b|\\bthx\\b|\\bcreations\\b|\\bhappiest\\b|\\bparadise*\\b|\\btoleran*\\b|\\bcreative\\b|\\bhappily\\b|\\bpartie*\\b|\\btranquil*\\b|\\bcreativity\\b|\\bhappiness\\b|\\bparty*\\b|\\btreasur*\\b|\\bcredit*\\b|\\bhappy\\b|\\bpassion*\\b|\\btreat\\b|\\bcute\\b|\\bharmon*\\b|\\bpeace\\b|\\btriumph*\\b|\\bcuter\\b|\\bheal\\b|\\bpeacefu\\b|\\btrue\\b|\\bcutest\\b|\\bhealed\\b|\\bpeacefully\\b|\\btruer\\b|\\bcutie*\\b|\\bhealer*\\b|\\bpeacekeep\\b|\\btruest\\b|\\bdaring\\b|\\bhealing\\b|\\bpeacemak*\\b|\\btruly\\b|\\bdarlin*\\b|\\bheals\\b|\\bperfect\\b|\\btrust\\b|\\bdear\\b|\\bhealthy\\b|\\bperfected\\b|\\btrusted\\b|\\bdearly\\b|\\bheartfelt\\b|\\bperfecting\\b|\\btrusting\\b|\\bdecent\\b|\\bheartwarm*\\b|\\bperfection\\b|\\btrusts\\b|\\bdefinitely\\b|\\bheaven*\\b|\\bperfectly\\b|\\btrustworthiness\\b|\\bdelectabl*\\b|\\bheh*\\b|\\bplay\\b|\\btrustworthy\\b|\\bdelicate*\\b|\\bhelper*\\b|\\bplayed\\b|\\btrusty\\b|\\bdelicious*\\b|\\bhelpful\\b|\\bplayful\\b|\\btruth*\\b|\\bdeligh*\\b|\\bhelpfully\\b|\\bplayfully\\b|\\bty\\b|\\bdesir*\\b|\\bhelpfulness\\b|\\bplayfulness\\b|\\bupbeat\\b|\\bdetermina*\\b|\\bhelping\\b|\\bplaying\\b|\\buseful\\b|\\bdetermined\\b|\\bhelps\\b|\\bplays\\b|\\busefully\\b|\\bdevot*\\b|\\bhero\\b|\\bpleasant*\\b|\\busefulness\\b|\\bdignified\\b|\\bhero's\\b|\\bplease*\\b|\\bvaluabl*\\b|\\bdignifies\\b|\\bheroes\\b|\\bpleasing\\b|\\bvalue\\b|\\bdignifying\\b|\\bheroic*\\b|\\bpleasur*\\b|\\bvalued\\b|\\bdignity\\b|\\bheroine*\\b|\\bpolite\\b|\\bvalues\\b|\\bdivin*\\b|\\bheroism\\b|\\bpolitely\\b|\\bvaluing\\b|\\beager\\b|\\bhilarious\\b|\\bpopular\\b|\\bvigor*\\b|\\beagerly\\b|\\bhoho*\\b|\\bpopulari*\\b|\\bvigour*\\b|\\beagerness\\b|\\bhonest\\b|\\bpositive\\b|\\bvirtue*\\b|\\bease*\\b|\\bhonestly\\b|\\bpositively\\b|\\bvirtuo*\\b|\\beasier\\b|\\bhonesty\\b|\\bpositives\\b|\\bvital*\\b|\\beasiest\\b|\\bhonor*\\b|\\bpositivi*\\b|\\bwarm\\b|\\beasily\\b|\\bhonour*\\b|\\bprais*\\b|\\bwarmed\\b|\\beasiness\\b|\\bhooray\\b|\\bprecious*\\b|\\bwarmer\\b|\\beasing\\b|\\bhope\\b|\\bprettier\\b|\\bwarmest\\b|\\beasy*\\b|\\bhoped\\b|\\bprettiest\\b|\\bwarming\\b|\\becsta*\\b|\\bhopeful\\b|\\bpretty\\b|\\bwarmly\\b|\\belegan*\\b|\\bhopefully\\b|\\bpride\\b|\\bwarms\\b|\\bencourag*\\b|\\bhopes\\b|\\bprivileg*\\b|\\bwarmth\\b|\\benerg*\\b|\\bhoping\\b|\\bprize*\\b|\\bwealth\\b|\\bengag*\\b|\\bhug\\b|\\bprofit*\\b|\\bwealthie\\b|\\benjoy*\\b|\\bhugg*\\b|\\bpromise*\\b|\\bwealthies\\b",re.IGNORECASE)
negemo_re=re.compile("\:\(|\\bdismay*\\b|\\bignorant\\b|\\bpoorest\\b|\\btragic\\b|\)\:|\\bdisreput*\\b|\\bignore\\b|\\bpoorly\\b|\\btrauma*\\b|\\babandon*\\b|\\bdiss\\b|\\bignored\\b|\\bpoorness*\\b|\\btrembl*\\b|\\babuse*\\b|\\bdissatisf*\\b|\\bignores\\b|\\bpowerless*\\b|\\btrick\\b|\\babusi*\\b|\\bdistraught\\b|\\bignoring\\b|\\bprejudic*\\b|\\btricked\\b|\\bache*\\b|\\bdistress*\\b|\\bimmoral*\\b|\\bpressur*\\b|\\btrickier\\b|\\baching*\\b|\\bdistrust*\\b|\\bimpatien*\\b|\\bprick*\\b|\\btrickiest\\b|\\badvers*\\b|\\bdisturb*\\b|\\bimpersona\\b|\\bproblem*\\b|\\btricks\\b|\\bafraid\\b|\\bdomina*\\b|\\bimpolite*\\b|\\bprotest\\b|\\btricky\\b|\\baggravat*\\b|\\bdoom*\\b|\\binadequa*\\b|\\bprotested\\b|\\btrite\\b|\\baggress\\b|\\bdork*\\b|\\bincompeten*\\b|\\bprotesting\\b|\\btrivia\\b|\\baggressed\\b|\\bdoubt*\\b|\\bindecis*\\b|\\bprotests\\b|\\btroubl*\\b|\\baggresses\\b|\\bdread*\\b|\\bineffect*\\b|\\bpuk*\\b|\\bturmoil\\b|\\baggressing\\b|\\bdull\\b|\\binferior\\b|\\bpunish*\\b|\\btwitchy\\b|\\baggression*\\b|\\bdumb\\b|\\binferiority\\b|\\bpushy\\b|\\bugh\\b|\\baggressive\\b|\\bdumbass*\\b|\\binhibit*\\b|\\bqueas*\\b|\\buglier\\b|\\baggressively\\b|\\bdumber\\b|\\binsecur*\\b|\\brage*\\b|\\bugliest\\b|\\baggressor*\\b|\\bdumbest\\b|\\binsincer*\\b|\\braging\\b|\\bugly\\b|\\bagitat*\\b|\\bdummy\\b|\\binsult*\\b|\\brancid*\\b|\\bunaccept*\\b|\\bagoniz*\\b|\\bdump*\\b|\\binterrup*\\b|\\brape*\\b|\\bunattractive\\b|\\bagony\\b|\\bdwell*\\b|\\bintimidat*\\b|\\braping\\b|\\buncertain*\\b|\\balarm*\\b|\\begotis*\\b|\\birrational*\\b|\\brapist*\\b|\\buncomfortabl*\\b|\\balone\\b|\\bembarrass*\\b|\\birrita*\\b|\\brebel*\\b|\\buncontrol*\\b|\\banger*\\b|\\bemotiona\\b|\\bisolat*\\b|\\breek*\\b|\\bundesir*\\b|\\bangrier\\b|\\bemptier\\b|\\bjaded\\b|\\bregret*\\b|\\buneas*\\b|\\bangriest\\b|\\bemptiest\\b|\\bjealous\\b|\\breject*\\b|\\bunfair\\b|\\bangry\\b|\\bemptiness\\b|\\bjealousies\\b|\\breluctan*\\b|\\bunfortunate*\\b|\\banguish*\\b|\\bempty\\b|\\bjealously\\b|\\bremorse*\\b|\\bunfriendly\\b|\\bannoy\\b|\\benemie*\\b|\\bjealousy\\b|\\brepress*\\b|\\bungrateful*\\b|\\bannoyed\\b|\\benemy*\\b|\\bjerk\\b|\\bresent*\\b|\\bunhapp*\\b|\\bannoying\\b|\\benrag*\\b|\\bjerked\\b|\\bresign*\\b|\\bunimportan\\b|\\bannoys\\b|\\benvie*\\b|\\bjerks\\b|\\brestless*\\b|\\bunimpress*\\b|\\bantagoni*\\b|\\benvious\\b|\\bkill*\\b|\\brevenge*\\b|\\bunkind\\b|\\banxiety\\b|\\benvy*\\b|\\blame\\b|\\bridicul*\\b|\\bunlov*\\b|\\banxious\\b|\\bevil\\b|\\blamely\\b|\\brigid\\b|\\bunlucky\\b|\\banxiously\\b|\\bexcruciat*\\b|\\blameness\\b|\\brigidity\\b|\\bunpleasan\\b|\\banxiousness\\b|\\bexhaust*\\b|\\blamer\\b|\\brigidly\\b|\\bunprotected\\b|\\bapath*\\b|\\bfail*\\b|\\blamest\\b|\\brisk*\\b|\\bunsafe\\b|\\bappall*\\b|\\bfake\\b|\\blazier\\b|\\brotten\\b|\\bunsavory\\b|\\bapprehens*\\b|\\bfatal*\\b|\\blaziest\\b|\\brude\\b|\\bunsettl*\\b|\\bargh*\\b|\\bfatigu*\\b|\\blazy\\b|\\brudely\\b|\\bunsuccessful*\\b|\\bargu*\\b|\\bfault*\\b|\\bliabilit*\\b|\\bruin*\\b|\\bunsure*\\b|\\barrogan*\\b|\\bfear\\b|\\bliar*\\b|\\bsad\\b|\\bunwelcom*\\b|\\basham*\\b|\\bfeared\\b|\\blied\\b|\\bsadder\\b|\\bupset\\b|\\bassault*\\b|\\bfearful*\\b|\\blies\\b|\\bsaddest\\b|\\bupsets\\b|\\basshole*\\b|\\bfearing\\b|\\blone\\b|\\bsadly\\b|\\bupsetting\\b|\\battack*\\b|\\bfears\\b|\\blonelier\\b|\\bsadness\\b|\\buptight*\\b|\\baversi*\\b|\\bferoc*\\b|\\blonelies\\b|\\bsarcas*\\b|\\buseless\\b|\\bavoid*\\b|\\bfeud*\\b|\\bloneliness\\b|\\bsavage*\\b|\\buselessly\\b|\\bawful\\b|\\bfiery\\b|\\blonely\\b|\\bscare\\b|\\buselessness\\b|\\bawkward\\b|\\bfight*\\b|\\bloner*\\b|\\bscared\\b|\\bvain\\b|\\bbad\\b|\\bfired\\b|\\blonging*\\b|\\bscares\\b|\\bvanity\\b|\\bbadly\\b|\\bflunk*\\b|\\blose\\b|\\bscarier\\b|\\bvicious\\b|\\bbashful*\\b|\\bfoe*\\b|\\bloser*\\b|\\bscariest\\b|\\bviciously\\b|\\bbastard*\\b|\\bfool\\b|\\bloses\\b|\\bscaring\\b|\\bviciousness\\b|\\bbattl*\\b|\\bfooled\\b|\\blosing\\b|\\bscary\\b|\\bvictim*\\b|\\bbeaten\\b|\\bfooling\\b|\\bloss*\\b|\\bsceptic*\\b|\\bvile\\b|\\bbereave\\b|\\bfoolish\\b|\\blost\\b|\\bscream*\\b|\\bvillain*\\b|\\bbitch*\\b|\\bfoolishly\\b|\\blous*\\b|\\bscrew*\\b|\\bviolat*\\b|\\bbitter\\b|\\bfools\\b|\\bloveless\\b|\\bselfish*\\b|\\bviolence\\b|\\bbitterly\\b|\\bforbade\\b|\\blow\\b|\\bserious\\b|\\bviolen\\b|\\bbitterness\\b|\\bforbid\\b|\\blower\\b|\\bseriously\\b|\\bviolently\\b|\\bblam*\\b|\\bforbidden\\b|\\blowered\\b|\\bseriousness\\b|\\bvomit*\\b|\\bbore*\\b|\\bforbidding\\b|\\blowering\\b|\\bsevere*\\b|\\bvulnerab*\\b|\\bboring\\b|\\bforbids\\b|\\blowers\\b|\\bshake*\\b|\\bwar\\b|\\bbother*\\b|\\bfought\\b|\\blowest\\b|\\bshaki*\\b|\\bwarfare*\\b|\\bbroke\\b|\\bfrantic*\\b|\\blowli*\\b|\\bshaky\\b|\\bwarn*\\b|\\bbrutal*\\b|\\bfreak*\\b|\\blowly\\b|\\bshame*\\b|\\bwarred\\b|\\bburden*\\b|\\bfright*\\b|\\bluckless*\\b|\\bshit*\\b|\\bwarring\\b|\\bcareless*\\b|\\bfrustrat*\\b|\\bludicrous*\\b|\\bshock*\\b|\\bwars\\b|\\bcheat*\\b|\\bfuck\\b|\\blying\\b|\\bshook\\b|\\bweak\\b|\\bcoldly\\b|\\bfucked*\\b|\\bmad\\b|\\bshy\\b|\\bweaken\\b|\\bcomplain*\\b|\\bfucker*\\b|\\bmaddening*\\b|\\bshyly\\b|\\bweakened\\b|\\bcondemn*\\b|\\bfuckface*\\b|\\bmadder\\b|\\bshyness\\b|\\bweakening\\b|\\bconfront*\\b|\\bfuckh*\\b|\\bmaddest\\b|\\bsick\\b|\\bweakens\\b|\\bconfuse\\b|\\bfuckin*\\b|\\bmaniac*\\b|\\bsicken*\\b|\\bweaker\\b|\\bconfused\\b|\\bfucks\\b|\\bmasochis*\\b|\\bsicker\\b|\\bweakes\\b|\\bconfusedly\\b|\\bfucktard\\b|\\bmeaner\\b|\\bsickest\\b|\\bweakling\\b|\\bconfusing\\b|\\bfucktwat*\\b|\\bmeanest\\b|\\bsickly\\b|\\bweakly\\b|\\bcontempt*\\b|\\bfuckwad*\\b|\\bmelanchol*\\b|\\bsigh\\b|\\bweapon*\\b|\\bcontradic*\\b|\\bfume*\\b|\\bmess\\b|\\bsighed\\b|\\bweary\\b|\\bcrap\\b|\\bfuming\\b|\\bmessier\\b|\\bsighing\\b|\\bweep*\\b|\\bcrappy\\b|\\bfurious*\\b|\\bmessiest\\b|\\bsighs\\b|\\bweird\\b|\\bcrazy\\b|\\bfury\\b|\\bmessy\\b|\\bsin\\b|\\bweirded\\b|\\bcried\\b|\\bgeek*\\b|\\bmiser*\\b|\\bsinister\\b|\\bweirder\\b|\\bcries\\b|\\bgloom\\b|\\bmiss\\b|\\bsins\\b|\\bweirdest\\b|\\bcritical\\b|\\bgloomie\\b|\\bmissed\\b|\\bslut*\\b|\\bweirdly\\b|\\bcritici*\\b|\\bgloomies\\b|\\bmisses\\b|\\bsmh\\b|\\bweirdness\\b|\\bcrude\\b|\\bgloomily\\b|\\bmissing\\b|\\bsmother*\\b|\\bweirdo\\b|\\bcrudely\\b|\\bgloominess\\b|\\bmistak*\\b|\\bsmug*\\b|\\bweirdos\\b|\\bcruel\\b|\\bgloomy\\b|\\bmock\\b|\\bsnob*\\b|\\bweirds\\b|\\bcrueler\\b|\\bgoddam*\\b|\\bmocked\\b|\\bsob\\b|\\bwept\\b|\\bcruelest\\b|\\bgood-for-nothing\\b|\\bmocker*\\b|\\bsobbed\\b|\\bwhine*\\b|\\bcruelty\\b|\\bgossip*\\b|\\bmocking\\b|\\bsobbing\\b|\\bwhining\\b|\\bcrushed\\b|\\bgrave*\\b|\\bmocks\\b|\\bsobs\\b|\\bwhore*\\b|\\bcry\\b|\\bgreed*\\b|\\bmolest*\\b|\\bsolemn*\\b|\\bwicked\\b|\\bcrying\\b|\\bgrief\\b|\\bmooch*\\b|\\bsorrow*\\b|\\bwickedly\\b|\\bcunt*\\b|\\bgriev*\\b|\\bmoodi*\\b|\\bsorry\\b|\\bwimp*\\b|\\bcurse\\b|\\bgrim\\b|\\bmoody\\b|\\bspite*\\b|\\bwitch*\\b|\\bcut\\b|\\bgrimac*\\b|\\bmoron*\\b|\\bstale\\b|\\bwoe*\\b|\\bcynic*\\b|\\bgrimly\\b|\\bmourn*\\b|\\bstammer*\\b|\\bworried\\b|\\bdamag*\\b|\\bgross\\b|\\bmurder*\\b|\\bstank*\\b|\\bworrier\\b|\\bdamn*\\b|\\bgrossed\\b|\\bnag*\\b|\\bstartl*\\b|\\bworries\\b|\\bdanger\\b|\\bgrosser\\b|\\bnast*\\b|\\bsteal*\\b|\\bworry\\b|\\bdangerous\\b|\\bgrossest\\b|\\bneedy\\b|\\bstench*\\b|\\bworrying\\b|\\bdangerously\\b|\\bgrossing\\b|\\bneglect*\\b|\\bstink\\b|\\bworse\\b|\\bdangers\\b|\\bgrossly\\b|\\bnerd*\\b|\\bstinky\\b|\\bworsen\\b|\\bdaze*\\b|\\bgrossness\\b|\\bnervous\\b|\\bstrain*\\b|\\bworsened\\b|\\bdecay*\\b|\\bgrouch*\\b|\\bnervously\\b|\\bstrange\\b|\\bworsening\\b|\\bdeceptive\\b|\\bgrr*\\b|\\bnervousness\\b|\\bstrangest\\b|\\bworsens\\b|\\bdeceiv*\\b|\\bgrudg*\\b|\\bneurotic*\\b|\\bstress*\\b|\\bworst\\b|\\bdefeat*\\b|\\bguilt\\b|\\bnightmar*\\b|\\bstruggl*\\b|\\bworthless\\b|\\bdefect*\\b|\\bguilt-trip*\\b|\\bnumbed\\b|\\bstubborn*\\b|\\bwrong\\b|\\bdefenc*\\b|\\bguiltier\\b|\\bnumbing\\b|\\bstunk\\b|\\bwrongdoing\\b|\\bdefend*\\b|\\bguiltiest\\b|\\bnumbness\\b|\\bstupid\\b|\\bwronged\\b|\\bdefense\\b|\\bguilty\\b|\\bnumbs\\b|\\bstupider\\b|\\bwrongful\\b|\\bdefenseless\\b|\\bhangover*\\b|\\bobnoxious*\\b|\\bstupidest\\b|\\bwrongly\\b|\\bdefensive\\b|\\bharass*\\b|\\bobsess*\\b|\\bstupidity\\b|\\bwrongness\\b|\\bdefensively\\b|\\bharm\\b|\\boffence*\\b|\\bstupidly\\b|\\bwrongs\\b|\\bdefensiveness\\b|\\bharmed\\b|\\boffend*\\b|\\bstutter*\\b|\\byearn*\\b|\\bdegrad*\\b|\\bharmful\\b|\\boffense\\b|\\bsuck\\b|\\byell\\b|\\bdemean*\\b|\\bharmfully\\b|\\boffenses\\b|\\bsucked\\b|\\byelled\\b|\\bdemot*\\b|\\bharmfulness\\b|\\boffensive\\b|\\bsucker*\\b|\\byelling\\b|\\bdenia\\b|\\bharming\\b|\\boutrag*\\b|\\bsucks\\b|\\byells\\b|\\bdepress*\\b|\\bharms\\b|\\boverwhelm\\b|\\bsucky\\b|\\byuck\\b|\\bdepriv*\\b|\\bharsh\\b|\\bpain\\b|\\bsuffer\\b|\\bdespair*\\b|\\bhate\\b|\\bpained\\b|\\bsuffered\\b|\\bdesperat*\\b|\\bhated\\b|\\bpainf*\\b|\\bsufferer*\\b|\\bdespis*\\b|\\bhateful*\\b|\\bpains\\b|\\bsuffering\\b|\\bdestroy*\\b|\\bhater*\\b|\\bpanic*\\b|\\bsuffers\\b|\\bdestruct\\b|\\bhates\\b|\\bparanoi*\\b|\\bsuspicio*\\b|\\bdestructed\\b|\\bhating\\b|\\bpathetic\\b|\\btantrum*\\b|\\bdestruction\\b|\\bhatred\\b|\\bpathetically\\b|\\btears\\b|\\bdestructive\\b|\\bhaunted\\b|\\bpeculiar*\\b|\\bteas*\\b|\\bdestructiveness\\b|\\bhazard*\\b|\\bperv\\b|\\btedious\\b|\\bdevastat*\\b|\\bheartbreak\\b|\\bperver*\\b|\\btemper\\b|\\bdevil*\\b|\\bheartbroke\\b|\\bpervy\\b|\\btempers\\b|\\bdifficult\\b|\\bheartless*\\b|\\bpessimis*\\b|\\btense\\b|\\bdifficulties\\b|\\bhell\\b|\\bpest*\\b|\\btensely\\b|\\bdifficulty\\b|\\bhellish\\b|\\bpetrif*\\b|\\btensing\\b|\\bdisadvantag\\b|\\bhelpless*\\b|\\bpettier\\b|\\btension*\\b|\\bdisagree*\\b|\\bhesita*\\b|\\bpettiest\\b|\\bterrible\\b|\\bdisappoint*\\b|\\bhomesick*\\b|\\bpetty\\b|\\bterribly\\b|\\bdisaster*\\b|\\bhopeless*\\b|\\bphobi*\\b|\\bterrified\\b|\\bdiscomfort*\\b|\\bhorrible\\b|\\bphony\\b|\\bterrifies\\b|\\bdiscourag*\\b|\\bhorribly\\b|\\bpiss*\\b|\\bterrify\\b|\\bdisgrac*\\b|\\bhorrid*\\b|\\bpitiable\\b|\\bterrifying\\b|\\bdisgust*\\b|\\bhorror*\\b|\\bpitied\\b|\\bterror*\\b|\\bdishearten*\\b|\\bhostil*\\b|\\bpities\\b|\\bthief\\b|\\bdishonor*\\b|\\bhumiliat*\\b|\\bpitiful\\b|\\bthiev*\\b|\\bdisillusion*\\b|\\bhungove\\b|\\bpitifully\\b|\\bthreat*\\b|\\bdislike\\b|\\bhurt*\\b|\\bpity*\\b|\\btimid*\\b|\\bdon't like\\b|\\bdo not like\\b|\\bdisliked\\b|\\bidiot*\\b|\\bpoison*\\b|\\btortur*\\b|\\bdislikes\\b|\\bignorable\\b|\\bpoor\\b|\\btraged*\\b|\\bdisliking\\b|\\bignoramus\\b|\\bpoorer\\b|\\btragically\\b",re.IGNORECASE)

from scipy.stats import norm

def analyze_text(text,filename,linenumber):
	text = text.lower().strip()
	results = []
	WordsCount=len(text.split())*1.0
	results.append(str(filename))
	results.append(str(linenumber))
	results.append(str(WordsCount))

	#Get individual scores


	we=len(we_re.findall(text))*1.0
	you=len(you_re.findall(text))*1.0
	i=len(i_re.findall(text))*1.0
	shehe=len(shehe_re.findall(text))*1.0

	social=len(social_re.findall(text))*1.0
	swear=len(swear_re.findall(text))*1.0
	negate=len(negate_re.findall(text))*1.0
	differ=len(differ_re.findall(text))*1.0

	article=len(article_re.findall(text))*1.0
	prep=len(prep_re.findall(text))*1.0
	pronoun=len(pronoun_re.findall(text))*1.0
	auxverb=len(auxverb_re.findall(text))*1.0
	negate=len(negate_re.findall(text))*1.0
	conj=len(conj_re.findall(text))*1.0
	adverb=len(adverb_re.findall(text))*1.0

	insight=len(insight_re.findall(text))*1.0
	relativ=len(relativ_re.findall(text))*1.0
	discrep=len(discrep_re.findall(text))*1.0

	posemo=len(posemo_re.findall(text))*1.0
	negemo=len(negemo_re.findall(text))*1.0


	analytic_zscore = ((30.0 + ((article) + (prep) - (pronoun) - (auxverb) - (negate) - (conj) - (adverb)) / WordsCount * 100.0) - 9.5) / 14.0
	clout_zscore = ((10.0 + ((we) + (you) + (social) - (i) - (swear) - (negate) - (differ)) / WordsCount * 100.0) - 10.0) / 10.0
	authentic_zscore = (((( (i) + (insight) + (differ) + (relativ) - (discrep) - (shehe)) / WordsCount * 100.0)) - 21.0) / 6.0
	tone_zscore = ((( (posemo) - (negemo) ) / WordsCount * 100.0) - 1.3) / 2.0



	analytic_score = norm.cdf(analytic_zscore)*100
	clout_score =  norm.cdf(clout_zscore)*100
	authentic_score = norm.cdf(authentic_zscore)*100
	tone_score = norm.cdf(tone_zscore)*100
	
	results.append(str(numpy.round(analytic_score,2)))
	results.append(str(numpy.round(clout_score,2)))
	results.append(str(numpy.round(authentic_score,2)))
	results.append(str(numpy.round(tone_score,2)))
	
	return results

def analyze_lines(files,output_file):
	results = numpy.zeros((1000,4+3)).astype("S100")
	k=0
	with open(output_file,"wb") as j:
		labels="\t".join(["Analytic","Clout","Authentic","Tone"])
		j.write("filename"+"\t"+"linenumber"+"\t"+"numberwords"+"\t"+labels+"\n")
		for filename in files: 
			with open(filename,"rb") as g:
				linenumber=1
				for line in g:
					res = analyze_text(line,filename,linenumber)
					if k < 1000: 
						results[k,:] = numpy.array(res)
						k+=1
					j.write("\t".join(res)+"\n")
					linenumber+=1
	return results[0:k,:]

def analyze_lines2(files):
	results = numpy.zeros((1000,4+3)).astype("S100")
	k=0
	for filename in files: 
		with open(filename,"rb") as g:
			linenumber=1
			for line in g:
				res = analyze_text(line,filename,linenumber)
				if k < 1000: 
					results[k,:] = numpy.array(res)
					k+=1
				linenumber+=1
	return results[0:k,:]
	
def filedialog(self):
	self.filelist=[]
	dlg = wx.FileDialog(self, message="Choose File",defaultFile="",style=wx.OPEN |  wx.MULTIPLE| wx.CHANGE_DIR)
	if dlg.ShowModal() == wx.ID_OK:
		paths = dlg.GetPaths()
		for path in paths:
			self.filelist.append(str(path))
	dlg.Destroy()
	return self.filelist

def folderdialog(self):
	self.filelist=[]
	dlg = wx.FileDialog(self, message="Choose File",defaultFile="", wildcard="*.dat",style=wx.SAVE | wx.OVERWRITE_PROMPT| wx.CHANGE_DIR)
	if dlg.ShowModal() == wx.ID_OK:
		infile = dlg.GetPath()
	dlg.Destroy()
	return infile

	
	
class MyForm(wx.Frame):
	global myGrid
	
	#----------------------------------------------------------------------
	def __init__(self):
		global main_self
		
		wx.Frame.__init__(self, None, wx.ID_ANY,title="TALC-X: The Automated Language Counter",size=(APP_SIZE_X, APP_SIZE_Y))
		self.SetMaxSize((APP_SIZE_X, APP_SIZE_Y))
		self.SetMinSize((APP_SIZE_X, APP_SIZE_Y))

		self.Bind(wx.EVT_CLOSE, self.onClose)
		
		
		self.panel_one = PanelOne(self)
		self.panel_two = PanelTwo(self)
		
		self.panel_two.Hide()
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.panel_one, 1, wx.EXPAND)
		self.sizer.Add(self.panel_two, 1, wx.EXPAND)
		
	
		self.SetSizer(self.sizer)
 
 
		
		fileMenu = wx.Menu()
		#switch_panels_menu_item1 = fileMenu.Append(wx.ID_ANY, "Compute Aggregation","Some text")
		switch_panels_menu_item1 = fileMenu.Append(wx.ID_ANY,"Analyze","Some text")
		switch_panels_menu_item2 = fileMenu.Append(wx.ID_ANY,"Results","Some text")
		switch_panels_menu_item3 = fileMenu.Append(wx.ID_ANY,"About","Some text")
		switch_panels_menu_item4 = fileMenu.Append(wx.ID_ANY,"Exit Program","Some text")
		
		#self.Bind(wx.EVT_MENU, self.onSwitchPanels1,switch_panels_menu_item1)
		self.Bind(wx.EVT_MENU, self.analyze,switch_panels_menu_item1)
		self.Bind(wx.EVT_MENU, self.results,switch_panels_menu_item2)
		self.Bind(wx.EVT_MENU, self.about,switch_panels_menu_item3)
		self.Bind(wx.EVT_MENU, self.onExitProgram,switch_panels_menu_item4)
		

		
		menubar = wx.MenuBar()
		menubar.Append(fileMenu, '&Menu')
		self.SetMenuBar(menubar)
		main_self=self
    #----------------------------------------------------------------------
	

	
	def analyze(self, event):
		self.SetTitle("TALC-X: Analyze Text")
		self.panel_two.Hide()
		self.panel_one.Show()
		self.Layout()
		
		
	def results(self, event=True):
		self.SetTitle("TALC-X: Analysis Results")
		self.panel_one.Hide()
		self.panel_two = PanelTwo(self)
		self.sizer.Add(self.panel_two, 1, wx.EXPAND)
		self.SetSizer(self.sizer)
		self.Layout()
		
	def about(self, event):
		wx.MessageBox('The summary variables are research-based composites that have been converted to 100-point scales where 0 = very low along the dimension and 100 = very high.  Analytic refers to analytical or formal thinking.  Clout taps writing that is authoritative, confident, and exhibits leadership.  Authenticity refers to writing that is personal and honest.  Emotional tone is scored such that higher numbers are more positive and upbeat and lower numbers are more negative.', 'About')

	def onTaskbar(self, evt):
		mainopen=0
		self.Hide()
		
	def onClose(self, evt):
		self.Destroy()
	
	def onExitProgram(self, event):
		dlg = wx.MessageDialog(self,"Do you really want to close this application?","Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
		result = dlg.ShowModal()
		dlg.Destroy()
		if result == wx.ID_OK:
			self.Destroy()

global outputdata
global headers
headers=["","","","","","",""]
outputdata=numpy.zeros((0,0))


class PanelTwo(wx.Panel):
	""""""
	
	
	def __init__(self, parent):

		"""Constructor"""
		wx.Panel.__init__(self, parent=parent)
		global outputdata
		global headers
		datafile=outputdata
		self.myGrid = wx.grid.Grid(self)
		self.myGrid.CreateGrid(datafile.shape[0], datafile.shape[1])
		for x in range(len(headers)):
			self.myGrid.SetColLabelValue(x, str(headers[x]))
		for i in range(0,datafile.shape[0]):
			for j in range(0,datafile.shape[1]):
				self.myGrid.SetCellValue(i,j, str(datafile[i,j]))
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.myGrid, 1, wx.EXPAND)
		self.SetSizer(sizer)	
	
	
########################################################################
class PanelOne(wx.Panel):
	#----------------------------------------------------------------------
	def __init__(self, parent):
		global filename
		global filename2
		global outputname
		"""Constructor"""
		wx.Panel.__init__(self, parent=parent)

	
		filename =""
		filename2 =""
		outputname =""
		
		self.label_1 = wx.StaticText(self, -1, "Please Enter the Following Information:",(20, 20))

		
		self.label_2 = wx.StaticText(self, -1, "Document(s):",(45, 55))
		self.text_ctrl_filename2 = wx.TextCtrl(self, -1, filename2,(140, 53),(200, 20) )
		wx.Button(self, 4, 'Select File(s)', (350, 53), (110, -1))

		self.label_1 = wx.StaticText(self, -1, "Output file name:",(45, 90 ))
		self.text_ctrl_output = wx.TextCtrl(self, -1, "",(140, 88),(200, 20) )	
		wx.Button(self, 3, 'Create Output File', (350, 88), (110, -1))
		
		
		wx.Button(self, 1, 'Analyze', (200, 130),(110, -1))
		#self.label_3 = wx.StaticText(self, -1, "\xa9 Hernandez, Newman, Jeon 2014",(360, 240))

		
		self.Bind(wx.EVT_BUTTON, self.Start, id=1)
		self.Bind(wx.EVT_BUTTON, self.Files, id=2)
		self.Bind(wx.EVT_BUTTON, self.destfile, id=3)
		self.Bind(wx.EVT_BUTTON, self.Files2, id=4)


		

###What happends when you press the Analyze button      
	def Start(self, event):

		global filename2
		global outputname
		global main_self
		global outputdata
		global headers
		headers=["Filename","Linenumber","Words","Analytic","Clout","Authenticity","Emotional"]
		wx.MessageBox('The program will now begin analyzing the text\n \n Please be patitent while the program is running', 'Status')
		if outputname!="":outputdata = analyze_lines(filename2,outputname)
		else:outputdata = analyze_lines2(filename2)
		#wx.MessageBox('The analysis is finished', 'Status')
		main_self.results()
		return 
####What happens when you press the Test Mode button	

	def display_results(self):
		global main_self
		main_self.panel_one.Hide()
		main_self.panel_two = PanelTwo(self)
		main_self.sizer.Add(main_self.panel_two, 1, wx.EXPAND)
		main_self.SetSizer(main_self.sizer)
		main_self.Layout()


	def destfile(self, event):
			global outputname
			outputname = folderdialog(self)
			self.text_ctrl_output.SetValue(str(outputname))

	def Files(self, event):
		global filename
		filename = filedialog(self)
		self.text_ctrl_filename.SetValue(",".join(filename))
		self.filename=filename
	
	def Files2(self, event):
		global filename2
		filename2 = filedialog(self)
		self.text_ctrl_filename2.SetValue(",".join(filename2))
		self.filename2=filename2
		



		
# Run the program
if __name__ == "__main__":
	app = wx.App(False)

	frame = MyForm()
	frame.Show()
	app.MainLoop()