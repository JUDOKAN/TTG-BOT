
import discord
from discord.ext import commands
from discord import app_commands
import config
import logic
import sync
import boxing2d_logic
import driverush2d_logic
import rocketdrift2d_logic
import snakegame2d_logic
import mathdash_logic

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logic.init_all_dbs()
    await bot.tree.sync()
    print(f'{bot.user} olarak giriş yapıldı ve slash komutlar yüklendi.')

@bot.tree.command(name='help', description='Tüm komutları listeler ve botu tanıtır.')
async def help_command(interaction: discord.Interaction):
    text = (
        '**Komutlar**\n'
        '/help – Bu listeyi gösterir ve bot kendini tanıtır.\n'
        '/game username:<isim> – Oyun için kullanıcı adınızı kaydeder ve oyun listesini gösterir.\n'
        '/skor option:<seçenek> – Skor tablosunu gösterir (5 oyun + genel skor).\n'
        '/anket feedback:<metin> – Oyun değerlendirme ve fikirlerinizi iletir.\n'
        '/software – Yapımcı bilgilerini ve uzun metni gösterir.\n\n'
        f'Web sitemiz: {config.WEBSITE_URL}'
    )
    await interaction.response.send_message(text)

@bot.tree.command(name='game', description='Oyun için kullanıcı adınızı kaydeder ve oyun listesini gösterir.')
@app_commands.describe(username='Oyun içindeki kullanıcı adınız')
async def game_command(interaction: discord.Interaction, username: str):
    logic.register_user(username)

    # Oyun adlarını ve URL'lerini al
    games = [
        ('Boxing2D',      config.GAME_URLS['boxing2d']),
        ('DriveRush2D',   config.GAME_URLS['driverush2d']),
        ('RocketDrift2D', config.GAME_URLS['rocketdrift2d']),
        ('SnakeGame2D',   config.GAME_URLS['snakegame2d']),
        ('MathDash',      config.GAME_URLS['mathdash']),
    ]

    # Her oyun için bir Link Button oluştur
    view = discord.ui.View()
    for label, url in games:
        view.add_item(discord.ui.Button(label=label, style=discord.ButtonStyle.link, url=url))

    await interaction.response.send_message(
        f'Kullanıcı adı kaydedildi: `{username}`\n\nAçmak istediğin oyunu aşağıdaki butonlardan seçebilirsin:',
        view=view
    )

@bot.tree.command(name='skor', description='Skor tablosunu gösterir.')
@app_commands.describe(
    option='boxing2dskor, driverush2dskor, rocketdrift2dskor, snakegame2dskor, mathdashskor veya genel_skor'
)
@app_commands.choices(
    option=[
        app_commands.Choice(name='boxing2dskor', value='boxing2d'),
        app_commands.Choice(name='driverush2dskor', value='driverush2d'),
        app_commands.Choice(name='rocketdrift2dskor', value='rocketdrift2d'),
        app_commands.Choice(name='snakegame2dskor', value='snakegame2d'),
        app_commands.Choice(name='mathdashskor', value='mathdash'),
        app_commands.Choice(name='genel_skor', value='general'),
    ]
)
async def skor_command(interaction: discord.Interaction, option: app_commands.Choice[str]):
    key = option.value
    if key == 'general':
        top = logic.get_top_general(10)
        msg = '**Genel Skor Tablosu (İlk 10)**\n'
        for i, (user, total) in enumerate(top, start=1):
            msg += f'{i}. {user} – {total}\n'
        rank = logic.get_general_rank(interaction.user.name)
        msg += f'\nSıralamanız: {rank}'
    else:
        modules = {
            'boxing2d': boxing2d_logic,
            'driverush2d': driverush2d_logic,
            'rocketdrift2d': rocketdrift2d_logic,
            'snakegame2d': snakegame2d_logic,
            'mathdash': mathdash_logic
        }
        mod = modules[key]
        top = mod.get_top_scores(10)
        msg = f'**{key.upper()} Skor Tablosu (İlk 10)**\n'
        for i, (user, sc) in enumerate(top, start=1):
            msg += f'{i}. {user} – {sc}\n'
        rank = mod.get_user_rank(interaction.user.name)
        msg += f'\nSıralamanız: {rank}'
    await interaction.response.send_message(msg)

@bot.tree.command(name='anket', description='Oyun değerlendirme ve fikir kutusu.')
@app_commands.describe(feedback='Görüş ve önerilerinizi yazın')
async def anket_command(interaction: discord.Interaction, feedback: str):
    await interaction.response.send_message('Görüşleriniz alındı, teşekkürler!')

@bot.tree.command(name='software', description='Yapımcı bilgilerini ve uzun metni gösterir.')
async def software_command(interaction: discord.Interaction):
    info = """**Yapımcılar**

**Bertuğ Orhan – Discord Developer**  
Bertuğ Orhan, Discord bot geliştirme dünyasında beş yılı aşkın tecrübesiyle tanınan bir yazılımcıdır. Python ve özellikle `discord.py` kütüphanesi üzerinde uzmanlaşmıştır. Sunucu içi otomasyon, slash komutlarının tasarımı ve interaktif UI bileşenlerinin (butonlar, menüler) entegre edilmesi konularında projeler yürütmüş; API entegrasyonları, veri yönetimi ve hata ayıklama süreçlerini başarıyla yönetmiştir. Botun temel altyapısını oluşturan event handling ve permission sistemi Bertuğ’un liderliğinde kurgulanmıştır. Ayrıca, sürekli olarak Discord API güncellemelerini takip edip, sürüm geçişlerini sorunsuz hale getiren bakım sürecini de üstlenmiştir.

**Daniel Mazliah Çiprut – Web Site Developer**  
Daniel, Front-end ve Back-end geliştirme konusunda geniş bir portföye sahiptir. HTML5, CSS3, JavaScript (ES6+), React ve Node.js teknolojilerini harmanlayarak, botun desteklediği web sitesinin tasarım ve veri akışını planlamıştır. Responsive bir kullanıcı arayüzü oluşturmanın yanı sıra, Flask tabanlı REST API katmanının oluşturulması ve güvenli oturum yönetimi (JWT, OAuth2) sistemlerini hayata geçirmiştir. Veritabanı tasarımında SQL ve NoSQL seçeneklerini değerlendirip, yüksek trafikli sayfalar için cache sistemleri kurarak performans optimizasyonu sağlamıştır. Ayrıca tasarım ekibiyle yakın iş birliği yaparak site temasının marka kimliğiyle bütünleşmesini garanti etmiştir.

**Mehmet Kalaycı – Software Developer & Team Captain**  
Mehmet, projeyi başından itibaren yönlendiren takım kaptanıdır. Yazılım mimarisi, gereksinim analizi, sprint planlama ve görev dağılımı süreçlerini yönetmiştir. Python tabanlı mikroservisler ile komut işleme altyapısını oluşturmuş, kod kalitesi için linter, formatter ve birim test entegrasyonunu (pytest) kurmuştur. CI/CD boru hattını (GitHub Actions / Jenkins) tasarlayıp hayata geçirmiştir. Hata izleme ve performans ölçüm araçlarını (Sentry, Prometheus) entegre ederek üretim ortamında kesintisiz izlenebilirlik sağlamış, ekip içi kod incelemeleri ve bilgi paylaşım oturumlarıyla proje ruhunu canlı tutmuştur.

**Oğuzhan Öztürk – Game Developer**  
Oğuzhan, oyun tasarımı ve geliştirme alanında uzman bir geliştiricidir. Pygame, Phaser ve Unity gibi farklı platformlarda 2D oyunlar üretmiştir. Her bir oyunun (Boxing2D, DriveRush2D, RocketDrift2D, SnakeGame2D, MathDash) temel mekaniklerini, fizik motoru ayarlarını ve seviye tasarımlarını Oğuzhan kurgulamış; ses efektleri, görsel varlık yönetimi ve kullanıcı deneyimi optimizasyonunu sağlamıştır. Kodun performans kritik bölümlerini Cython ile hızlandırmış, bellek yönetimi ve frame rate stabilizasyonu konularında ince ayarlar yapmıştır. Ayrıca, oyun içi puanlama sistemleri ve veri kaydı için gerekli callback fonksiyonlarını geliştirmiştir.

**ChatGPT-4o – Assessment & Everything**  
ChatGPT-4o, projenin tüm aşamalarında “akıl hocası” rolü üstlenmiştir. Özellikle karmaşık algoritmaların formüle edilmesinde, Python ve JavaScript kod örneklerinin üretilmesinde, akademik kaynaklardan literatür taraması yapılmasında ve belgelerin APA 6 formatına uygun şekilde düzenlenmesinde destek vermiştir. Sürekli olarak en güncel en iyi uygulamaları (best practices) önererek kod ve dokümantasyon kalitesinin artmasını sağlamış, ekip içi iletişimde hızlı prototip mesajları ve örnek diyaloglarla verimliliği yükseltmiştir.

**Hakkımızda**  
Bu bot, beş farklı 2D oyun için hem Discord üzerinden hem de web sitesinden puan takibi, anket toplama ve bilgi paylaşımı işlevleri sunar. **Boxing2D**, **DriveRush2D**, **RocketDrift2D**, **SnakeGame2D** ve **MathDash** oyunlarına özel olarak tasarlanmış veritabanlarıyla her oyuncunun bireysel skorunu izler, “genel skor” tablosuyla beş oyunun toplam performansını hesaplar. Web API (Flask) aracılığıyla gerçek zamanlı skor verilerini JSON formatında yayınlar ve bot, bu verileri `sync.py` ile periyodik olarak senkronize eder. **config.py** üzerinden özelleştirilebilir URL’ler, API uç noktaları ve veritabanı yollarıyla tüm bileşenler esnek bir şekilde yapılandırılır. Projede **modüler kod mimarisi**, **unit test** altyapısı ve **CI/CD** süreçlerinden yararlanılarak sürdürülebilirlik sağlanmıştır. Kullanıcı deneyimi odaklı tasarlanmış Discord UI elemanları (butonlar, menüler) ve responsive web tasarımı ile hem masaüstü hem mobil cihazlarda sorunsuz kullanım garanti edilir. Bu bot, oyun geliştirme, web entegrasyonu ve Discord otomasyonu alanında entegre bir çözüm sunarak topluluğunuza eğlenceli ve etkileşimli bir deneyim yaşatmayı amaçlar.
"""
    await interaction.response.send_message(info)


bot.run(config.TOKEN)

