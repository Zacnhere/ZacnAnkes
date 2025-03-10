import string

from pyrogram import filters
from time import time

from Teiko import *


admins_in_chat = {}

async def list_admins(client, chat_id: int):
    global admins_in_chat
    
    admins_in_chat[chat_id] = {
        "last_updated_at": time(),
        "data": [
            member.user.id
            async for member in client.get_chat_members(
                chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS
            )
        ],
    }
    return admins_in_chat[chat_id]["data"]


async def isGcast(filter, client, update):
    with open('bl.txt') as file:
        blc = [w.lower().strip() for w in file.readlines()]

    bl_chars = "§∆π©®$€¥£¢𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚏𝚠𝚡𝚢𝚣𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐟𝐰𝐱𝐲𝐳𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒇𝒘𝒙𝒚𝒛𝑎𝑏𝑐𝑑𝑒𝑓𝑔ℎ𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑓𝑤𝑥𝑦𝑧ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜғᴡxʏᴢ𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝒻𝓌𝓍𝓎𝓏𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓯𝔀𝔁𝔂𝔃ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᶠʷˣʸᶻᗩᗷᑕᗪᗴᖴᘜᕼIᒍKᒪᗰᑎOᑭᑫᖇՏTᑌᖴᗯ᙭Yᘔ𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝗳𝘄𝘅𝘆𝘇𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙛𝙬𝙭𝙮𝙯𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘧𝘸𝘹𝘺𝘻🅐︎🅑︎🅒︎🅓︎🅔︎🅕︎🅖︎🅗︎🅘︎🅙︎🅚︎🅛︎🅜︎🅝︎🅞︎🅟︎🅠︎🅡︎🅢︎🅣︎🅤︎🅕︎🅦︎🅧︎🅨︎🅩︎𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔣𝔴𝔵𝔶𝔷ɐbɔdǝɟƃɥᴉɾʞlɯnodbɹsʇnɟʍxƃza‌‌b‌‌c‌‌d‌‌e‌‌f‌‌g‌‌h‌‌i‌‌j‌‌k‌‌l‌‌m‌‌n‌‌o‌‌p‌‌q‌‌r‌‌s‌‌t‌‌u‌‌f‌‌w‌‌x‌‌y‌‌z‌‌ă‌b‌‌c‌‌d‌‌ĕ‌f‌‌ğ‌h‌‌ĭ‌j‌‌k‌‌l‌‌m‌‌n‌‌ŏ‌p‌‌q‌‌r‌‌s‌‌t‌‌ŭ‌f‌‌w‌‌x‌‌y‌‌z‌‌ȃ‌b‌‌c‌‌d‌‌ȇ‌f‌‌g‌‌h‌‌ȋ‌j‌‌k‌‌l‌‌m‌‌n‌‌ȏ‌p‌‌q‌‌ȓ‌s‌‌t‌‌ȗ‌f‌‌w‌‌x‌‌y‌‌z‌‌🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯 🇰 🇱 🇲 🇳 🇴 🇵 🇶 🇷 🇸 🇹 🇺 🇫 🇼 🇽 🇾 🇿🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🄵🅆🅇🅈🅉🅰︎🅱︎🅲︎🅳︎🅴︎🅵︎🅶︎🅷︎🅸︎🅹︎🅺︎🅻︎🅼︎🅽︎🅾︎🅿︎🆀︎🆁︎🆂︎🆃︎🆄︎🅵︎🆆︎🆇︎🆈︎🆉︎ꪖ᥇ᥴᦔꫀᠻᧁꫝ𝓲𝓳𝘬ꪶꪑꪀꪮρ𝘲𝘳𝘴𝓽ꪊᠻ᭙᥊ꪗɀ卂乃匚ᗪ乇千ᘜ卄|ﾌҜㄥ爪几ㄖ卩Ҩ尺丂ㄒㄩ千山乂ㄚ乙a‌b‌c‌d‌e‌f‌g‌h‌i‌j‌k‌l‌m‌n‌o‌p‌q‌r‌s‌t‌u‌f‌w‌x‌y‌z‌ḁ‌b‌‌c‌‌d‌‌e‌‌f‌‌g‌‌h‌‌i‌‌j‌‌k‌‌l‌‌m‌‌n‌‌o‌‌p‌‌q‌‌r‌‌s‌‌t‌‌u‌‌f‌‌w‌‌x‌‌y‌‌z‌‌a‌b‌c‌d‌e‌f‌g‌h‌i‌j‌k‌l‌m‌n‌o‌p‌q‌r‌s‌t‌u‌f‌w‌x‌y‌z‌ꍏꌃꏳꀷꏂꎇꁅꀍꀤ꒻ꀘ꒒ꎭꈤꂦᖘꆰꋪꌚ꓄ꀎꎇꅐꉧꌩꁴa҈b҈c҈d҈e҈f҈g҈h҈i҈j҈k҈l҈m҈n҈o҈p҈q҈r҈s҈t҈u҈f҈w҈x҈y҈z҈a‌b‌c‌d‌e‌f‌g‌h‌i‌j‌k‌l‌m‌n‌o‌p‌q‌r‌s‌t‌u‌f‌w‌x‌y‌z‌a⃠b⃠c⃠d⃠e⃠f⃠g⃠h⃠i⃠j⃠k⃠l⃠m⃠n⃠o⃠p⃠q⃠r⃠s⃠t⃠u⃠f⃠w⃠x⃠y⃠z⃠a‌‌b‌‌c‌‌d‌‌e‌‌f‌‌g‌‌h‌‌i‌‌j‌‌k‌‌l‌‌m‌‌n‌‌o‌‌p‌‌q‌‌r‌‌s‌‌t‌‌u‌‌f‌‌w‌‌x‌‌y‌‌z‌‌a‌b‌c‌d‌e‌f‌g‌h‌i‌j‌k‌l‌m‌n‌o‌p‌q‌r‌s‌t‌u‌f‌w‌x‌y‌z‌ልጌርዕቿቻኗዘጎጋጕረጠክዐየዒዪነፕሁቻሠሸሃጊa‌b‌c‌d‌e‌f‌g‌h‌i‌j‌k‌l‌m‌n‌o‌p‌q‌r‌s‌t‌u‌f‌w‌x‌y‌z‌a༙b༙c༙d༙e༙f༙g༙h༙i༙j༙k༙l༙m༙n༙o༙p༙q༙r༙s༙t༙u༙f༙w༙x༙y༙z༙𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝙵𝚆𝚇𝚈𝚉𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐅𝐖𝐗𝐘𝐙𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑭𝑾𝑿𝒀𝒁𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝐹𝑊𝑋𝑌𝑍𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰ℱ𝒲𝒳𝒴𝒵𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓕𝓦𝓧𝓨𝓩𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗙𝗪𝗫𝗬𝗭𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙁𝙒𝙓𝙔𝙕𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘍𝘞𝘟𝘠𝘡𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔉𝔚𝔛𝔜ℨA‌‌B‌‌C‌‌D‌‌E‌‌F‌‌G‌‌H‌‌I‌‌J‌‌K‌‌L‌‌M‌‌N‌‌O‌‌P‌‌Q‌‌R‌‌S‌‌T‌‌U‌‌F‌‌W‌‌X‌‌Y‌‌Z‌‌Ă‌B‌‌C‌‌D‌‌Ĕ‌F‌‌Ğ‌H‌‌Ĭ‌J‌‌K‌‌L‌‌M‌‌N‌‌Ŏ‌P‌‌Q‌‌R‌‌S‌‌T‌‌Ŭ‌F‌‌W‌‌X‌‌Y‌‌Z‌‌Ȃ‌B‌‌C‌‌D‌‌Ȇ‌F‌‌G‌‌H‌‌Ȋ‌J‌‌K‌‌L‌‌M‌‌N‌‌Ȏ‌P‌‌Q‌‌Ȓ‌S‌‌T‌‌Ȗ‌F‌‌W‌‌X‌‌Y‌‌Z‌‌A‌B‌C‌D‌E‌F‌G‌H‌I‌J‌K‌L‌M‌N‌O‌P‌Q‌R‌S‌T‌U‌F‌W‌X‌Y‌Z‌Ḁ‌B‌‌C‌‌D‌‌E‌‌F‌‌G‌‌H‌‌I‌‌J‌‌K‌‌L‌‌M‌‌N‌‌O‌‌P‌‌Q‌‌R‌‌S‌‌T‌‌U‌‌F‌‌W‌‌X‌‌Y‌‌Z‌‌A‌B‌C‌D‌E‌F‌G‌H‌I‌J‌K‌L‌M‌N‌O‌P‌Q‌R‌S‌T‌U‌F‌W‌X‌Y‌Z‌A҈B҈C҈D҈E҈F҈G҈H҈I҈J҈K҈L҈M҈N҈O҈P҈Q҈R҈S҈T҈U҈F҈W҈X҈Y҈Z҈A‌B‌C‌D‌E‌F‌G‌H‌I‌J‌K‌L‌M‌N‌O‌P‌Q‌R‌S‌T‌U‌F‌W‌X‌Y‌Z‌A‌‌B‌‌C‌‌D‌‌E‌‌F‌‌G‌‌H‌‌I‌‌J‌‌K‌‌L‌‌M‌‌N‌‌O‌‌P‌‌Q‌‌R‌‌S‌‌T‌‌U‌‌F‌‌W‌‌X‌‌Y‌‌Z‌‌A‌B‌C‌D‌E‌F‌G‌H‌I‌J‌K‌L‌M‌N‌O‌P‌Q‌R‌S‌T‌U‌F‌W‌X‌Y‌Z‌A‌B‌C‌D‌E‌F‌G‌H‌I‌J‌K‌L‌M‌N‌O‌P‌Q‌R‌S‌T‌U‌F‌W‌X‌Y‌Z‌A༙B༙C༙D༙E༙F༙G༙H༙I༙J༙K༙L༙M༙N༙O༙P༙Q༙R༙S༙T༙U༙F༙W༙X༙Y༙Z༙𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂ℒ𝑀ℕ𝑂ℙ𝑄ℝ𝑆𝑇𝑈𝑉𝑊𝑋𝑌ℤ"
    blc.extend(bl_chars)

    white_list = await DB.get_list_vars(TB.me.id, f"whitelist_{update.chat.id}") or []
    if update.from_user.id in white_list:
        return False

    if update.from_user.id in (await list_admins(client, update.chat.id)):
        return False

    bl_words = await DB.get_vars(TB.me.id, f"word_{update.chat.id}") or []
    if any(chara in update.text for chara in blc) or any(word in update.text for word in bl_words):
        return True

    return False

Ankes = filters.create(isGcast)
