import PageShell, { Block } from "@/components/PageShell";

export const metadata = {
  title: "Gizlilik ve veriler",
  description:
    "Neva hangi verileri tutuyor, ne kadar süreyle saklıyor ve nasıl siliniyor.",
};

export default function GizlilikPage() {
  return (
    <PageShell
      title="Gizlilik ve veriler"
      intro="Ruh sağlığıyla ilgili konuştuğun bir yerde neyin saklandığını bilmek hakkın. Kısa ve açık anlatalım."
    >
      <Block heading="Üyelik zorunlu değil">
        <p>
          Neva&apos;yı hesap açmadan kullanabilirsin. Bu durumda kimliğinle
          ilişkilendirilebilecek hiçbir bilgi istenmiyor; oturumun tarayıcında
          tutulan geçici bir kimlikle yürüyor.
        </p>
        <p>
          Karşılığında sohbetlerin saklanmıyor — bir sonraki gelişinde
          sıfırdan başlıyorsun. Hangisinin sana uygun olduğuna sen karar
          ver; ikisi de tam olarak çalışıyor.
        </p>
      </Block>

      <Block heading="Mesajların ne kadar kalıyor">
        <p>
          Bu, hesabının olup olmamasına göre değişiyor ve ikisini ayrı ayrı
          anlatmak istiyoruz.
        </p>
        <p>
          <strong>Üyeliksiz kullanırsan</strong> mesajların yalnızca sohbetin
          sürdüğü kadar tutuluyor. Yaklaşık bir saat işlem yapılmazsa oturum ve
          içindeki bütün mesajlar otomatik olarak siliniyor. Geri getirilemez.
        </p>
        <p>
          <strong>Hesabın varsa</strong> sohbetlerin sen silene kadar
          saklanıyor. Bunu sen istediğin için yapıyoruz: eski konuşmalarına
          dönebilmen, kaldığın yerden devam edebilmen ve zaman içindeki
          değişimi görebilmen bunu gerektiriyor. Otomatik bir silme süresi
          yok — karar sende.
        </p>
        <p>
          Sistem kayıtlarına mesaj içeriği yazılmıyor. Kayıtlarda yalnızca
          teknik bilgiler bulunuyor: isteğin ne kadar sürdüğü, hangi konu
          başlığında arama yapıldığı, kalite kontrolünden geçip geçmediği.
        </p>
      </Block>

      <Block heading="Hesap açarsan">
        <p>
          E-posta adresin ve şifrenin şifrelenmiş özeti saklanıyor. Şifrenin
          kendisi hiçbir yerde açık biçimde tutulmuyor.
        </p>
        <p>
          Ölçüm yaptıysan sonuçların hesabınla ilişkilendiriliyor — zaman
          içindeki değişimi görebilmen için.
        </p>
        <p>
          Konuşmalarından bazı sinyaller çıkarılıyor: tekrar eden konular,
          denediğin teknikler ve bunların sana iyi gelip gelmediği. Bunlar
          Neva&apos;nın seni hatırlaması içindir, bir değerlendirme ya da tanı
          değildir ve yanılabilirler. Ne çıkarıldığını Gelişimim sayfasından
          görebilir, tek tuşla silebilirsin — sohbetlerin yerinde kalır.
        </p>
      </Block>

      <Block heading="Silme hakkı">
        <p>
          Sohbetlerini tek tek silebilirsin: sohbet listesindeki çöp kutusu
          simgesi o konuşmayı ve içindeki bütün mesajları kaldırır.
        </p>
        <p>
          Konuşmalardan çıkarılan notları ayrıca silebilirsin; bunun için
          sohbetlerinden vazgeçmen gerekmiyor.
        </p>
        <p>
          Hesabını silersen hesabına bağlı her şey — sohbetler, mesajlar,
          ölçüm sonuçları, çıkarılan notlar ve açık oturumlar — birlikte
          siliniyor. Bu işlem geri alınamıyor.
        </p>
      </Block>

      <Block heading="Oturum güvenliği">
        <p>
          Giriş yaptığında tarayıcına, JavaScript&apos;in okuyamadığı bir
          oturum çerezi bırakılıyor. Bu, sitede bir açık olsa bile oturumunun
          çalınmasını zorlaştırıyor.
        </p>
        <p>
          Hesabım sayfasından açık oturumlarını görebilir, tanımadığın bir
          cihazı kapatabilir ya da tek seferde hepsinden çıkabilirsin. Şifreni
          değiştirdiğinde diğer cihazlardaki oturumlar kendiliğinden kapanıyor.
        </p>
      </Block>

      <Block heading="Nerede tutuluyor">
        <p>
          Veriler Avrupa Birliği sınırları içindeki sunucularda (Frankfurt)
          barındırılıyor. Yapay zekâ cevaplarının üretimi için Anthropic
          altyapısı kullanılıyor; bu sağlayıcıya gönderilen içerik model
          eğitiminde kullanılmıyor.
        </p>
      </Block>

      <Block heading="Yapay zekâ olduğu açıkça belirtilir">
        <p>
          Neva bir yapay zekâ sistemidir ve bunu hiçbir noktada gizlemez.
          İnsan bir uzman olduğu izlenimi vermez. Her cevabın nasıl üretildiğini
          inceleyebilmen için şeffaflık paneli sunar. Bu yaklaşım Avrupa Birliği
          Yapay Zekâ Yasası&apos;nın şeffaflık ilkeleriyle uyumludur.
        </p>
      </Block>
    </PageShell>
  );
}
